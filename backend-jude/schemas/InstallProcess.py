from pydantic import BaseModel, Field

class InstallProcess(BaseModel):
    """A Pydantic model for the installation process."""
    install_process: str = Field(description="A paragraph on the process of installing the project, mentioning toolchains like NPM or pip if applicable.")
