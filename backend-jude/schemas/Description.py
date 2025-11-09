import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field, field_serializer
from langchain_core.documents import Document

class Description(BaseModel):
    description: str = Field(description='Description of the programming repo and what it aims to do')
