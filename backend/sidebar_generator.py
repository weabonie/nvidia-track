"""
Sidebar generator for Docusaurus.
Creates sidebars.js based on documentation plan.
"""

from pathlib import Path
from typing import List, Dict, Any

from ia_planner import DocumentationPlan, SectionPlan


class SidebarGenerator:
    """Generates Docusaurus sidebar configuration."""
    
    def __init__(self, plan: DocumentationPlan):
        """
        Initialize sidebar generator.
        
        Args:
            plan: Documentation plan with sections and pages
        """
        self.plan = plan
    
    def generate_sidebar(self, output_path: Path) -> None:
        """
        Generate sidebars.js file.
        
        Args:
            output_path: Path to save sidebars.js
        """
        print("Generating sidebar configuration...")
        
        sidebar_config = self._build_sidebar_config()
        sidebar_js = self._format_sidebar_js(sidebar_config)
        
        with open(output_path, 'w') as f:
            f.write(sidebar_js)
        
        print(f"✓ Sidebar generated at {output_path}")
    
    def _build_sidebar_config(self) -> Dict[str, Any]:
        """
        Build sidebar configuration structure.
        
        Returns:
            Sidebar config dict
        """
        items = []
        
        # Add homepage at top
        items.append({
            "type": "doc",
            "id": "index",
            "label": "Home"
        })
        
        # Add sections as categories
        for section in self.plan.sections:
            if not section.pages:
                continue
            
            section_items = []
            for page in section.pages:
                section_items.append({
                    "type": "doc",
                    "id": f"{section.name}/{page.slug}",
                    "label": page.title
                })
            
            items.append({
                "type": "category",
                "label": section.name,
                "items": section_items,
                "collapsed": False
            })
        
        return {
            "tutorialSidebar": items
        }
    
    def _format_sidebar_js(self, config: Dict[str, Any]) -> str:
        """
        Format sidebar config as JavaScript.
        
        Args:
            config: Sidebar configuration dict
            
        Returns:
            JavaScript code for sidebars.js
        """
        # Convert to formatted JS
        js_lines = [
            "// @ts-check",
            "",
            "/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */",
            "const sidebars = {",
            "  tutorialSidebar: ["
        ]
        
        for item in config["tutorialSidebar"]:
            js_lines.append(self._format_item(item, indent=4))
        
        js_lines.extend([
            "  ],",
            "};",
            "",
            "module.exports = sidebars;",
            ""
        ])
        
        return "\n".join(js_lines)
    
    def _format_item(self, item: Dict[str, Any], indent: int = 0) -> str:
        """
        Format a single sidebar item as JavaScript.
        
        Args:
            item: Item dict
            indent: Indentation level (spaces)
            
        Returns:
            JavaScript code for the item
        """
        ind = " " * indent
        
        if item["type"] == "doc":
            return f'{ind}{{ type: "doc", id: "{item["id"]}", label: "{item["label"]}" }},'
        
        elif item["type"] == "category":
            lines = [
                f'{ind}{{',
                f'{ind}  type: "category",',
                f'{ind}  label: "{item["label"]}",',
                f'{ind}  collapsed: {str(item.get("collapsed", False)).lower()},',
                f'{ind}  items: ['
            ]
            
            for sub_item in item["items"]:
                lines.append(self._format_item(sub_item, indent + 4))
            
            lines.extend([
                f'{ind}  ]',
                f'{ind}}},'
            ])
            
            return "\n".join(lines)
        
        return ""
    
    def validate_sidebar(self, docs_dir: Path) -> List[str]:
        """
        Validate that all sidebar references point to existing files.
        
        Args:
            docs_dir: Base docs directory
            
        Returns:
            List of warnings/errors
        """
        warnings = []
        
        # Check homepage
        homepage = docs_dir / "index.md"
        if not homepage.exists():
            warnings.append(f"Homepage not found: {homepage}")
        
        # Check section pages
        for section in self.plan.sections:
            section_dir = docs_dir / section.name
            
            if not section_dir.exists():
                warnings.append(f"Section directory not found: {section_dir}")
                continue
            
            for page in section.pages:
                page_file = section_dir / f"{page.slug}.md"
                if not page_file.exists():
                    warnings.append(f"Page not found: {page_file}")
        
        return warnings
