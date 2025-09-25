import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.embeddings import EmbeddingModel
from backend.simple_store import SimpleVectorStore
from backend.llm_client import QrokLLMClient
from backend.document_processor import DocumentProcessor

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Initialize components
embedding_model = EmbeddingModel()
vector_db = os.getenv("VECTOR_DB", "FAISS")
store = SimpleVectorStore()
store.load("./vector_store")

llm_client = QrokLLMClient()

class ChatRequest(BaseModel):
    query: str

@app.post("/ingest")
async def ingest_file(file: UploadFile):
    content = await file.read()
    with open(f"temp_{file.filename}", "wb") as f:
        f.write(content)
    
    text = DocumentProcessor.extract_text_from_file(f"temp_{file.filename}")
    chunks = DocumentProcessor.chunk_text(text, int(os.getenv("CHUNK_SIZE", 500)), int(os.getenv("CHUNK_OVERLAP", 50)))
    embeddings = embedding_model.embed_texts(chunks)
    metadata = [{"source": file.filename}] * len(chunks)
    
    store.add_texts(chunks, embeddings, metadata)
    store.save("./vector_store")
    
    os.remove(f"temp_{file.filename}")
    return {"message": f"Ingested {len(chunks)} chunks from {file.filename}"}

@app.post("/ingest_folder")
async def ingest_folder():
    data_folder = os.getenv("DATA_FOLDER", "./data")
    total_chunks = 0
    
    for filename in os.listdir(data_folder):
        if filename.endswith(('.txt', '.pdf', '.docx')):
            filepath = os.path.join(data_folder, filename)
            text = DocumentProcessor.extract_text_from_file(filepath)
            chunks = DocumentProcessor.chunk_text(text, int(os.getenv("CHUNK_SIZE", 500)), int(os.getenv("CHUNK_OVERLAP", 50)))
            embeddings = embedding_model.embed_texts(chunks)
            metadata = [{"source": filename}] * len(chunks)
            
            store.add_texts(chunks, embeddings, metadata)
            total_chunks += len(chunks)
    
    store.save("./vector_store")
    
    return {"message": f"Ingested {total_chunks} chunks from folder"}

@app.post("/chat")
async def chat(request: ChatRequest):
    query_embedding = embedding_model.embed_text(request.query)
    results = store.search(query_embedding, int(os.getenv("TOP_K", 5)))
    
    context = "\n".join([r["text"] for r in results])
    prompt = f"Context:\n{context}\n\nQuestion: {request.query}\nAnswer based only on the context:"
    
    answer = llm_client.generate_response(prompt)
    sources = [r["metadata"]["source"] for r in results]
    
    return {"answer": answer, "sources": list(set(sources))}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")