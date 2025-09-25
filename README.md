# 🤖 AI Document Assistant

A modern, production-ready RAG (Retrieval-Augmented Generation) chatbot with a beautiful web interface that intelligently answers questions from your documents.

![AI Document Assistant](https://img.shields.io/badge/AI-Document%20Assistant-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red?style=for-the-badge&logo=fastapi)

## ✨ Features

- 🎨 **Modern UI/UX** - Beautiful, responsive web interface with animations
- 📁 **Multi-format Support** - PDF, DOCX, TXT file processing
- 🔄 **Flexible Upload** - Drag & drop, single file, or batch folder processing
- 🧠 **Smart Embeddings** - Configurable embedding models via environment variables
- 💾 **Vector Storage** - Efficient similarity search with cosine similarity
- 🔌 **Pluggable LLM** - Easy integration with different LLM providers (Qrok Cloud)
- 📊 **Real-time Stats** - Document and chunk counters
- 💬 **Interactive Chat** - Typing indicators, source attribution, message history
- 📱 **Mobile Responsive** - Works seamlessly on all devices

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone or download the project
cd rag_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env file with your settings:
# - Add your Qrok API key
# - Customize embedding model
# - Adjust chunk size and overlap
```

### 4. Add Documents (Optional)
```bash
# Create data directory if it doesn't exist
mkdir data

# Add your documents (.txt, .pdf, .docx files)
# Documents will be automatically processed when you click "Process ./data Folder"
```

### 5. Launch Application
```bash
# Start the server
python -m uvicorn backend.main:app --reload

# Open your browser and visit:
# http://localhost:8000
```

## 🎯 How to Use

1. **Upload Documents**: 
   - Use the sidebar to upload individual files
   - Or click "Process ./data Folder" to batch process documents

2. **Start Chatting**: 
   - Type your questions in the chat input
   - Get intelligent answers based on your documents
   - View source attributions for each response

3. **Manage Chat**: 
   - Clear chat history anytime
   - Monitor document and chunk statistics

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/ingest` | POST | Upload and process single file |
| `/ingest_folder` | POST | Process all files in ./data directory |
| `/chat` | POST | Send query and get AI response |

## ⚙️ Configuration Options

### Environment Variables (.env)

```env
# Embedding Model (HuggingFace model name)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Vector Database (currently using SimpleVectorStore ....you can switch to faiss_store or chroma_store)
VECTOR_DB=SIMPLE

# Data folder path
DATA_FOLDER=./data

# LLM Provider Settings
QROK_API_URL=https://api.qrok.cloud/v1
QROK_API_KEY=your_api_key_here

# Retrieval Settings
TOP_K=5                 # Number of relevant chunks to retrieve
CHUNK_SIZE=500         # Size of text chunks
CHUNK_OVERLAP=50       # Overlap between chunks
```

## 🏗️ Architecture

```
📁 rag_bot/
├── 📁 backend/
│   ├── main.py              # FastAPI application
│   ├── embeddings.py        # Embedding model interface
│   ├── simple_store.py      # Vector storage implementation
│   ├── llm_client.py        # LLM provider client
│   └── document_processor.py # Document parsing and chunking
├── 📁 frontend/
│   ├── index.html           # Modern web interface
│   └── app.js              # Interactive JavaScript
├── 📁 data/                # Document storage directory
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## 🔄 Extending the System

### Adding New Document Types
1. Extend `DocumentProcessor` class in `backend/document_processor.py`
2. Add new file extension handling
3. Implement text extraction logic

### Switching Embedding Models
1. Update `EMBEDDING_MODEL` in `.env`
2. Use any HuggingFace transformer model
3. System automatically adapts to new model dimensions

### Integrating Different LLMs
1. Modify `QrokLLMClient` in `backend/llm_client.py`
2. Update API endpoints and authentication
3. Adjust prompt formatting as needed

## 🐛 Troubleshooting

### Common Issues

**Import Errors**: Ensure virtual environment is activated and dependencies installed
```bash
pip install --upgrade -r requirements.txt
```

**Model Download Issues**: First run may take time to download embedding models
```bash
# Pre-download models (optional)
python -c "from transformers import AutoModel; AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')"
```

**File Upload Errors**: Check file permissions and supported formats (.txt, .pdf, .docx)


## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Made with ❤️ using FastAPI, Transformers, and modern web technologies**
