"""
Jarvis AI Assistant - Main Streamlit Application
A personal AI assistant with LLM and vector database integration.
"""
import os
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from llm_engine import LLMEngine
from vector_store import VectorStore
from knowledge import get_knowledge_base
from logger import get_logger
from utils import format_timestamp, truncate_text

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger("app", log_file=os.getenv("LOG_FILE", "data/output/app.log"))

# Page configuration
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_custom_css():
    """Load custom CSS styling."""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .sidebar-section {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    .stats-card {
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'llm_engine' not in st.session_state:
        model = os.getenv("OLLAMA_MODEL", "llama2")
        st.session_state.llm_engine = LLMEngine(model=model)
        logger.info("LLM Engine initialized")
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStore()
        # Load existing index or create new one with knowledge base
        try:
            st.session_state.vector_store.load()
        except:
            knowledge_base = get_knowledge_base()
            documents = knowledge_base.get_all_documents()
            st.session_state.vector_store.add_documents(documents)
            st.session_state.vector_store.save()
        logger.info("Vector Store initialized")
    
    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False


def render_sidebar():
    """Render the sidebar with navigation and options."""
    with st.sidebar:
        st.markdown('<div class="main-header">🤖 Jarvis</div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Menu")
        page = st.radio(
            "Navigation",
            ["AI Chat Helper", "Statistics", "Settings"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics
        if page == "Statistics":
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("### 📊 Statistics")
            
            stats = st.session_state.vector_store.get_stats()
            st.metric("Documents", stats['num_documents'])
            st.metric("Messages", len(st.session_state.messages))
            st.metric("Model", st.session_state.llm_engine.model)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Settings
        elif page == "Settings":
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Settings")
            
            # Temperature slider
            temp = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.llm_engine.temperature,
                step=0.1,
                help="Controls randomness in responses"
            )
            st.session_state.llm_engine.temperature = temp
            
            # Max tokens
            max_tokens = st.slider(
                "Max Response Length",
                min_value=128,
                max_value=2048,
                value=st.session_state.llm_engine.max_tokens,
                step=128
            )
            st.session_state.llm_engine.max_tokens = max_tokens
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Actions")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_started = False
            st.rerun()
        
        if st.button("💾 Save Vector Store"):
            st.session_state.vector_store.save()
            st.success("Vector store saved!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Jarvis AI Assistant**
        
        Your personal AI helper powered by:
        - 🧠 Self-hosted LLM (Ollama)
        - 🔍 Vector Database (FAISS)
        - 💬 Conversational Interface
        
        Ask me anything!
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        return page


def render_chat_message(message: dict, index: int):
    """
    Render a chat message.
    
    Args:
        message: Message dictionary with 'role' and 'content'
        index: Message index
    """
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', '')
    
    if role == 'user':
        css_class = 'user-message'
        icon = '👤'
        label = 'You'
    else:
        css_class = 'assistant-message'
        icon = '🤖'
        label = 'Jarvis'
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{icon} {label}</strong>
        {f'<span style="float: right; font-size: 0.8rem; color: #666;">{timestamp}</span>' if timestamp else ''}
        <br><br>
        {content}
    </div>
    """, unsafe_allow_html=True)


def get_relevant_context(query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant context from vector store.
    
    Args:
        query: User query
        top_k: Number of documents to retrieve
    
    Returns:
        Formatted context string
    """
    results = st.session_state.vector_store.search(query, top_k=top_k)
    
    if not results:
        return ""
    
    context_parts = ["Here is some relevant information from the knowledge base:\n"]
    for i, (doc, score) in enumerate(results, 1):
        context_parts.append(f"{i}. {doc}")
    
    return "\n".join(context_parts)


def generate_response(user_query: str) -> str:
    """
    Generate response using LLM and vector store.
    
    Args:
        user_query: User's query
    
    Returns:
        Generated response
    """
    # Get relevant context from vector store
    context = get_relevant_context(user_query)
    
    # Prepare system message
    system_message = (
        "You are Jarvis, a helpful AI assistant. "
        "Use the provided context from the knowledge base to answer questions accurately. "
        "If you don't know something, say so honestly. "
        "Be concise, friendly, and helpful."
    )
    
    # Add context to prompt if available
    if context:
        enhanced_query = f"{context}\n\nUser Question: {user_query}"
    else:
        enhanced_query = user_query
    
    # Generate response
    result = st.session_state.llm_engine.generate(
        prompt=enhanced_query,
        context=st.session_state.messages[-10:] if len(st.session_state.messages) > 0 else None,
        system_message=system_message
    )
    
    # Log interaction
    logger.log_user_interaction(
        query=user_query,
        response=result['response'],
        response_time=result['duration']
    )
    
    return result['response']


def main():
    """Main application function."""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get current page
    current_page = render_sidebar()
    
    # Main chat interface
    if current_page == "AI Chat Helper":
        st.markdown('<div class="main-header">💬 Chat with Jarvis</div>', unsafe_allow_html=True)
        
        # Welcome message
        if not st.session_state.chat_started and len(st.session_state.messages) == 0:
            st.markdown("""
            <div class="chat-message assistant-message">
                <strong>🤖 Jarvis</strong><br><br>
                Hello! I'm Jarvis, your AI assistant. I'm here to help you with:
                <ul>
                    <li>Answering questions on various topics</li>
                    <li>Programming and technical support</li>
                    <li>General knowledge and information</li>
                    <li>Recommendations and suggestions</li>
                </ul>
                How can I assist you today?
            </div>
            """, unsafe_allow_html=True)
            st.session_state.chat_started = True
        
        # Display chat history
        for idx, message in enumerate(st.session_state.messages):
            render_chat_message(message, idx)
        
        # Chat input
        st.markdown("---")
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Your message:",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)
        
        # Process user input
        if send_button and user_input:
            # Add user message
            timestamp = format_timestamp()
            st.session_state.messages.append({
                'role': 'user',
                'content': user_input,
                'timestamp': timestamp
            })
            
            # Generate and add assistant response
            with st.spinner("Jarvis is thinking..."):
                response = generate_response(user_input)
            
            st.session_state.messages.append({
                'role': 'assistant',
                'content': response,
                'timestamp': format_timestamp()
            })
            
            # Rerun to display new messages
            st.rerun()
    
    elif current_page == "Statistics":
        st.markdown('<div class="main-header">📊 Statistics Dashboard</div>', unsafe_allow_html=True)
        
        # Display detailed statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("Total Messages", len(st.session_state.messages))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            stats = st.session_state.vector_store.get_stats()
            st.metric("Knowledge Base Docs", stats['num_documents'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("Active Model", st.session_state.llm_engine.model)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Vector store info
        st.markdown("### 🔍 Vector Store Information")
        stats = st.session_state.vector_store.get_stats()
        st.json(stats)
        
        # LLM info
        st.markdown("### 🧠 LLM Configuration")
        st.write(f"**Model:** {st.session_state.llm_engine.model}")
        st.write(f"**Temperature:** {st.session_state.llm_engine.temperature}")
        st.write(f"**Max Tokens:** {st.session_state.llm_engine.max_tokens}")


if __name__ == "__main__":
    main()
