"""
Vector Store for Jarvis AI Assistant using FAISS.
Handles storage and retrieval of knowledge embeddings.
"""
import os
import pickle
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from logger import get_logger


class VectorStore:
    """Vector database using FAISS for similarity search."""
    
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_path: Optional[str] = None,
        dimension: int = 384
    ):
        """
        Initialize the vector store.
        
        Args:
            embedding_model: Name of the sentence transformer model
            index_path: Path to save/load FAISS index
            dimension: Embedding dimension (384 for all-MiniLM-L6-v2)
        """
        self.embedding_model_name = embedding_model
        self.index_path = index_path or os.getenv("FAISS_INDEX_PATH", "data/output/faiss_index")
        self.dimension = dimension
        self.logger = get_logger("vector_store")
        
        # Initialize components
        self._init_embedding_model()
        self._init_faiss_index()
        
        # Storage for documents
        self.documents: List[str] = []
        
        self.logger.info("Vector Store initialized")
    
    def _init_embedding_model(self):
        """Initialize the embedding model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            self.logger.warning("Sentence Transformers not installed. Using mock embeddings.")
            self.embedding_model = None
            self.mock_embeddings = True
        else:
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
                self.mock_embeddings = False
                self.logger.info(f"Loaded embedding model: {self.embedding_model_name}")
            except Exception as e:
                self.logger.warning(f"Failed to load embedding model: {e}. Using mock embeddings.")
                self.embedding_model = None
                self.mock_embeddings = True
    
    def _init_faiss_index(self):
        """Initialize FAISS index."""
        if not FAISS_AVAILABLE:
            self.logger.warning("FAISS not installed. Vector search will be limited.")
            self.index = None
            self.mock_search = True
        else:
            # Create a flat L2 index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.mock_search = False
            self.logger.info(f"Created FAISS index with dimension {self.dimension}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
        
        Returns:
            Embedding vector as numpy array
        """
        if self.mock_embeddings or self.embedding_model is None:
            # Return random embedding for testing
            return np.random.rand(self.dimension).astype('float32')
        
        try:
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            return embedding.astype('float32')
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return np.random.rand(self.dimension).astype('float32')
    
    def add_documents(self, documents: List[str]):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document strings
        """
        if not documents:
            return
        
        self.logger.info(f"Adding {len(documents)} documents to vector store")
        
        # Generate embeddings
        embeddings = []
        for doc in documents:
            embedding = self.embed_text(doc)
            embeddings.append(embedding)
        
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        if self.index is not None and not self.mock_search:
            self.index.add(embeddings_array)
        
        # Store documents
        self.documents.extend(documents)
        
        self.logger.info(f"Total documents in store: {len(self.documents)}")
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of tuples (document, similarity_score)
        """
        if not self.documents:
            self.logger.warning("No documents in vector store")
            return []
        
        # Generate query embedding
        query_embedding = self.embed_text(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        
        if self.mock_search or self.index is None:
            # Simple keyword-based fallback
            return self._mock_search(query, top_k)
        
        try:
            # Search in FAISS
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.documents)))
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.documents):
                    # Convert distance to similarity score (inverse)
                    similarity = 1.0 / (1.0 + float(dist))
                    results.append((self.documents[idx], similarity))
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error during search: {e}")
            return self._mock_search(query, top_k)
    
    def _mock_search(self, query: str, top_k: int) -> List[Tuple[str, float]]:
        """
        Fallback keyword-based search.
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            List of tuples (document, similarity_score)
        """
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            doc_words = set(doc.lower().split())
            # Simple Jaccard similarity
            intersection = query_words.intersection(doc_words)
            union = query_words.union(doc_words)
            score = len(intersection) / len(union) if union else 0.0
            scored_docs.append((doc, score))
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k]
    
    def save(self):
        """Save the vector store to disk."""
        if not self.documents:
            self.logger.warning("No documents to save")
            return
        
        try:
            save_path = Path(self.index_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            if self.index is not None and not self.mock_search:
                faiss.write_index(self.index, f"{self.index_path}.faiss")
            
            # Save documents
            with open(f"{self.index_path}.pkl", 'wb') as f:
                pickle.dump(self.documents, f)
            
            self.logger.info(f"Vector store saved to {self.index_path}")
        
        except Exception as e:
            self.logger.error(f"Error saving vector store: {e}")
    
    def load(self):
        """Load the vector store from disk."""
        try:
            # Load FAISS index
            if FAISS_AVAILABLE and Path(f"{self.index_path}.faiss").exists():
                self.index = faiss.read_index(f"{self.index_path}.faiss")
                self.mock_search = False
            
            # Load documents
            if Path(f"{self.index_path}.pkl").exists():
                with open(f"{self.index_path}.pkl", 'rb') as f:
                    self.documents = pickle.load(f)
            
            self.logger.info(f"Vector store loaded from {self.index_path}")
            self.logger.info(f"Loaded {len(self.documents)} documents")
        
        except Exception as e:
            self.logger.error(f"Error loading vector store: {e}")
    
    def clear(self):
        """Clear all documents from the vector store."""
        self.documents = []
        self._init_faiss_index()
        self.logger.info("Vector store cleared")
    
    def get_stats(self) -> dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with stats
        """
        return {
            "num_documents": len(self.documents),
            "embedding_dimension": self.dimension,
            "embedding_model": self.embedding_model_name,
            "index_type": "FAISS" if self.index is not None else "Mock",
            "mock_mode": self.mock_search or self.mock_embeddings
        }
