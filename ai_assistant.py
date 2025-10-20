"""
AI Assistant Core Module
=========================
Handles AI model interactions and response generation for different modes.

Supports multiple AI providers:
- OpenAI (GPT-3.5, GPT-4)
- Hugging Face (Various models)
- Ollama (Local models)

Author: Contributed for Hacktoberfest 2025
"""

import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from AI model"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, config):
        """Initialize OpenAI provider"""
        self.config = config
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": kwargs.get("system_prompt", "You are a helpful AI assistant.")},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", self.config.temperature),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

class HuggingFaceProvider(AIProvider):
    """Hugging Face API provider"""
    
    def __init__(self, config):
        """Initialize Hugging Face provider"""
        self.config = config
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
        
        try:
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(token=self.api_key)
        except ImportError:
            raise ImportError("huggingface_hub package not installed. Run: pip install huggingface_hub")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Hugging Face"""
        try:
            model = self.config.get_model()
            
            # Format prompt with system message if provided
            system_prompt = kwargs.get("system_prompt", "You are a helpful AI assistant.")
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            response = self.client.text_generation(
                full_prompt,
                model=model,
                max_new_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
            )
            return response.strip()
        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}")

class OllamaProvider(AIProvider):
    """Ollama local model provider"""
    
    def __init__(self, config):
        """Initialize Ollama provider"""
        self.config = config
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("requests package not installed. Run: pip install requests")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Ollama"""
        try:
            system_prompt = kwargs.get("system_prompt", "You are a helpful AI assistant.")
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.config.get_model(),
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", self.config.temperature),
                        "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
                    }
                }
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")

class AIAssistant:
    """Main AI Assistant class that handles different modes and providers"""
    
    # System prompts for different modes
    MODE_PROMPTS = {
        "chat": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and conversational responses.",
        
        "summarize": "You are an expert at summarizing text. Provide concise, accurate summaries that capture the key points and main ideas. Use bullet points when appropriate.",
        
        "translate": "You are a professional translator. Translate the given text accurately while preserving the original meaning, tone, and context. If the source/target language isn't specified, ask for clarification.",
        
        "ideas": "You are a creative idea generator. Provide innovative, practical, and diverse ideas. Think outside the box and explain why each idea could work.",
        
        "code": "You are an expert programmer proficient in multiple languages. Provide clean, well-commented code with explanations. Include best practices and potential improvements."
    }
    
    def __init__(self, config):
        """Initialize AI Assistant with configuration"""
        self.config = config
        self.provider = self._init_provider()
    
    def _init_provider(self) -> AIProvider:
        """Initialize the appropriate AI provider"""
        provider_map = {
            "openai": OpenAIProvider,
            "huggingface": HuggingFaceProvider,
            "ollama": OllamaProvider
        }
        
        provider_class = provider_map.get(self.config.provider)
        if not provider_class:
            raise ValueError(f"Unknown provider: {self.config.provider}")
        
        return provider_class(self.config)
    
    def generate_response(self, user_input: str, mode: str = "chat") -> str:
        """
        Generate AI response based on user input and mode
        
        Args:
            user_input: User's input text
            mode: AI mode (chat, summarize, translate, ideas, code)
        
        Returns:
            AI-generated response
        """
        # Get system prompt for the mode
        system_prompt = self.MODE_PROMPTS.get(mode, self.MODE_PROMPTS["chat"])
        
        # Add mode-specific formatting
        formatted_input = self._format_input(user_input, mode)
        
        # Generate response
        try:
            response = self.provider.generate(
                formatted_input,
                system_prompt=system_prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def _format_input(self, user_input: str, mode: str) -> str:
        """Format user input based on mode"""
        if mode == "summarize":
            return f"Please summarize the following text:\n\n{user_input}"
        
        elif mode == "translate":
            return f"Translate this text:\n\n{user_input}"
        
        elif mode == "ideas":
            return f"Generate creative ideas for:\n\n{user_input}"
        
        elif mode == "code":
            return f"Help me with this programming task:\n\n{user_input}"
        
        # Default chat mode
        return user_input
    
    def switch_provider(self, provider_name: str) -> None:
        """Switch to a different AI provider"""
        old_provider = self.config.provider
        self.config.provider = provider_name
        
        try:
            self.provider = self._init_provider()
        except Exception as e:
            # Revert on error
            self.config.provider = old_provider
            raise e

# Fallback provider for when no API keys are available
class MockProvider(AIProvider):
    """Mock provider for testing without API keys"""
    
    def __init__(self, config):
        self.config = config
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response"""
        mode = kwargs.get("mode", "chat")
        
        responses = {
            "chat": f"This is a mock response to: '{prompt[:50]}...'\n\nTo use real AI, please configure your API keys in the .env file.",
            "summarize": f"[Mock Summary] The text discusses: {prompt[:100]}...",
            "translate": f"[Mock Translation] Translated version of: {prompt[:100]}...",
            "ideas": f"[Mock Ideas]\n1. First idea related to: {prompt[:50]}\n2. Second creative approach\n3. Third innovative solution",
            "code": f"[Mock Code]\n# Code example for: {prompt[:50]}\ndef example():\n    pass  # Implementation here"
        }
        
        return responses.get(mode, responses["chat"])
