import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field, field_serializer
from langchain_core.documents import Document

class SerializedDoc(BaseModel):
    dependencies: List[str] = Field(description='List of dependencies needed to run the project. This should not include the project name itself. For instance, some examples include Node, Python, TypeScript or React. Look at the files itself based on the language to determine dependencies.')
    goal: str = Field(description='Why this project was made. The end goal of this software. For instance, a web browser might want to help users navigate the web easier.')
    pages: Dict[str, str] = Field(description='Names of each page mapped to what the summary of each page would be, each summary should be a paragraph. Subsections of the project to write about')
    repo_name: str = Field(description='Name of the project itself.')
