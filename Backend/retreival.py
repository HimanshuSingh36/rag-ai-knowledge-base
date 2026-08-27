import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)


# Connect to existing Qdrant collection
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="rag_documents",
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


# Test question
query = "What AI experience does Himanshu have?"


# Retrieve relevant chunks
results = vector_store.similarity_search(
    query,
    k=3,
)


print("\nRetrieved documents:\n")

for i, doc in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(doc.page_content)
    print("Done with retrieval")