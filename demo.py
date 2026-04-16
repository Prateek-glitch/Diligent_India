#!/usr/bin/env python3
"""
Demo script to showcase Jarvis AI Assistant functionality.
Run this to test the system without launching the full Streamlit UI.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from llm_engine import LLMEngine
from vector_store import VectorStore
from knowledge import get_knowledge_base
from logger import get_logger
from utils import format_timestamp


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print(" " * 20 + "🤖 JARVIS AI ASSISTANT DEMO")
    print("=" * 70)
    print("\nWelcome! This demo showcases the core functionality of Jarvis.")
    print("Note: Running in DEMO MODE (Ollama and full AI features may not be active)")
    print("=" * 70 + "\n")


def demo_llm_engine():
    """Demonstrate LLM engine capabilities."""
    print("\n📚 1. LLM ENGINE DEMO")
    print("-" * 70)
    
    llm = LLMEngine(model="llama2", temperature=0.7)
    
    queries = [
        "Hello, who are you?",
        "What can you help me with?",
        "Tell me about Python programming"
    ]
    
    for query in queries:
        print(f"\n❓ Query: {query}")
        result = llm.generate(query)
        print(f"🤖 Response: {result['response']}")
        print(f"⏱️  Time: {result['duration']:.3f}s")


def demo_knowledge_base():
    """Demonstrate knowledge base functionality."""
    print("\n\n📖 2. KNOWLEDGE BASE DEMO")
    print("-" * 70)
    
    kb = get_knowledge_base()
    
    print(f"\n✓ Total documents: {len(kb.get_all_documents())}")
    print(f"✓ Categories: {', '.join(kb.get_categories())}")
    
    print("\n🔍 Sample from 'general' category:")
    for i, doc in enumerate(kb.get_category("general")[:3], 1):
        print(f"   {i}. {doc}")
    
    print("\n🔍 Search for 'Python programming':")
    results = kb.search_knowledge("Python programming")
    for i, doc in enumerate(results[:3], 1):
        print(f"   {i}. {doc[:80]}...")


def demo_vector_store():
    """Demonstrate vector store capabilities."""
    print("\n\n🔢 3. VECTOR STORE DEMO")
    print("-" * 70)
    
    kb = get_knowledge_base()
    vs = VectorStore()
    
    # Add documents
    docs = kb.get_all_documents()
    vs.add_documents(docs)
    
    stats = vs.get_stats()
    print(f"\n✓ Documents indexed: {stats['num_documents']}")
    print(f"✓ Embedding model: {stats['embedding_model']}")
    print(f"✓ Embedding dimension: {stats['embedding_dimension']}")
    
    # Search
    query = "What is Jarvis and what can it do?"
    print(f"\n🔍 Searching for: '{query}'")
    results = vs.search(query, top_k=3)
    
    print("\n📊 Top 3 Results:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n   {i}. Score: {score:.3f}")
        print(f"      {doc[:100]}...")


def demo_integration():
    """Demonstrate integrated RAG (Retrieval-Augmented Generation)."""
    print("\n\n🎯 4. RAG INTEGRATION DEMO")
    print("-" * 70)
    
    # Initialize components
    llm = LLMEngine(model="llama2")
    kb = get_knowledge_base()
    vs = VectorStore()
    vs.add_documents(kb.get_all_documents())
    
    query = "What technologies does Jarvis use?"
    
    print(f"\n❓ User Query: {query}")
    
    # Step 1: Retrieve relevant context
    print("\n📚 Step 1: Retrieving relevant context from knowledge base...")
    context_docs = vs.search(query, top_k=2)
    context = "\n".join([doc for doc, _ in context_docs])
    print(f"✓ Found {len(context_docs)} relevant documents")
    
    # Step 2: Generate response with context
    print("\n🤖 Step 2: Generating response with context...")
    enhanced_prompt = f"Context:\n{context}\n\nQuestion: {query}"
    result = llm.generate(enhanced_prompt)
    
    print(f"\n💬 Final Response:\n{result['response']}")
    print(f"\n⏱️  Total time: {result['duration']:.3f}s")


def demo_conversation():
    """Demonstrate conversation with history."""
    print("\n\n💬 5. CONVERSATION DEMO")
    print("-" * 70)
    
    llm = LLMEngine(model="llama2")
    conversation = []
    
    exchanges = [
        "Hi, I'm learning about AI",
        "What is machine learning?",
        "How does it relate to Python?"
    ]
    
    for user_msg in exchanges:
        print(f"\n👤 You: {user_msg}")
        
        result = llm.generate(user_msg, context=conversation)
        assistant_msg = result['response']
        
        print(f"🤖 Jarvis: {assistant_msg}")
        
        # Add to conversation history
        conversation.append({"role": "user", "content": user_msg})
        conversation.append({"role": "assistant", "content": assistant_msg})


def demo_statistics():
    """Show system statistics."""
    print("\n\n📊 6. SYSTEM STATISTICS")
    print("-" * 70)
    
    llm = LLMEngine()
    kb = get_knowledge_base()
    vs = VectorStore()
    vs.add_documents(kb.get_all_documents())
    
    stats = vs.get_stats()
    
    print(f"\n🔧 LLM Configuration:")
    print(f"   • Model: {llm.model}")
    print(f"   • Temperature: {llm.temperature}")
    print(f"   • Max Tokens: {llm.max_tokens}")
    
    print(f"\n📚 Knowledge Base:")
    print(f"   • Total Documents: {len(kb.get_all_documents())}")
    print(f"   • Categories: {len(kb.get_categories())}")
    
    print(f"\n🔢 Vector Store:")
    print(f"   • Indexed Documents: {stats['num_documents']}")
    print(f"   • Embedding Dimension: {stats['embedding_dimension']}")
    print(f"   • Index Type: {stats['index_type']}")


def main():
    """Run all demos."""
    print_banner()
    
    try:
        demo_llm_engine()
        demo_knowledge_base()
        demo_vector_store()
        demo_integration()
        demo_conversation()
        demo_statistics()
        
        print("\n" + "=" * 70)
        print(" " * 25 + "✅ DEMO COMPLETED!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Install Ollama to enable full AI capabilities")
        print("2. Run 'streamlit run app.py' to launch the web UI")
        print("3. Customize the knowledge base in data/input_files/")
        print("4. Check README.md for detailed documentation")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
