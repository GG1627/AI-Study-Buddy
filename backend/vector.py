from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Load the data
df =pd.read_csv("./data/realistic_restaurant_reviews.csv")

# Load the embeddings model
# embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Switch to Google Gemini for production
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_GEMINI_API_KEY"),
    dimensions=1024
)

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"]},
            id = str(i)
        )

        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="documents_gemini",
    embedding_function=embeddings,
    persist_directory=db_location
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}

)







