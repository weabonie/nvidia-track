"""
NVIDIA NIM Client for local Nemotron inference.
OpenAI-compatible REST endpoint wrapper.
"""

import requests
from typing import List, Dict, Any, Optional
import json


class NIMClient:
    """Client for interacting with local NVIDIA NIM endpoint."""
    
    def __init__(self, base_url: str = "http://localhost:8000/v1"):
        """
        Initialize NIM client.
        
        Args:
            base_url: Base URL for the NIM endpoint (default: http://localhost:8000/v1)
        """
        self.base_url = base_url.rstrip('/')
        self.models_endpoint = f"{self.base_url}/models"
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        
    def list_models(self) -> List[str]:
        """
        List available models from the NIM endpoint.
        
        Returns:
            List of model names/IDs
            
        Raises:
            RuntimeError: If the endpoint is unreachable or returns an error
        """
        try:
            response = requests.get(self.models_endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract model IDs from OpenAI-compatible response
            if "data" in data:
                return [model.get("id") for model in data["data"]]
            return []
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to list models from {self.models_endpoint}: {e}")
    
    def get_nemotron_model(self) -> str:
        """
        Get the first available Nemotron instruct model.
        
        Returns:
            Model name/ID
            
        Raises:
            RuntimeError: If no Nemotron model is found
        """
        models = self.list_models()
        
        # Look for Nemotron instruct models
        for model in models:
            if "nemotron" in model.lower() and "instruct" in model.lower():
                return model
        
        # Fallback to first model if no specific Nemotron found
        if models:
            return models[0]
            
        raise RuntimeError("No models available from NIM endpoint")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> str:
        """
        Generate a chat completion using the NIM endpoint.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (if None, auto-detects Nemotron model)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response (not implemented)
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If the API call fails
        """
        if model is None:
            model = self.get_nemotron_model()
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract content from OpenAI-compatible response
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            
            raise RuntimeError(f"Unexpected response format: {data}")
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Chat completion failed: {e}")
    
    def check_health(self) -> bool:
        """
        Check if the NIM endpoint is reachable and has models.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            models = self.list_models()
            return len(models) > 0
        except Exception:
            return False


def create_system_message(content: str) -> Dict[str, str]:
    """Helper to create a system message."""
    return {"role": "system", "content": content}


def create_user_message(content: str) -> Dict[str, str]:
    """Helper to create a user message."""
    return {"role": "user", "content": content}


def create_assistant_message(content: str) -> Dict[str, str]:
    """Helper to create an assistant message."""
    return {"role": "assistant", "content": content}
