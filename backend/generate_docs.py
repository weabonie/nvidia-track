"""
Main orchestration script for documentation generation.
End-to-end workflow from spec to containerized docs site.
"""

import argparse
import sys
from pathlib import Path
import subprocess
import shutil

from nim_client import NIMClient
from spec_schema import ProjectSpec
from ia_planner import IAPlanner, DocumentationPlan
from docusaurus_scaffolder import DocusaurusScaffolder
from content_generator import ContentGenerator
from sidebar_generator import SidebarGenerator
from quality_checker import QualityChecker


class DocsOrchestrator:
    """Main orchestrator for the documentation generation pipeline."""
    
    def __init__(
        self,
        spec_path: str,
        site_dir: str,
        nim_url: str = "http://localhost:8000/v1"
    ):
        """
        Initialize orchestrator.
        
        Args:
            spec_path: Path to project spec JSON file
            site_dir: Directory for Docusaurus site
            nim_url: NIM endpoint URL
        """
        self.spec_path = Path(spec_path)
        self.site_dir = Path(site_dir).absolute()
        self.plan_path = self.site_dir.parent / f"{self.site_dir.name}_plan.json"
        
        # Initialize clients
        self.nim_client = NIMClient(nim_url)
        
        # Load spec
        print(f"Loading spec from {self.spec_path}...")
        self.spec = ProjectSpec.from_json_file(str(self.spec_path))
        
        # Validate spec
        warnings = self.spec.validate_spec()
        if warnings:
            print("\nSpec validation warnings:")
            for warning in warnings:
                print(f"  ⚠ {warning}")
            print()
    
    def check_nim_health(self) -> bool:
        """Check if NIM endpoint is healthy."""
        print("Checking NIM endpoint health...")
        
        if not self.nim_client.check_health():
            print("✗ NIM endpoint is not reachable or has no models")
            print("  Make sure NVIDIA NIM is running locally at the configured URL")
            return False
        
        try:
            model = self.nim_client.get_nemotron_model()
            print(f"✓ NIM endpoint is healthy (using model: {model})")
            return True
        except Exception as e:
            print(f"✗ Failed to get Nemotron model: {e}")
            return False
    
    def plan_documentation(self, reuse_plan: bool = True) -> DocumentationPlan:
        """
        Plan documentation IA.
        
        Args:
            reuse_plan: Whether to reuse existing plan if available
            
        Returns:
            Documentation plan
        """
        # Check for existing plan
        if reuse_plan and self.plan_path.exists():
            print(f"Reusing existing plan from {self.plan_path}")
            return DocumentationPlan.load(str(self.plan_path))
        
        # Generate new plan
        print("Planning documentation structure with Nemotron...")
        planner = IAPlanner(self.nim_client)
        plan = planner.plan_documentation(self.spec)
        
        # Validate plan
        warnings = plan.validate_plan()
        if warnings:
            print("\nPlan validation warnings:")
            for warning in warnings:
                print(f"  ⚠ {warning}")
            print()
        
        # Save plan
        plan.save(str(self.plan_path))
        print(f"✓ Plan saved to {self.plan_path}")
        
        # Print summary
        print(f"\nPlanned {len(plan.sections)} sections:")
        for section in plan.sections:
            print(f"  - {section.name}: {len(section.pages)} pages")
        print()
        
        return plan
    
    def scaffold_site(self, plan: DocumentationPlan) -> DocusaurusScaffolder:
        """
        Scaffold Docusaurus site.
        
        Args:
            plan: Documentation plan
            
        Returns:
            Scaffolder instance
        """
        scaffolder = DocusaurusScaffolder(str(self.site_dir))
        
        # Create or configure site
        scaffolder.scaffold_site(self.spec.project_name)
        
        # Clear default docs
        scaffolder.clear_default_docs()
        
        # Create section directories
        section_names = [s.name for s in plan.sections]
        scaffolder.create_directory_structure(section_names)
        
        return scaffolder
    
    def generate_content(self, plan: DocumentationPlan, regenerate_all: bool = False) -> None:
        """
        Generate documentation content.
        
        Args:
            plan: Documentation plan
            regenerate_all: Whether to regenerate all pages (vs only missing)
        """
        generator = ContentGenerator(self.nim_client)
        docs_dir = self.site_dir / "docs"
        
        if regenerate_all:
            print("Generating all documentation pages...")
            generator.generate_all_pages(self.spec, plan, docs_dir)
        else:
            print("Generating missing documentation pages...")
            
            # Generate homepage if missing
            homepage = docs_dir / "index.md"
            if not homepage.exists():
                generator.generate_homepage(self.spec, plan, homepage)
            else:
                print("Homepage already exists, skipping")
            
            # Generate missing section pages
            for section in plan.sections:
                for page in section.pages:
                    page_file = docs_dir / section.name / f"{page.slug}.md"
                    if not page_file.exists():
                        generator.generate_page(page, self.spec, plan, page_file)
                    else:
                        print(f"Page {section.name}/{page.slug} already exists, skipping")
    
    def generate_sidebar(self, plan: DocumentationPlan) -> None:
        """
        Generate sidebar configuration.
        
        Args:
            plan: Documentation plan
        """
        generator = SidebarGenerator(plan)
        sidebar_path = self.site_dir / "sidebars.js"
        generator.generate_sidebar(sidebar_path)
        
        # Validate sidebar
        docs_dir = self.site_dir / "docs"
        warnings = generator.validate_sidebar(docs_dir)
        if warnings:
            print("\nSidebar validation warnings:")
            for warning in warnings:
                print(f"  ⚠ {warning}")
            print()
    
    def run_quality_checks(self, plan: DocumentationPlan) -> bool:
        """
        Run quality gates.
        
        Args:
            plan: Documentation plan
            
        Returns:
            True if all checks passed
        """
        docs_dir = self.site_dir / "docs"
        checker = QualityChecker(self.spec, plan, docs_dir)
        gates = checker.run_all_checks()
        return checker.print_report(gates)
    
    def build_site(self, scaffolder: DocusaurusScaffolder) -> Path:
        """
        Build static site.
        
        Args:
            scaffolder: Scaffolder instance
            
        Returns:
            Path to build directory
        """
        print("\nBuilding static site...")
        scaffolder.ensure_dependencies()
        build_dir = scaffolder.build_site()
        return build_dir
    
    def build_container(self) -> None:
        """Build Docker container."""
        print("\nBuilding Docker container...")
        
        # Copy Dockerfile to site directory
        dockerfile_src = Path(__file__).parent / "Dockerfile"
        dockerfile_dst = self.site_dir / "Dockerfile"
        
        if dockerfile_src.exists():
            shutil.copy(dockerfile_src, dockerfile_dst)
        
        # Build image
        image_name = f"{self.spec.project_name.lower().replace(' ', '-')}-docs"
        
        try:
            subprocess.run(
                ["docker", "build", "-t", image_name, "."],
                cwd=str(self.site_dir),
                check=True
            )
            print(f"✓ Container image built: {image_name}")
            print(f"\nTo run the container:")
            print(f"  docker run -p 3000:80 {image_name}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Container build failed: {e}")
            raise
    
    def run_container(self) -> None:
        """Run Docker container locally."""
        print("\nRunning Docker container...")
        
        image_name = f"{self.spec.project_name.lower().replace(' ', '-')}-docs"
        
        try:
            subprocess.run(
                [
                    "docker", "run",
                    "-d",
                    "-p", "3000:80",
                    "--name", f"{image_name}-instance",
                    image_name
                ],
                check=True
            )
            print(f"✓ Container running at http://localhost:3000")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to run container: {e}")
            raise
    
    def run_full_pipeline(
        self,
        replan: bool = False,
        regenerate: bool = False,
        build: bool = True,
        containerize: bool = False,
        run_container: bool = False
    ) -> None:
        """
        Run the full documentation generation pipeline.
        
        Args:
            replan: Whether to regenerate the IA plan
            regenerate: Whether to regenerate all content
            build: Whether to build the static site
            containerize: Whether to build the Docker container
            run_container: Whether to run the container locally
        """
        print("=" * 60)
        print("DOCUMENTATION GENERATION PIPELINE")
        print("=" * 60 + "\n")
        
        # Step 1: Check NIM health
        if not self.check_nim_health():
            print("\n✗ Pipeline aborted: NIM endpoint not available")
            sys.exit(1)
        
        # Step 2: Plan IA
        plan = self.plan_documentation(reuse_plan=not replan)
        
        # Step 3: Scaffold site
        scaffolder = self.scaffold_site(plan)
        
        # Step 4: Generate content
        self.generate_content(plan, regenerate_all=regenerate)
        
        # Step 5: Generate sidebar
        self.generate_sidebar(plan)
        
        # Step 6: Run quality checks
        print("\n" + "=" * 60)
        print("Running quality checks...")
        print("=" * 60)
        all_passed = self.run_quality_checks(plan)
        
        if not all_passed:
            print("\n⚠ Some quality checks failed, but continuing...")
        
        # Step 7: Build site
        if build:
            build_dir = self.build_site(scaffolder)
            print(f"\n✓ Static site ready at {build_dir}")
        
        # Step 8: Containerize
        if containerize:
            self.build_container()
        
        # Step 9: Run container
        if run_container:
            self.run_container()
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"\nSite directory: {self.site_dir}")
        print(f"Plan file: {self.plan_path}")
        if build:
            print(f"Static build: {self.site_dir / 'build'}")
        print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from project spec using local Nemotron"
    )
    
    parser.add_argument(
        "spec",
        help="Path to project specification JSON file"
    )
    
    parser.add_argument(
        "--site-dir",
        default="./docs-site",
        help="Directory for Docusaurus site (default: ./docs-site)"
    )
    
    parser.add_argument(
        "--nim-url",
        default="http://localhost:8000/v1",
        help="NVIDIA NIM endpoint URL (default: http://localhost:8000/v1)"
    )
    
    parser.add_argument(
        "--replan",
        action="store_true",
        help="Regenerate documentation plan (ignore existing plan)"
    )
    
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Regenerate all content (ignore existing pages)"
    )
    
    parser.add_argument(
        "--no-build",
        action="store_true",
        help="Skip building the static site"
    )
    
    parser.add_argument(
        "--containerize",
        action="store_true",
        help="Build Docker container"
    )
    
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run Docker container locally (implies --containerize)"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not Path(args.spec).exists():
        print(f"Error: Spec file not found: {args.spec}")
        sys.exit(1)
    
    # Create orchestrator
    orchestrator = DocsOrchestrator(
        spec_path=args.spec,
        site_dir=args.site_dir,
        nim_url=args.nim_url
    )
    
    # Run pipeline
    try:
        orchestrator.run_full_pipeline(
            replan=args.replan,
            regenerate=args.regenerate,
            build=not args.no_build,
            containerize=args.containerize or args.run,
            run_container=args.run
        )
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
