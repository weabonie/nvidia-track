from pydantic import BaseModel, Field

class ProjectName(BaseModel):
    """Extract a human-readable project name."""
    name: str = Field(description="A human-readable, properly formatted project name (use title case, spaces allowed)")
    description: str = Field(description="A concise one-sentence description of what this project does")
