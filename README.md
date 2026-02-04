# 🤖 Build Your Own Jarvis - AI Assistant

A powerful personal AI assistant powered by self-hosted large language models (LLM), vector databases, and an intuitive chatbot interface. Jarvis helps you with various tasks, from answering questions to providing technical support.

## ✨ Features

- **🧠 Self-hosted LLM Integration**: Uses Ollama for running models like LLaMA, Mistral, or CodeLlama locally
- **🔍 Vector Database**: FAISS-powered similarity search for efficient knowledge retrieval
- **💬 Interactive Chat UI**: Beautiful Streamlit-based interface with real-time responses
- **📚 Knowledge Base**: Pre-loaded with enterprise knowledge and easily extensible
- **🎨 Modern UI Design**: Clean, responsive interface with sidebar navigation and statistics
- **📊 Analytics Dashboard**: Track usage statistics and monitor system performance
- **⚙️ Customizable Settings**: Adjust temperature, response length, and other parameters
- **💾 Session Management**: Persistent chat history and context-aware responses
- **🔒 Secure**: Environment-based configuration with no hardcoded credentials

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Streamlit  │ ──── │  LLM Engine  │ ──── │   Ollama    │
│     UI      │      │   (Python)   │      │  (LLaMA)    │
└─────────────┘      └──────────────┘      └─────────────┘
       │                     │
       │              ┌──────────────┐
       └────────────  │ Vector Store │
                      │   (FAISS)    │
                      └──────────────┘
                             │
                      ┌──────────────┐
                      │  Knowledge   │
                      │     Base     │
                      └──────────────┘
```

## 📁 Project Structure

```
project/
├── app.py                # Streamlit chatbot UI
├── llm_engine.py         # LLM integration (Ollama)
├── vector_store.py       # Vector database (FAISS)
├── knowledge.py          # Enterprise knowledge base
├── utils.py              # Utility functions
├── logger.py             # Logging and analytics
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
│
├── models/               # Model configurations
│   └── ollama_weights/
│       ├── config.json
│       └── README.md
│
├── static/               # UI assets
│   ├── styles.css
│   └── logo.png
│
├── data/
│   ├── input_files/      # Knowledge base files
│   │   ├── sample_knowledge.txt
│   │   └── README.md
│   └── output/           # Generated files (logs, indexes)
│       └── README.md
│
└── tests/                # Unit tests
    ├── conftest.py
    ├── test_llm_engine.py
    ├── test_vector_store.py
    ├── test_knowledge.py
    └── test_app.py
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running (optional for demo mode)
- 4GB+ RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prateek-glitch/Diligent_India.git
   cd Diligent_India
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Install and run Ollama (optional)**
   ```bash
   # Install Ollama from https://ollama.ai/
   # Pull a model
   ollama pull llama2
   ```

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start chatting with Jarvis!

## 🎯 Usage

### Basic Chat
1. Type your question in the input field
2. Press "Send" or hit Enter
3. Jarvis will respond using the LLM and knowledge base

### Navigation
- **AI Chat Helper**: Main chat interface
- **Statistics**: View usage metrics and system stats
- **Settings**: Adjust temperature, response length, etc.

### Actions
- **Clear Chat**: Start a fresh conversation
- **Save Vector Store**: Persist knowledge base changes

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_llm_engine.py -v
```

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vector Store
VECTOR_STORE_TYPE=faiss
FAISS_INDEX_PATH=data/output/faiss_index

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/output/app.log

# Application
APP_TITLE=Jarvis AI Assistant
MAX_HISTORY=10
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Customizing the Knowledge Base

Add your own knowledge by:
1. Creating text files in `data/input_files/`
2. Adding documents programmatically:
   ```python
   from knowledge import get_knowledge_base
   kb = get_knowledge_base()
   kb.add_document("category", "Your knowledge here")
   ```

## 🔧 Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python 3.8+
- **LLM**: Ollama (LLaMA, Mistral, CodeLlama)
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Sentence Transformers
- **Testing**: Pytest
- **Logging**: Python logging with colorlog

## 📊 Features in Detail

### LLM Engine
- Support for multiple Ollama models
- Configurable temperature and token limits
- Conversation context management
- Fallback mock mode for testing

### Vector Store
- FAISS-based similarity search
- Automatic embedding generation
- Save/load functionality
- Keyword fallback search

### Knowledge Base
- Pre-loaded with AI/ML knowledge
- Categorized information
- Easy to extend
- Search functionality

### UI Components
- Real-time chat interface
- Message history
- Sidebar navigation
- Statistics dashboard
- Settings panel

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for self-hosted LLM infrastructure
- [FAISS](https://github.com/facebookresearch/faiss) for vector similarity search
- [Streamlit](https://streamlit.io/) for the UI framework
- [Sentence Transformers](https://www.sbert.net/) for embeddings

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation in each module
- Review the test files for usage examples

## 🚧 Roadmap

- [ ] Add support for Pinecone vector database
- [ ] Implement user authentication
- [ ] Add voice input/output
- [ ] Create REST API backend
- [ ] Add response rating system
- [ ] Implement conversation export
- [ ] Add multi-language support
- [ ] Create mobile app

---

**Built with ❤️ for the AI community**