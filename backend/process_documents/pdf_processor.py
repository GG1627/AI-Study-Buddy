import PyPDF2
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        # Clean up the text
        page_text = page_text.replace("\n", " ").replace("\t", " ")
        text += page_text + " "
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks for better retrieval"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def add_pdf_to_vector_store(pdf_text: str, filename: str):
    """Add PDF content to ChromaDB"""
    # embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # Switch to Google Gemini for production
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_GEMINI_API_KEY"),
        dimensions=1024
    )
    
    # Use the same vector store as your existing setup
    vector_store = Chroma(
        collection_name="documents_gemini",  # Same collection
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db"
    )
    
    # Chunk the text
    chunks = chunk_text(pdf_text)
    
    # Create documents
    documents = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={"source": filename, "chunk": i}
        )
        documents.append(doc)
        ids.append(f"{filename}_{i}")
    
    # Add to vector store
    vector_store.add_documents(documents=documents, ids=ids)
    
    return len(chunks)




