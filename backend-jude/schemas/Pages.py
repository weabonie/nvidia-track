from pydantic import BaseModel, Field
from typing import Dict

class Pages(BaseModel):
    """Documentation pages/sections for the project."""
    pages: Dict[str, str] = Field(
        description="""A dictionary of documentation section names to their descriptions. 
        Include relevant sections like:
        - "Introduction": Overview of the project, features, and use cases
        - "Quick Start": How to get started quickly
        - "Installation": Detailed setup instructions
        - "Configuration": Environment variables, settings, etc.
        - "API Reference" or "Backend API": API documentation if applicable
        - "Frontend Guide" or "UI Guide": Frontend documentation if applicable
        - "Usage Examples": Example use cases and walkthroughs
        - "Troubleshooting": Common issues and solutions
        - "Architecture": System design and technical overview if it's a complex project
        Each description should be 1-2 sentences explaining what that section covers."""
    )
