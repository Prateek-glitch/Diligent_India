"""
Pytest configuration and fixtures.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        "Python is a programming language",
        "JavaScript is used for web development",
        "Machine learning uses Python and mathematics",
        "Artificial Intelligence is transforming industries",
        "Web development requires HTML, CSS, and JavaScript"
    ]


@pytest.fixture
def sample_messages():
    """Sample chat messages for testing."""
    return [
        {"role": "user", "content": "Hello", "timestamp": "2024-01-01 10:00:00"},
        {"role": "assistant", "content": "Hi! How can I help?", "timestamp": "2024-01-01 10:00:01"},
        {"role": "user", "content": "What is AI?", "timestamp": "2024-01-01 10:01:00"},
    ]


@pytest.fixture
def temp_index_path(tmp_path):
    """Temporary path for vector store index."""
    return str(tmp_path / "test_index")
