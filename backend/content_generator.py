"""
Content generation engine.
Uses Nemotron to generate documentation pages based on spec and plan.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import re

from nim_client import NIMClient, create_system_message, create_user_message
from spec_schema import ProjectSpec
from ia_planner import DocumentationPlan, PagePlan


class ContentGenerator:
    """Generates documentation content using LLM."""
    
    def __init__(self, nim_client: NIMClient):
        """
        Initialize content generator.
        
        Args:
            nim_client: NIM client for LLM inference
        """
        self.client = nim_client
    
    def generate_homepage(
        self,
        spec: ProjectSpec,
        plan: DocumentationPlan,
        output_path: Path
    ) -> None:
        """
        Generate the homepage (docs/index.md).
        
        Args:
            spec: Project specification
            plan: Documentation plan
            output_path: Path to save the homepage
        """
        print("Generating homepage...")
        
        # Build context
        context = self._build_homepage_context(spec, plan)
        
        # Create prompts
        system_prompt = self._create_homepage_system_prompt()
        user_prompt = self._create_homepage_user_prompt(spec, plan, context)
        
        # Generate content
        messages = [
            create_system_message(system_prompt),
            create_user_message(user_prompt)
        ]
        
        content = self.client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Clean and save
        content = self._clean_markdown(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Homepage generated at {output_path}")
    
    def generate_page(
        self,
        page: PagePlan,
        spec: ProjectSpec,
        plan: DocumentationPlan,
        output_path: Path
    ) -> None:
        """
        Generate a single documentation page.
        
        Args:
            page: Page plan with title, slug, scope
            spec: Project specification
            plan: Full documentation plan (for cross-links)
            output_path: Path to save the page
        """
        print(f"Generating page: {page.title}...")
        
        # Build context
        context = self._build_page_context(page, spec, plan)
        
        # Create prompts
        system_prompt = self._create_page_system_prompt()
        user_prompt = self._create_page_user_prompt(page, spec, context)
        
        # Generate content
        messages = [
            create_system_message(system_prompt),
            create_user_message(user_prompt)
        ]
        
        content = self.client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=3000
        )
        
        # Clean and save
        content = self._clean_markdown(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Page generated at {output_path}")
    
    def generate_all_pages(
        self,
        spec: ProjectSpec,
        plan: DocumentationPlan,
        docs_dir: Path
    ) -> None:
        """
        Generate all pages according to the plan.
        
        Args:
            spec: Project specification
            plan: Documentation plan
            docs_dir: Base docs directory
        """
        # Generate homepage
        homepage_path = docs_dir / "index.md"
        self.generate_homepage(spec, plan, homepage_path)
        
        # Generate section pages
        total_pages = sum(len(section.pages) for section in plan.sections)
        current = 0
        
        for section in plan.sections:
            for page in section.pages:
                current += 1
                print(f"[{current}/{total_pages}] ", end="")
                
                page_path = docs_dir / section.name / f"{page.slug}.md"
                self.generate_page(page, spec, plan, page_path)
    
    def _build_homepage_context(self, spec: ProjectSpec, plan: DocumentationPlan) -> str:
        """Build context string for homepage generation."""
        parts = [
            f"Project: {spec.project_name}",
            f"Description: {spec.description}",
            f"\nTech Stack: {', '.join(spec.tech_stack)}",
        ]
        
        if spec.repo_url:
            parts.append(f"Repository: {spec.repo_url}")
        
        # Add quickstart bullets from plan
        if plan.homepage_bullets:
            parts.append(f"\nQuickstart Steps:\n" + "\n".join(f"- {b}" for b in plan.homepage_bullets))
        
        # Add key pages to link to
        key_pages = []
        for section in plan.sections[:2]:  # First 2 sections
            if section.pages:
                key_pages.append(f"{section.name}/{section.pages[0].slug}")
        
        if key_pages:
            parts.append(f"\nKey Pages: {', '.join(key_pages)}")
        
        return "\n".join(parts)
    
    def _build_page_context(self, page: PagePlan, spec: ProjectSpec, plan: DocumentationPlan) -> str:
        """Build context string for page generation."""
        parts = [
            f"Page Title: {page.title}",
            f"Section: {page.section}",
            f"\nScope:\n" + "\n".join(f"- {b}" for b in page.scope_bullets),
        ]
        
        # Add relevant spec data based on page scope
        page_lower = page.title.lower() + " " + " ".join(page.scope_bullets).lower()
        
        # If page mentions setup/installation
        if any(word in page_lower for word in ["setup", "install", "getting started", "quickstart"]):
            if spec.setup.tools:
                parts.append(f"\nRequired Tools: {', '.join(spec.setup.tools)}")
            if spec.setup.os_constraints:
                parts.append(f"OS Requirements: {', '.join(spec.setup.os_constraints)}")
        
        # If page mentions configuration/environment
        if any(word in page_lower for word in ["config", "environment", "variable"]):
            if spec.env_variables:
                env_list = "\n".join(f"- {e.name}: {e.purpose}" for e in spec.env_variables[:5])
                parts.append(f"\nEnvironment Variables:\n{env_list}")
        
        # If page mentions API
        if "api" in page_lower:
            if spec.apis:
                api_list = "\n".join(f"- {a.method} {a.path}: {a.purpose}" for a in spec.apis[:5])
                parts.append(f"\nAPI Endpoints:\n{api_list}")
        
        # If page mentions modules/architecture
        if any(word in page_lower for word in ["module", "component", "architecture", "structure"]):
            if spec.modules:
                module_list = "\n".join(f"- {m.name} ({m.path}): {m.summary}" for m in spec.modules[:5])
                parts.append(f"\nModules:\n{module_list}")
        
        # If page mentions deployment
        if any(word in page_lower for word in ["deploy", "docker", "container", "production"]):
            if spec.deployment:
                deploy_list = "\n".join(f"- {d.platform}: {d.description}" for d in spec.deployment)
                parts.append(f"\nDeployment Targets:\n{deploy_list}")
        
        # If page mentions troubleshooting
        if any(word in page_lower for word in ["troubleshoot", "debug", "error", "faq"]):
            if spec.faq:
                faq_list = "\n".join(f"- Q: {f.question}\n  A: {f.answer}" for f in spec.faq[:3])
                parts.append(f"\nCommon Issues:\n{faq_list}")
        
        return "\n".join(parts)
    
    def _create_homepage_system_prompt(self) -> str:
        """Create system prompt for homepage generation."""
        return """You are an expert technical writer creating documentation homepages.

Your homepage must include:
1. A single H1 title with the project name
2. A 1-paragraph pitch (what it is, who it's for, why it matters)
3. A "Quick Start" section with 3-5 numbered steps to get running
4. A "What's Next" section with links to 3-5 key documentation pages

Requirements:
- Tone: practical, welcoming, concise
- Format: valid Markdown
- Structure: H1 title, intro paragraph, H2 sections
- Links: use relative paths like `[Page Title](SectionName/page-slug)`
- Code blocks: use proper syntax highlighting
- NO explanations, just output the Markdown content

Output ONLY the Markdown content, nothing else."""
    
    def _create_homepage_user_prompt(self, spec: ProjectSpec, plan: DocumentationPlan, context: str) -> str:
        """Create user prompt for homepage generation."""
        # Build list of pages to link to
        link_suggestions = []
        for section in plan.sections:
            for page in section.pages[:2]:  # First 2 pages per section
                link_suggestions.append(f"- [{page.title}]({section.name}/{page.slug})")
        
        links_text = "\n".join(link_suggestions[:5])  # Top 5 pages
        
        return f"""Create a homepage (index.md) for this project:

{context}

Include links to these key pages:
{links_text}

The Quick Start should be actionable and follow this flow: install → configure → verify.
Output ONLY the Markdown content."""
    
    def _create_page_system_prompt(self) -> str:
        """Create system prompt for page generation."""
        return """You are an expert technical writer creating comprehensive documentation pages.

Every page must follow this structure:
1. H1 title (matching the planned title exactly)
2. Short intro paragraph: "When to use this" (2-3 sentences)
3. Prerequisites section (H2): list required tools, knowledge, or setup
4. Main content sections (H2): step-by-step procedures in chronological order
5. Configuration section (H2): variables, flags, files with clear explanations
6. Verification section (H2): how to confirm it worked
7. Troubleshooting section (H2): top 3 common issues and fixes

Requirements:
- Tone: practical, specific, copy-paste friendly
- Audience: developers who want working examples
- Format: valid Markdown
- Code: use proper syntax highlighting and realistic examples
- Paths/names: use EXACT names from the spec (no hallucination)
- Cross-links: link to related pages using relative paths
- Tables: use Markdown tables for config options
- Consistency: match terminology and naming from the spec

Output ONLY the Markdown content, nothing else."""
    
    def _create_page_user_prompt(self, page: PagePlan, spec: ProjectSpec, context: str) -> str:
        """Create user prompt for page generation."""
        return f"""Create a documentation page with this exact title: {page.title}

{context}

The page should cover exactly the scope bullets above. Use EXACT names from the context (env vars, APIs, modules, etc.).

Include realistic code examples. Link to related topics using relative paths.

Output ONLY the Markdown content."""
    
    def _clean_markdown(self, content: str) -> str:
        """
        Clean up generated Markdown content.
        
        Args:
            content: Raw Markdown from LLM
            
        Returns:
            Cleaned Markdown
        """
        # Remove any leading/trailing whitespace
        content = content.strip()
        
        # Remove markdown code fence wrappers if present
        if content.startswith("```markdown"):
            content = content[len("```markdown"):].lstrip()
        if content.startswith("```"):
            content = content[3:].lstrip()
        if content.endswith("```"):
            content = content[:-3].rstrip()
        
        # Ensure proper spacing around headers
        content = re.sub(r'\n(#{1,6})\s', r'\n\n\1 ', content)
        
        # Ensure consistent line endings
        content = content.replace('\r\n', '\n')
        
        # Add trailing newline
        if not content.endswith('\n'):
            content += '\n'
        
        return content
