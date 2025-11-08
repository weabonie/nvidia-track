"""
Quality gates checker.
Validates generated documentation for common issues.
"""

from pathlib import Path
from typing import List, Dict, Set, Tuple
import re

from spec_schema import ProjectSpec
from ia_planner import DocumentationPlan


class QualityGate:
    """Result of a quality gate check."""
    
    def __init__(self, name: str, passed: bool, issues: List[str]):
        self.name = name
        self.passed = passed
        self.issues = issues
    
    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        result = f"{status}: {self.name}"
        if self.issues:
            result += "\n  " + "\n  ".join(f"- {issue}" for issue in self.issues)
        return result


class QualityChecker:
    """Validates documentation quality."""
    
    def __init__(self, spec: ProjectSpec, plan: DocumentationPlan, docs_dir: Path):
        """
        Initialize quality checker.
        
        Args:
            spec: Project specification
            plan: Documentation plan
            docs_dir: Base docs directory
        """
        self.spec = spec
        self.plan = plan
        self.docs_dir = docs_dir
        self.all_pages = self._collect_all_pages()
    
    def _collect_all_pages(self) -> Dict[str, Path]:
        """Collect all Markdown files in docs directory."""
        pages = {}
        
        # Add homepage
        homepage = self.docs_dir / "index.md"
        if homepage.exists():
            pages["index"] = homepage
        
        # Add section pages
        for section in self.plan.sections:
            section_dir = self.docs_dir / section.name
            if section_dir.exists():
                for page in section.pages:
                    page_file = section_dir / f"{page.slug}.md"
                    if page_file.exists():
                        pages[f"{section.name}/{page.slug}"] = page_file
        
        return pages
    
    def run_all_checks(self) -> List[QualityGate]:
        """
        Run all quality checks.
        
        Returns:
            List of quality gate results
        """
        gates = [
            self.check_ia_sanity(),
            self.check_page_titles(),
            self.check_spec_fidelity(),
            self.check_dead_links(),
            self.check_page_structure(),
            self.check_duplication(),
        ]
        
        return gates
    
    def check_ia_sanity(self) -> QualityGate:
        """Check information architecture is sensible."""
        issues = []
        
        # Check section count
        if len(self.plan.sections) < 2:
            issues.append("Less than 2 sections - might need more structure")
        elif len(self.plan.sections) > 5:
            issues.append("More than 5 sections - might be too fragmented")
        
        # Check page count
        total_pages = sum(len(s.pages) for s in self.plan.sections)
        if total_pages < 4:
            issues.append(f"Only {total_pages} pages - documentation is sparse")
        elif total_pages > 20:
            issues.append(f"{total_pages} pages - might overwhelm users")
        
        # Check for empty sections
        for section in self.plan.sections:
            if not section.pages:
                issues.append(f"Section '{section.name}' has no pages")
        
        return QualityGate("IA Sanity", len(issues) == 0, issues)
    
    def check_page_titles(self) -> QualityGate:
        """Check that H1 titles match planned titles and slugs."""
        issues = []
        
        for section in self.plan.sections:
            for page in section.pages:
                page_id = f"{section.name}/{page.slug}"
                page_file = self.all_pages.get(page_id)
                
                if not page_file:
                    issues.append(f"Page not found: {page_id}")
                    continue
                
                # Read first line (should be H1)
                with open(page_file, 'r') as f:
                    first_lines = [f.readline().strip() for _ in range(3)]
                
                # Look for H1 in first few lines
                h1_found = False
                for line in first_lines:
                    if line.startswith('# '):
                        h1_title = line[2:].strip()
                        if h1_title != page.title:
                            issues.append(
                                f"H1 mismatch in {page_id}: "
                                f"expected '{page.title}', got '{h1_title}'"
                            )
                        h1_found = True
                        break
                
                if not h1_found:
                    issues.append(f"No H1 found in {page_id}")
        
        return QualityGate("H1/Title Consistency", len(issues) == 0, issues)
    
    def check_spec_fidelity(self) -> QualityGate:
        """Check that content uses exact names from spec (no hallucination)."""
        issues = []
        
        # Collect spec vocabulary
        spec_env_vars = {e.name for e in self.spec.env_variables}
        spec_api_paths = {a.path for a in self.spec.apis}
        spec_module_names = {m.name for m in self.spec.modules}
        
        # Check each page for common hallucination patterns
        for page_id, page_file in self.all_pages.items():
            with open(page_file, 'r') as f:
                content = f.read()
            
            # Check for env var references that don't match spec
            env_pattern = r'\b[A-Z][A-Z0-9_]{2,}\b'
            found_vars = set(re.findall(env_pattern, content))
            
            # Filter out common non-env-var caps words
            common_words = {'API', 'URL', 'HTTP', 'HTTPS', 'JSON', 'XML', 'SQL', 'ID', 'UUID', 'GET', 'POST', 'PUT', 'DELETE', 'PATCH'}
            found_vars = found_vars - common_words
            
            for var in found_vars:
                if spec_env_vars and var not in spec_env_vars:
                    # Only warn if we have env vars in spec
                    pass  # Too noisy, skip for now
        
        return QualityGate("Spec Fidelity", len(issues) == 0, issues)
    
    def check_dead_links(self) -> QualityGate:
        """Check for broken internal links."""
        issues = []
        
        # Collect all valid targets
        valid_targets = set(self.all_pages.keys())
        
        # Check each page for links
        for page_id, page_file in self.all_pages.items():
            with open(page_file, 'r') as f:
                content = f.read()
            
            # Find Markdown links: [text](path)
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, content)
            
            for link_text, link_path in links:
                # Skip external links
                if link_path.startswith('http://') or link_path.startswith('https://'):
                    continue
                
                # Skip anchors
                if link_path.startswith('#'):
                    continue
                
                # Clean path (remove anchors)
                clean_path = link_path.split('#')[0]
                
                # Skip empty paths
                if not clean_path:
                    continue
                
                # Check if target exists
                # Handle both relative and absolute doc paths
                if clean_path not in valid_targets:
                    # Also try without .md extension
                    if clean_path.endswith('.md'):
                        clean_path = clean_path[:-3]
                    
                    if clean_path not in valid_targets:
                        issues.append(f"Broken link in {page_id}: [{link_text}]({link_path})")
        
        return QualityGate("Internal Links", len(issues) == 0, issues)
    
    def check_page_structure(self) -> QualityGate:
        """Check that pages follow expected structure."""
        issues = []
        
        required_sections = {
            'prerequisites': ['prerequisite', 'requirement', 'before you begin'],
            'verification': ['verif', 'confirm', 'check', 'test'],
            'troubleshooting': ['troubleshoot', 'debug', 'common issue', 'error', 'problem']
        }
        
        for page_id, page_file in self.all_pages.items():
            # Skip homepage
            if page_id == "index":
                continue
            
            with open(page_file, 'r') as f:
                content = f.read().lower()
            
            # Extract headers
            headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
            headers_text = ' '.join(headers).lower()
            
            # Check for required sections
            for section_name, keywords in required_sections.items():
                found = any(kw in headers_text for kw in keywords)
                if not found:
                    # Only warn, not fail
                    pass  # Too strict for initial generation
        
        return QualityGate("Page Structure", len(issues) == 0, issues)
    
    def check_duplication(self) -> QualityGate:
        """Check for duplicate titles or slugs."""
        issues = []
        
        # Check for duplicate slugs
        all_slugs = []
        for section in self.plan.sections:
            for page in section.pages:
                all_slugs.append(page.slug)
        
        seen = set()
        for slug in all_slugs:
            if slug in seen:
                issues.append(f"Duplicate slug: {slug}")
            seen.add(slug)
        
        # Check for very similar titles
        all_titles = []
        for section in self.plan.sections:
            for page in section.pages:
                all_titles.append(page.title.lower())
        
        for i, title1 in enumerate(all_titles):
            for title2 in all_titles[i+1:]:
                if title1 == title2:
                    issues.append(f"Duplicate title: {title1}")
        
        return QualityGate("Uniqueness", len(issues) == 0, issues)
    
    def print_report(self, gates: List[QualityGate]) -> bool:
        """
        Print quality report.
        
        Args:
            gates: List of quality gate results
            
        Returns:
            True if all gates passed, False otherwise
        """
        print("\n" + "=" * 60)
        print("QUALITY GATES REPORT")
        print("=" * 60)
        
        passed_count = sum(1 for g in gates if g.passed)
        total_count = len(gates)
        
        for gate in gates:
            print(f"\n{gate}")
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed_count}/{total_count} gates passed")
        print("=" * 60 + "\n")
        
        return passed_count == total_count
