"""
Configuration Management Module
================================
Handles application configuration and settings.

Author: Contributed for Hacktoberfest 2025
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for AI Text Assistant"""
    
    # Default models for each provider
    DEFAULT_MODELS = {
        "openai": "gpt-3.5-turbo",
        "huggingface": "mistralai/Mistral-7B-Instruct-v0.2",
        "ollama": "llama2"
    }
    
    def __init__(self):
        """Initialize configuration with defaults and environment variables"""
        # AI Provider settings
        self.provider = os.getenv("AI_PROVIDER", "openai")
        self.model = os.getenv("AI_MODEL", None)
        
        # Generation parameters
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        
        # Ollama settings
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Chat history settings
        self.history_dir = os.getenv("HISTORY_DIR", "chat_history")
        self.auto_save_history = os.getenv("AUTO_SAVE_HISTORY", "true").lower() == "true"
        
        # Web UI settings
        self.web_port = int(os.getenv("WEB_PORT", "5000"))
        self.web_host = os.getenv("WEB_HOST", "127.0.0.1")
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def get_model(self) -> str:
        """Get the model name for current provider"""
        if self.model:
            return self.model
        return self.DEFAULT_MODELS.get(self.provider, "")
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate configuration
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check provider
        if self.provider not in ["openai", "huggingface", "ollama"]:
            return False, f"Invalid provider: {self.provider}"
        
        # Check API keys for respective providers
        if self.provider == "openai" and not self.openai_api_key:
            return False, "OPENAI_API_KEY not set"
        
        if self.provider == "huggingface" and not self.huggingface_api_key:
            return False, "HUGGINGFACE_API_KEY not set"
        
        # Check temperature range
        if not 0.0 <= self.temperature <= 2.0:
            return False, f"Temperature must be between 0.0 and 2.0, got {self.temperature}"
        
        # Check max tokens
        if self.max_tokens <= 0:
            return False, f"Max tokens must be positive, got {self.max_tokens}"
        
        return True, ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "provider": self.provider,
            "model": self.get_model(),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "history_dir": self.history_dir,
            "auto_save_history": self.auto_save_history,
            "web_port": self.web_port,
            "web_host": self.web_host,
            "debug_mode": self.debug_mode
        }
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary"""
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """String representation of configuration"""
        return f"Config(provider={self.provider}, model={self.get_model()}, temperature={self.temperature})"
