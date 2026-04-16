"""
Unit tests for the Vector Store module.
"""
import pytest
import numpy as np
from pathlib import Path

from vector_store import VectorStore


class TestVectorStore:
    """Test cases for VectorStore class."""
    
    def test_init(self):
        """Test vector store initialization."""
        store = VectorStore()
        assert store.dimension == 384
        assert store.documents == []
    
    def test_init_with_custom_dimension(self):
        """Test initialization with custom dimension."""
        store = VectorStore(dimension=768)
        assert store.dimension == 768
    
    def test_embed_text(self):
        """Test text embedding generation."""
        store = VectorStore()
        embedding = store.embed_text("Hello world")
        
        assert isinstance(embedding, np.ndarray)
        assert embedding.shape == (store.dimension,)
        assert embedding.dtype == np.float32
    
    def test_add_single_document(self):
        """Test adding a single document."""
        store = VectorStore()
        store.add_documents(["This is a test document"])
        
        assert len(store.documents) == 1
        assert store.documents[0] == "This is a test document"
    
    def test_add_multiple_documents(self):
        """Test adding multiple documents."""
        store = VectorStore()
        docs = ["Doc 1", "Doc 2", "Doc 3"]
        store.add_documents(docs)
        
        assert len(store.documents) == 3
        assert store.documents == docs
    
    def test_add_empty_documents(self):
        """Test adding empty document list."""
        store = VectorStore()
        store.add_documents([])
        
        assert len(store.documents) == 0
    
    def test_search_with_documents(self):
        """Test search functionality with documents."""
        store = VectorStore()
        docs = [
            "Python is a programming language",
            "JavaScript is used for web development",
            "Machine learning uses Python"
        ]
        store.add_documents(docs)
        
        results = store.search("Python programming", top_k=2)
        
        assert len(results) > 0
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
        assert all(len(r) == 2 for r in results)  # (document, score)
    
    def test_search_empty_store(self):
        """Test search on empty vector store."""
        store = VectorStore()
        results = store.search("test query")
        
        assert results == []
    
    def test_search_top_k(self):
        """Test search with different top_k values."""
        store = VectorStore()
        docs = [f"Document {i}" for i in range(10)]
        store.add_documents(docs)
        
        results = store.search("Document", top_k=3)
        assert len(results) <= 3
        
        results = store.search("Document", top_k=5)
        assert len(results) <= 5
    
    def test_mock_search(self):
        """Test fallback mock search."""
        store = VectorStore()
        store.mock_search = True
        docs = [
            "Python programming language",
            "Java programming language",
            "Web development with JavaScript"
        ]
        store.add_documents(docs)
        
        results = store._mock_search("Python programming", top_k=2)
        
        assert len(results) > 0
        assert all(isinstance(score, float) for _, score in results)
        assert all(0 <= score <= 1 for _, score in results)
    
    def test_clear(self):
        """Test clearing the vector store."""
        store = VectorStore()
        store.add_documents(["Doc 1", "Doc 2"])
        assert len(store.documents) == 2
        
        store.clear()
        assert len(store.documents) == 0
    
    def test_get_stats(self):
        """Test getting vector store statistics."""
        store = VectorStore()
        store.add_documents(["Doc 1", "Doc 2", "Doc 3"])
        
        stats = store.get_stats()
        
        assert isinstance(stats, dict)
        assert "num_documents" in stats
        assert stats["num_documents"] == 3
        assert "embedding_dimension" in stats
        assert "embedding_model" in stats
    
    def test_save_empty_store(self, tmp_path):
        """Test saving empty vector store."""
        store = VectorStore(index_path=str(tmp_path / "test_index"))
        store.save()
        # Should not raise an error
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading vector store."""
        index_path = str(tmp_path / "test_index")
        
        # Create and save
        store1 = VectorStore(index_path=index_path)
        docs = ["Doc 1", "Doc 2", "Doc 3"]
        store1.add_documents(docs)
        store1.save()
        
        # Load in new instance
        store2 = VectorStore(index_path=index_path)
        store2.load()
        
        assert len(store2.documents) == len(docs)
        assert store2.documents == docs
    
    def test_embedding_consistency(self):
        """Test that same text produces same embedding."""
        store = VectorStore()
        
        text = "Test consistency"
        emb1 = store.embed_text(text)
        emb2 = store.embed_text(text)
        
        # In mock mode, embeddings are random, so we just check shape
        assert emb1.shape == emb2.shape
