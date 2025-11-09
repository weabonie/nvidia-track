import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field, field_serializer
from langchain_core.documents import Document

class Dependencies(BaseModel):
    Dependencies: List[str] = Field(description='List of installable dependencies needed to run this project')
