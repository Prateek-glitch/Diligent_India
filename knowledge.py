"""
Knowledge base for the Jarvis AI Assistant.
Stores enterprise knowledge and domain-specific information.
"""
from typing import Dict, List


class KnowledgeBase:
    """Enterprise knowledge storage for Jarvis."""
    
    def __init__(self):
        """Initialize the knowledge base with predefined knowledge."""
        self.knowledge: Dict[str, List[str]] = {
            "general": [
                "Jarvis is an AI assistant designed to help users with various tasks and queries.",
                "The assistant uses a self-hosted large language model for natural language understanding.",
                "Jarvis can retrieve information from a vector database for accurate and contextual responses.",
            ],
            "capabilities": [
                "Jarvis can answer questions about various topics including technology, science, and general knowledge.",
                "The assistant can help with coding questions, debugging, and explaining programming concepts.",
                "Jarvis supports conversation history and context-aware responses.",
                "The assistant can provide recommendations and suggestions based on user queries.",
            ],
            "technology": [
                "Jarvis is built using Python and Streamlit for the user interface.",
                "The backend uses Ollama for LLM inference with models like LLaMA.",
                "FAISS (Facebook AI Similarity Search) is used as the vector database for knowledge retrieval.",
                "Sentence transformers are used for generating embeddings from text.",
            ],
            "features": [
                "Interactive chatbot interface with message history.",
                "Clear chat functionality to start fresh conversations.",
                "Like/dislike buttons for user feedback (future enhancement).",
                "Regenerate response option for alternative answers.",
                "Sidebar navigation for different features and settings.",
            ],
            "ai_ml": [
                "Large Language Models (LLMs) are neural networks trained on vast amounts of text data.",
                "Vector databases store information as high-dimensional vectors for efficient similarity search.",
                "Embeddings are numerical representations of text that capture semantic meaning.",
                "RAG (Retrieval-Augmented Generation) combines retrieval and generation for better responses.",
            ],
            "programming": [
                "Python is a versatile programming language widely used in AI and web development.",
                "FastAPI and Flask are popular Python frameworks for building REST APIs.",
                "Streamlit is a Python library for creating interactive web applications quickly.",
                "Git is a version control system for tracking changes in source code.",
            ],
            "best_practices": [
                "Always validate user input before processing to ensure security.",
                "Implement proper error handling and logging for debugging.",
                "Use environment variables for sensitive configuration like API keys.",
                "Write unit tests to ensure code reliability and maintainability.",
                "Document your code with clear comments and README files.",
            ],
        }
    
    def get_all_documents(self) -> List[str]:
        """
        Get all knowledge documents as a flat list.
        
        Returns:
            List of all knowledge documents
        """
        documents = []
        for category, docs in self.knowledge.items():
            documents.extend(docs)
        return documents
    
    def get_category(self, category: str) -> List[str]:
        """
        Get documents from a specific category.
        
        Args:
            category: Knowledge category
        
        Returns:
            List of documents in the category
        """
        return self.knowledge.get(category, [])
    
    def get_categories(self) -> List[str]:
        """
        Get all available categories.
        
        Returns:
            List of category names
        """
        return list(self.knowledge.keys())
    
    def add_document(self, category: str, document: str):
        """
        Add a new document to the knowledge base.
        
        Args:
            category: Category for the document
            document: Document text
        """
        if category not in self.knowledge:
            self.knowledge[category] = []
        self.knowledge[category].append(document)
    
    def search_knowledge(self, query: str) -> List[str]:
        """
        Simple keyword-based search through knowledge base.
        
        Args:
            query: Search query
        
        Returns:
            List of relevant documents
        """
        query_lower = query.lower()
        results = []
        
        for category, documents in self.knowledge.items():
            for doc in documents:
                if any(word in doc.lower() for word in query_lower.split()):
                    results.append(doc)
        
        return results[:5]  # Return top 5 results


# Global knowledge base instance
_knowledge_base = None


def get_knowledge_base() -> KnowledgeBase:
    """
    Get the global knowledge base instance.
    
    Returns:
        KnowledgeBase instance
    """
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
