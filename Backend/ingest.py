import os
from io import BytesIO
import uuid

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not QDRANT_URL:
    raise ValueError("QDRANT_URL is missing")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is missing")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")


# --------------------------------------------------
# 2. Embedding model
# --------------------------------------------------

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
)


# --------------------------------------------------
# 3. Ingest uploaded PDF
# --------------------------------------------------


def ingest_pdf(pdf_bytes: bytes, filename: str):

    # Read PDF from memory
    document_id = str(uuid.uuid4())
    reader = PdfReader(BytesIO(pdf_bytes))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            documents.append(
                Document(
                    page_content=page_text,
                    metadata={
                        "source": filename,
                        "page": page_number,
                        "document_id": document_id,
                    },
                )
            )

    print(f"Loaded {len(documents)} pages")

    # --------------------------------------------------
    # 4. Split into chunks
    # --------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # --------------------------------------------------
    # 5. Store embeddings in Qdrant Cloud
    # --------------------------------------------------

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="rag_documents",
    )

    print(f"Successfully indexed {filename} " f"into Qdrant Cloud ✅")

    return {
        "document_id": document_id,
        "filename": filename,
        "pages": len(documents),
        "chunks": len(chunks),
    }
