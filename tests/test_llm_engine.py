"""
Unit tests for the LLM Engine module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from llm_engine import LLMEngine


class TestLLMEngine:
    """Test cases for LLMEngine class."""
    
    def test_init(self):
        """Test LLM engine initialization."""
        engine = LLMEngine(model="llama2")
        assert engine.model == "llama2"
        assert engine.temperature == 0.7
        assert engine.max_tokens == 512
    
    def test_init_with_custom_params(self):
        """Test LLM engine initialization with custom parameters."""
        engine = LLMEngine(
            model="mistral",
            temperature=0.5,
            max_tokens=1024
        )
        assert engine.model == "mistral"
        assert engine.temperature == 0.5
        assert engine.max_tokens == 1024
    
    def test_mock_generate_hello(self):
        """Test mock generation for hello query."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        result = engine.generate("Hello")
        assert "response" in result
        assert "Jarvis" in result["response"]
        assert result["model"] == "llama2"
    
    def test_mock_generate_help(self):
        """Test mock generation for help query."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        result = engine.generate("Can you help me?")
        assert "response" in result
        assert "help" in result["response"].lower()
    
    def test_mock_generate_who(self):
        """Test mock generation for identity query."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        result = engine.generate("What are you?")
        assert "response" in result
        assert "AI assistant" in result["response"]
    
    def test_generate_with_context(self):
        """Test generation with conversation context."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        context = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        result = engine.generate("How are you?", context=context)
        assert "response" in result
        assert result["model"] == "llama2"
    
    def test_generate_with_system_message(self):
        """Test generation with system message."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        result = engine.generate(
            "Tell me about AI",
            system_message="You are a helpful assistant."
        )
        assert "response" in result
    
    def test_generate_returns_duration(self):
        """Test that generate returns duration."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        result = engine.generate("Test query")
        assert "duration" in result
        assert isinstance(result["duration"], float)
        assert result["duration"] >= 0
    
    def test_is_available_mock_mode(self):
        """Test availability check in mock mode."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        assert engine.is_available() == True
    
    def test_list_available_models_mock(self):
        """Test listing available models in mock mode."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        models = engine.list_available_models()
        assert isinstance(models, list)
        assert len(models) > 0
        assert "llama2 (mock)" in models
    
    def test_generate_error_handling(self):
        """Test error handling during generation."""
        engine = LLMEngine(model="llama2")
        engine.mock_mode = True
        
        # Simulate error by patching _mock_generate
        with patch.object(engine, '_mock_generate', side_effect=Exception("Test error")):
            result = engine.generate("Test")
            assert "error" in result
            assert "Test error" in result["response"]
    
    def test_temperature_bounds(self):
        """Test temperature parameter bounds."""
        engine = LLMEngine(model="llama2", temperature=0.0)
        assert engine.temperature == 0.0
        
        engine = LLMEngine(model="llama2", temperature=1.0)
        assert engine.temperature == 1.0
    
    def test_max_tokens_value(self):
        """Test max tokens parameter."""
        engine = LLMEngine(model="llama2", max_tokens=256)
        assert engine.max_tokens == 256
