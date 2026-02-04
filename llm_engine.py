"""
LLM Engine for Jarvis AI Assistant using Ollama.
Handles interaction with self-hosted language models.
"""
import os
import time
from typing import Dict, List, Optional

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from logger import get_logger


class LLMEngine:
    """Engine for interacting with self-hosted LLM via Ollama."""
    
    def __init__(
        self,
        model: str = "llama2",
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512
    ):
        """
        Initialize the LLM engine.
        
        Args:
            model: Model name (e.g., 'llama2', 'mistral', 'codellama')
            base_url: Ollama base URL (defaults to http://localhost:11434)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
        """
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = get_logger("llm_engine")
        
        if not OLLAMA_AVAILABLE:
            self.logger.warning("Ollama library not installed. Using mock responses.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.client = ollama.Client(host=self.base_url)
        
        self.logger.info(f"LLM Engine initialized with model: {model}")
    
    def generate(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        system_message: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate response from the LLM.
        
        Args:
            prompt: User prompt/query
            context: Conversation history (list of messages)
            system_message: System message to guide model behavior
        
        Returns:
            Dictionary with 'response', 'model', and 'duration' keys
        """
        start_time = time.time()
        
        try:
            if self.mock_mode:
                response = self._mock_generate(prompt)
            else:
                response = self._ollama_generate(prompt, context, system_message)
            
            duration = time.time() - start_time
            
            self.logger.info(f"Generated response in {duration:.2f}s")
            
            return {
                "response": response,
                "model": self.model,
                "duration": duration
            }
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "model": self.model,
                "duration": time.time() - start_time,
                "error": str(e)
            }
    
    def _ollama_generate(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: User prompt
            context: Conversation history
            system_message: System message
        
        Returns:
            Generated response text
        """
        messages = []
        
        # Add system message
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add conversation history
        if context:
            messages.extend(context)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Generate response
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        )
        
        return response['message']['content']
    
    def _mock_generate(self, prompt: str) -> str:
        """
        Generate mock response when Ollama is not available.
        
        Args:
            prompt: User prompt
        
        Returns:
            Mock response
        """
        prompt_lower = prompt.lower()
        
        # Simple keyword-based responses
        if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
        
        elif any(word in prompt_lower for word in ["who", "what", "are you"]):
            return ("I'm Jarvis, an AI assistant powered by a self-hosted large language model. "
                   "I'm designed to help you with various tasks, answer questions, and provide information.")
        
        elif any(word in prompt_lower for word in ["help", "assist", "support"]):
            return ("I can help you with:\n"
                   "- Answering questions on various topics\n"
                   "- Programming and coding assistance\n"
                   "- General knowledge and information\n"
                   "- Recommendations and suggestions\n\n"
                   "Feel free to ask me anything!")
        
        elif any(word in prompt_lower for word in ["thank", "thanks"]):
            return "You're welcome! Let me know if you need anything else."
        
        else:
            return (f"I understand you're asking about: '{prompt[:50]}...'\n\n"
                   f"While I'm running in demo mode (Ollama not connected), I can still help! "
                   f"To get full AI-powered responses, please ensure Ollama is installed and running. "
                   f"In the meantime, I'll do my best to assist you based on the knowledge base.")
    
    def is_available(self) -> bool:
        """
        Check if the LLM engine is available.
        
        Returns:
            True if Ollama is running and model is available
        """
        if self.mock_mode:
            return True  # Mock mode is always available
        
        try:
            # Try to list models to check connection
            self.client.list()
            return True
        except Exception as e:
            self.logger.warning(f"Ollama not available: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """
        List available models in Ollama.
        
        Returns:
            List of model names
        """
        if self.mock_mode:
            return ["llama2 (mock)", "mistral (mock)", "codellama (mock)"]
        
        try:
            models = self.client.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
            return []
