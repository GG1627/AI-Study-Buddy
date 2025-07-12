from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from vector import retriever
import json
import uvicorn
from process_documents.pdf_processor import extract_text_from_pdf, add_pdf_to_vector_store

app = FastAPI()

"""
Add CORS middleware so your Next.js frontend can talk to this API
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about documents.

Here are some relevant content: {content}

Here is the question to answer: {question}
"""
prompt = PromptTemplate.from_template(template)
chain = prompt | model

# Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# This is a test route to check if the API is running
@app.get("/")
async def root(): # ROOT ROUTE
    return {"message": "StudyForge API is running!"}

# Custom route to ask a question
@app.post("/ask-question")
async def ask_question(request: QuestionRequest):
    try:
        content = retriever.invoke(request.question)
        result = chain.invoke({
            "content": content,
            "question": request.question
        })
        return {"answer": result, "sources": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Custom route to upload a document
@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(file.file)
        
        # Add to vector store
        chunk_count = add_pdf_to_vector_store(pdf_text, file.filename)
        
        return {
            "message": f"File {file.filename} uploaded successfully",
            "chunks_created": chunk_count,
            "text_preview": pdf_text[:200] + "..." if len(pdf_text) > 200 else pdf_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)