from pydantic import BaseModel, Field
from typing import List

class InstallProcess(BaseModel):
    """Installation instructions as a list of steps."""
    installation: List[str] = Field(
        description="""A list of clear, actionable installation steps. Each step should be concise and specific.
        Example steps might include:
        - "Clone the repository"
        - "Navigate to the project directory"
        - "Install Node.js dependencies with npm install"
        - "Set up environment variables in .env file"
        - "Run the development server with npm run dev"
        Keep steps simple and in logical order."""
    )
