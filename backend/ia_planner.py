"""
Information Architecture (IA) planning agent.
Uses Nemotron to plan documentation structure based on project spec.
"""

from typing import List, Dict, Any
import json
from pydantic import BaseModel, Field

from nim_client import NIMClient, create_system_message, create_user_message
from spec_schema import ProjectSpec


class PagePlan(BaseModel):
    """Specification for a single documentation page."""
    title: str = Field(..., description="Page title (used as H1)")
    slug: str = Field(..., description="URL slug for the page (kebab-case)")
    section: str = Field(..., description="Section this page belongs to")
    scope_bullets: List[str] = Field(..., description="3-6 bullets describing what this page covers")
    
    @property
    def file_path(self) -> str:
        """Get the relative file path for this page."""
        return f"docs/{self.section}/{self.slug}.md"


class SectionPlan(BaseModel):
    """Specification for a documentation section."""
    name: str = Field(..., description="Section name (e.g., 'Guides', 'Reference')")
    description: str = Field(..., description="What this section contains")
    pages: List[PagePlan] = Field(default_factory=list, description="Pages in this section")


class DocumentationPlan(BaseModel):
    """Complete documentation information architecture plan."""
    project_name: str = Field(..., description="Project name from spec")
    sections: List[SectionPlan] = Field(..., description="2-4 documentation sections")
    homepage_bullets: List[str] = Field(..., description="Key bullets for homepage quickstart")
    
    def validate_plan(self) -> List[str]:
        """
        Validate the plan for common issues.
        
        Returns:
            List of warnings/errors
        """
        warnings = []
        
        # Check section count
        if len(self.sections) < 2:
            warnings.append("Only one section - consider adding more structure")
        if len(self.sections) > 5:
            warnings.append("More than 5 sections - might be too fragmented")
        
        # Check page count
        total_pages = sum(len(s.pages) for s in self.sections)
        if total_pages < 4:
            warnings.append(f"Only {total_pages} pages planned - documentation might be too sparse")
        if total_pages > 15:
            warnings.append(f"{total_pages} pages planned - might be overwhelming for users")
        
        # Check for slug uniqueness
        all_slugs = []
        for section in self.sections:
            for page in section.pages:
                all_slugs.append(page.slug)
        
        duplicates = {slug for slug in all_slugs if all_slugs.count(slug) > 1}
        if duplicates:
            warnings.append(f"Duplicate page slugs: {duplicates}")
        
        # Check for empty sections
        for section in self.sections:
            if len(section.pages) == 0:
                warnings.append(f"Section '{section.name}' has no pages")
        
        return warnings
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to dict for JSON serialization."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentationPlan":
        """Load from dict."""
        return cls.model_validate(data)
    
    def save(self, file_path: str) -> None:
        """Save plan to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, file_path: str) -> "DocumentationPlan":
        """Load plan from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class IAPlanner:
    """Agent that plans documentation information architecture."""
    
    def __init__(self, nim_client: NIMClient):
        """
        Initialize the IA planner.
        
        Args:
            nim_client: NIM client for LLM inference
        """
        self.client = nim_client
    
    def plan_documentation(self, spec: ProjectSpec) -> DocumentationPlan:
        """
        Generate a documentation plan based on the project spec.
        
        Args:
            spec: Validated project specification
            
        Returns:
            Complete documentation plan with sections and pages
        """
        # Build context from spec
        context = self._build_spec_context(spec)
        
        # Create prompt for planning
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(spec, context)
        
        # Get plan from LLM
        messages = [
            create_system_message(system_prompt),
            create_user_message(user_prompt)
        ]
        
        response = self.client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=3000
        )
        
        # Parse response into structured plan
        plan = self._parse_plan_response(response, spec.project_name)
        
        return plan
    
    def _build_spec_context(self, spec: ProjectSpec) -> str:
        """Build a concise context string from the spec."""
        parts = [
            f"Project: {spec.project_name}",
            f"Description: {spec.description}",
            f"\nTech Stack: {', '.join(spec.tech_stack)}",
        ]
        
        if spec.modules:
            parts.append(f"\nModules: {', '.join(m.name for m in spec.modules)}")
        
        if spec.apis:
            parts.append(f"\nAPI Endpoints: {len(spec.apis)} endpoints")
        
        if spec.env_variables:
            parts.append(f"\nEnvironment Variables: {', '.join(e.name for e in spec.env_variables)}")
        
        if spec.deployment:
            parts.append(f"\nDeployment Targets: {', '.join(d.platform for d in spec.deployment)}")
        
        if spec.faq:
            parts.append(f"\nFAQ Items: {len(spec.faq)} questions")
        
        return "\n".join(parts)
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for IA planning."""
        return """You are an expert technical documentation architect. Your job is to plan comprehensive, user-focused documentation.

Given a project specification, you will:
1. Identify 2-4 logical documentation sections (e.g., Guides, Concepts, Reference, How-To)
2. Plan 6-12 pages total, distributed across sections
3. For each page, define: title, URL slug, and 3-6 scope bullets

Requirements:
- Sections should follow a logical learning progression (getting started → concepts → reference → advanced)
- Page titles should be clear, action-oriented where possible
- Slugs should be kebab-case, concise, and SEO-friendly
- Scope bullets should be specific and complete (not vague)
- Balance breadth (covering all features) with depth (enough detail per page)
- Consider the target audience: developers who want practical, copy-paste guidance

Output ONLY valid JSON in this exact format:
{
  "sections": [
    {
      "name": "Section Name",
      "description": "What this section covers",
      "pages": [
        {
          "title": "Page Title",
          "slug": "page-slug",
          "scope_bullets": ["Bullet 1", "Bullet 2", "Bullet 3"]
        }
      ]
    }
  ],
  "homepage_bullets": ["Quick start step 1", "Quick start step 2", "Quick start step 3"]
}"""
    
    def _create_user_prompt(self, spec: ProjectSpec, context: str) -> str:
        """Create the user prompt with spec details."""
        return f"""Plan documentation for the following project:

{context}

Key considerations:
- Target audience: developers implementing or using this project
- Must cover: setup/installation, configuration, core concepts, API usage (if applicable), troubleshooting
- Should be practical and example-driven
- Balance getting started quickly vs. comprehensive reference

Plan 2-4 sections with 6-12 pages total. Return ONLY the JSON structure."""
    
    def _parse_plan_response(self, response: str, project_name: str) -> DocumentationPlan:
        """
        Parse LLM response into a DocumentationPlan.
        
        Args:
            response: Raw LLM response
            project_name: Project name from spec
            
        Returns:
            Validated DocumentationPlan
        """
        # Extract JSON from response (in case there's extra text)
        response = response.strip()
        
        # Find JSON block
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in LLM response")
        
        json_str = response[start_idx:end_idx]
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in LLM response: {e}\n{json_str}")
        
        # Build sections with pages
        sections = []
        for section_data in data.get("sections", []):
            pages = []
            section_name = section_data["name"]
            
            for page_data in section_data.get("pages", []):
                page = PagePlan(
                    title=page_data["title"],
                    slug=page_data["slug"],
                    section=section_name,
                    scope_bullets=page_data.get("scope_bullets", [])
                )
                pages.append(page)
            
            section = SectionPlan(
                name=section_name,
                description=section_data.get("description", ""),
                pages=pages
            )
            sections.append(section)
        
        plan = DocumentationPlan(
            project_name=project_name,
            sections=sections,
            homepage_bullets=data.get("homepage_bullets", [])
        )
        
        return plan
