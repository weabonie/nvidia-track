import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field, field_serializer
from langchain_core.documents import Document

class SerializedDoc(BaseModel):
    repo_name: str = Field(description='The repository slug/identifier (lowercase, kebab-case, no .git extension)', alias='repo-name')
    name: str = Field(description='Human-readable project name (title case, proper formatting)')
    description: str = Field(description='A concise one-sentence description of what the project does')
    goal: str = Field(description='The end goal or purpose of this software - what problem it solves or what value it provides')
    dependencies: List[str] = Field(description='List of key dependencies, frameworks, and technologies with versions where applicable (e.g., "Next.js 14", "FastAPI", "PostgreSQL")')
    installation: List[str] = Field(description='Step-by-step installation instructions as an array of clear, actionable steps')
    pages: Dict[str, str] = Field(description='Documentation sections mapped to their descriptions. Each section should have a clear purpose (e.g., "Introduction", "Quick Start", "API Reference", "Configuration", "Troubleshooting")')
    
    class Config:
        populate_by_name = True
