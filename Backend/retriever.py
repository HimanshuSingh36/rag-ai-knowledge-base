import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)


vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name="rag_documents",
)


def search_documents(query: str, document_id: str = None) -> str:

    if document_id:
        results = vector_store.similarity_search(
            query,
            k=4,
            filter={
                "must": [
                    {"key": "metadata.document_id", "match": {"value": document_id}}
                ]
            },
        )
    else:
        results = vector_store.similarity_search(
            query,
            k=4,
        )

    if not results:
        return "No relevant documents were found."

    formatted_results = []

    for index, document in enumerate(results, start=1):

        formatted_results.append(f"""
            Document Result {index}

            Content:
            {document.page_content}

            Metadata:
            {document.metadata}
            """.strip())

    return "\n\n".join(formatted_results)
