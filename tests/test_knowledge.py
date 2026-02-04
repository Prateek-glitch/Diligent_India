"""
Unit tests for the Knowledge Base module.
"""
import pytest

from knowledge import KnowledgeBase, get_knowledge_base


class TestKnowledgeBase:
    """Test cases for KnowledgeBase class."""
    
    def test_init(self):
        """Test knowledge base initialization."""
        kb = KnowledgeBase()
        assert isinstance(kb.knowledge, dict)
        assert len(kb.knowledge) > 0
    
    def test_predefined_categories(self):
        """Test that predefined categories exist."""
        kb = KnowledgeBase()
        expected_categories = [
            "general", "capabilities", "technology",
            "features", "ai_ml", "programming", "best_practices"
        ]
        
        for category in expected_categories:
            assert category in kb.knowledge
    
    def test_get_all_documents(self):
        """Test retrieving all documents."""
        kb = KnowledgeBase()
        docs = kb.get_all_documents()
        
        assert isinstance(docs, list)
        assert len(docs) > 0
        assert all(isinstance(doc, str) for doc in docs)
    
    def test_get_category(self):
        """Test retrieving documents from a specific category."""
        kb = KnowledgeBase()
        general_docs = kb.get_category("general")
        
        assert isinstance(general_docs, list)
        assert len(general_docs) > 0
        assert "Jarvis" in general_docs[0]
    
    def test_get_nonexistent_category(self):
        """Test retrieving from a non-existent category."""
        kb = KnowledgeBase()
        docs = kb.get_category("nonexistent")
        
        assert docs == []
    
    def test_get_categories(self):
        """Test retrieving all category names."""
        kb = KnowledgeBase()
        categories = kb.get_categories()
        
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert "general" in categories
        assert "technology" in categories
    
    def test_add_document_existing_category(self):
        """Test adding a document to an existing category."""
        kb = KnowledgeBase()
        initial_count = len(kb.get_category("general"))
        
        kb.add_document("general", "New test document")
        
        assert len(kb.get_category("general")) == initial_count + 1
        assert "New test document" in kb.get_category("general")
    
    def test_add_document_new_category(self):
        """Test adding a document to a new category."""
        kb = KnowledgeBase()
        assert "test_category" not in kb.knowledge
        
        kb.add_document("test_category", "Test document")
        
        assert "test_category" in kb.knowledge
        assert len(kb.get_category("test_category")) == 1
        assert kb.get_category("test_category")[0] == "Test document"
    
    def test_search_knowledge_with_results(self):
        """Test searching knowledge base with matching results."""
        kb = KnowledgeBase()
        results = kb.search_knowledge("Python programming")
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(doc, str) for doc in results)
    
    def test_search_knowledge_case_insensitive(self):
        """Test that search is case-insensitive."""
        kb = KnowledgeBase()
        results1 = kb.search_knowledge("python")
        results2 = kb.search_knowledge("PYTHON")
        
        # Both should return results
        assert len(results1) > 0
        assert len(results2) > 0
    
    def test_search_knowledge_partial_match(self):
        """Test search with partial keyword match."""
        kb = KnowledgeBase()
        # Search for a word that appears in multiple documents
        results = kb.search_knowledge("assistant")
        
        assert len(results) > 0
    
    def test_search_knowledge_max_results(self):
        """Test that search returns at most 5 results."""
        kb = KnowledgeBase()
        # Add many documents with the same keyword
        for i in range(10):
            kb.add_document("test", f"Test document {i} with keyword test")
        
        results = kb.search_knowledge("test")
        assert len(results) <= 5
    
    def test_search_knowledge_no_results(self):
        """Test search with no matching results."""
        kb = KnowledgeBase()
        results = kb.search_knowledge("xyzabc123nonexistent")
        
        # May return empty or very low relevance results
        assert isinstance(results, list)
    
    def test_get_knowledge_base_singleton(self):
        """Test that get_knowledge_base returns the same instance."""
        kb1 = get_knowledge_base()
        kb2 = get_knowledge_base()
        
        assert kb1 is kb2
    
    def test_knowledge_base_content_quality(self):
        """Test that knowledge base contains quality content."""
        kb = KnowledgeBase()
        all_docs = kb.get_all_documents()
        
        # Check that documents are not empty
        assert all(len(doc) > 10 for doc in all_docs)
        
        # Check that some expected keywords exist
        all_text = " ".join(all_docs).lower()
        assert "jarvis" in all_text
        assert "ai" in all_text or "assistant" in all_text
    
    def test_technology_category_content(self):
        """Test technology category contains relevant information."""
        kb = KnowledgeBase()
        tech_docs = kb.get_category("technology")
        
        tech_text = " ".join(tech_docs).lower()
        assert "python" in tech_text or "streamlit" in tech_text
