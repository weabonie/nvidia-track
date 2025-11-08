"""
Project specification schema and validation.
Defines the structure and validates input specs for documentation generation.
"""

from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Dict, Optional, Any
import json


class SetupRequirements(BaseModel):
    """Setup requirements specification."""
    os_constraints: List[str] = Field(default_factory=list, description="OS requirements (e.g., 'Linux', 'Windows 10+', 'macOS 12+')")
    tools: List[str] = Field(default_factory=list, description="Required tools and versions (e.g., 'Node.js 20+', 'Docker 24+')")
    hardware: List[str] = Field(default_factory=list, description="Hardware requirements (e.g., 'NVIDIA GPU with 8GB+ VRAM')")


class EnvVariable(BaseModel):
    """Environment variable specification."""
    name: str = Field(..., description="Variable name (e.g., 'API_KEY', 'DATABASE_URL')")
    purpose: str = Field(..., description="Short explanation of what this variable does")
    required: bool = Field(default=True, description="Whether this variable is required")
    default: Optional[str] = Field(default=None, description="Default value if any")


class APIEndpoint(BaseModel):
    """API endpoint specification."""
    name: str = Field(..., description="Endpoint name (e.g., 'Get User', 'Create Document')")
    path: str = Field(..., description="URL path (e.g., '/api/v1/users/{id}')")
    method: str = Field(..., description="HTTP method (GET, POST, PUT, DELETE, etc.)")
    purpose: str = Field(..., description="What this endpoint does")
    request_shape: Dict[str, Any] = Field(default_factory=dict, description="Request body/params structure")
    response_shape: Dict[str, Any] = Field(default_factory=dict, description="Response structure")
    auth_required: bool = Field(default=True, description="Whether authentication is required")


class Module(BaseModel):
    """Internal module/component specification."""
    name: str = Field(..., description="Module name (e.g., 'Authentication Service', 'Data Pipeline')")
    path: str = Field(..., description="Relative path in repo (e.g., 'src/auth/', 'services/pipeline/')")
    summary: str = Field(..., description="2-3 sentence explanation of what this module does")
    dependencies: List[str] = Field(default_factory=list, description="Other modules this depends on")


class DeploymentTarget(BaseModel):
    """Deployment target specification."""
    platform: str = Field(..., description="Platform name (e.g., 'Docker', 'Kubernetes', 'AWS Lambda')")
    description: str = Field(..., description="How deployment works on this platform")
    config_files: List[str] = Field(default_factory=list, description="Config files needed (e.g., 'Dockerfile', 'k8s/deployment.yaml')")


class FAQ(BaseModel):
    """FAQ entry specification."""
    question: str = Field(..., description="Common question or issue")
    answer: str = Field(..., description="Solution or explanation")
    category: Optional[str] = Field(default=None, description="Category (e.g., 'Installation', 'Configuration', 'Troubleshooting')")


class ProjectSpec(BaseModel):
    """
    Complete project specification for documentation generation.
    This is the single input that drives the entire doc generation process.
    """
    
    # Core metadata
    project_name: str = Field(..., description="Human-readable project name")
    description: str = Field(..., description="2-4 sentence explanation of what it is and who it's for")
    repo_url: Optional[str] = Field(default=None, description="Source repository URL")
    
    # Technology stack
    tech_stack: List[str] = Field(default_factory=list, description="Core technologies (e.g., 'Python 3.11', 'React 18', 'PostgreSQL 15')")
    
    # Setup and configuration
    setup: SetupRequirements = Field(default_factory=SetupRequirements, description="Requirements for running the project")
    env_variables: List[EnvVariable] = Field(default_factory=list, description="Environment variables the project uses")
    
    # APIs and modules
    apis: List[APIEndpoint] = Field(default_factory=list, description="API endpoints exposed by the project")
    modules: List[Module] = Field(default_factory=list, description="Internal components/modules")
    
    # Deployment
    deployment: List[DeploymentTarget] = Field(default_factory=list, description="Deployment targets and methods")
    
    # User support
    faq: List[FAQ] = Field(default_factory=list, description="Frequently asked questions and troubleshooting")
    
    # Optional extras
    extras: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional resources (e.g., {'architecture_diagram': 'url', 'design_doc': 'url', 'openapi_spec': 'path'})"
    )
    
    @field_validator('project_name')
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        """Ensure project name is non-empty and reasonable length."""
        if not v or len(v.strip()) == 0:
            raise ValueError("project_name cannot be empty")
        if len(v) > 100:
            raise ValueError("project_name is too long (max 100 characters)")
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is non-empty and reasonable length."""
        if not v or len(v.strip()) == 0:
            raise ValueError("description cannot be empty")
        if len(v) < 20:
            raise ValueError("description is too short (minimum 20 characters)")
        if len(v) > 1000:
            raise ValueError("description is too long (max 1000 characters)")
        return v.strip()
    
    def validate_spec(self) -> List[str]:
        """
        Run additional sanity checks beyond Pydantic validation.
        
        Returns:
            List of warning messages (empty if all checks pass)
        """
        warnings = []
        
        # Check for module name references in dependencies
        module_names = {m.name for m in self.modules}
        for module in self.modules:
            for dep in module.dependencies:
                if dep not in module_names:
                    warnings.append(f"Module '{module.name}' references unknown dependency '{dep}'")
        
        # Check for reasonable tech stack
        if not self.tech_stack:
            warnings.append("tech_stack is empty - consider adding core technologies")
        
        # Check for setup requirements
        if not self.setup.tools and not self.setup.os_constraints:
            warnings.append("No setup requirements specified - users won't know prerequisites")
        
        # Check for duplicate env variable names
        env_names = [e.name for e in self.env_variables]
        duplicates = {name for name in env_names if env_names.count(name) > 1}
        if duplicates:
            warnings.append(f"Duplicate environment variable names: {duplicates}")
        
        # Check for duplicate API paths
        api_paths = [(a.method, a.path) for a in self.apis]
        duplicate_apis = {path for path in api_paths if api_paths.count(path) > 1}
        if duplicate_apis:
            warnings.append(f"Duplicate API endpoints: {duplicate_apis}")
        
        # Check for empty sections
        if not self.modules and not self.apis:
            warnings.append("No modules or APIs defined - documentation will be minimal")
        
        return warnings
    
    @classmethod
    def from_json_file(cls, file_path: str) -> "ProjectSpec":
        """
        Load a project spec from a JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Validated ProjectSpec instance
            
        Raises:
            ValueError: If JSON is invalid or validation fails
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return cls.model_validate(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load spec from {file_path}: {e}")
    
    def to_json_file(self, file_path: str, indent: int = 2) -> None:
        """
        Save the spec to a JSON file.
        
        Args:
            file_path: Path to save JSON file
            indent: JSON indentation (default: 2)
        """
        with open(file_path, 'w') as f:
            json.dump(self.model_dump(), f, indent=indent)


# Example spec for testing
EXAMPLE_SPEC = {
    "project_name": "MyAPI Service",
    "description": "A REST API service for managing user data with authentication and real-time notifications. Built for developers who need a scalable backend for web and mobile applications.",
    "repo_url": "https://github.com/example/myapi",
    "tech_stack": ["Python 3.11", "FastAPI", "PostgreSQL 15", "Redis 7", "Docker"],
    "setup": {
        "os_constraints": ["Linux", "macOS", "Windows 10+"],
        "tools": ["Python 3.11+", "Docker 24+", "PostgreSQL 15+"],
        "hardware": ["2GB+ RAM", "10GB disk space"]
    },
    "env_variables": [
        {
            "name": "DATABASE_URL",
            "purpose": "PostgreSQL connection string",
            "required": True
        },
        {
            "name": "REDIS_URL",
            "purpose": "Redis connection string for caching",
            "required": True
        },
        {
            "name": "SECRET_KEY",
            "purpose": "JWT token signing key",
            "required": True
        }
    ],
    "apis": [
        {
            "name": "Get User",
            "path": "/api/v1/users/{id}",
            "method": "GET",
            "purpose": "Retrieve a user by ID",
            "request_shape": {},
            "response_shape": {"id": "string", "name": "string", "email": "string"},
            "auth_required": True
        },
        {
            "name": "Create User",
            "path": "/api/v1/users",
            "method": "POST",
            "purpose": "Create a new user account",
            "request_shape": {"name": "string", "email": "string", "password": "string"},
            "response_shape": {"id": "string", "name": "string", "email": "string"},
            "auth_required": False
        }
    ],
    "modules": [
        {
            "name": "Authentication Service",
            "path": "src/auth/",
            "summary": "Handles user authentication, JWT token generation, and session management. Supports OAuth2 and local authentication strategies.",
            "dependencies": []
        },
        {
            "name": "User Service",
            "path": "src/users/",
            "summary": "Manages user CRUD operations, profile updates, and user search. Integrates with the authentication service for access control.",
            "dependencies": ["Authentication Service"]
        }
    ],
    "deployment": [
        {
            "platform": "Docker",
            "description": "Single container deployment using Docker Compose",
            "config_files": ["Dockerfile", "docker-compose.yml"]
        }
    ],
    "faq": [
        {
            "question": "How do I reset my database?",
            "answer": "Run `docker-compose down -v` to remove volumes, then `docker-compose up -d` to recreate with fresh database.",
            "category": "Troubleshooting"
        }
    ],
    "extras": {
        "openapi_spec": "docs/openapi.yaml",
        "architecture_diagram": "https://example.com/arch.png"
    }
}
