from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

# Where documents are stored
DOCS_DIR = Path(__file__).parent.parent / "docs"
# Where ChromaDB stores vectors
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

def load_documents():
    """Load all documents from the docs folder."""
    documents = []
    for file_path in DOCS_DIR.iterdir():
        print(f"Loading: {file_path.name}")
        if file_path.suffix == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
            documents.extend(loader.load())
        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())
    return documents

def create_vector_store():
    """Split documents into chunks and store as vectors in ChromaDB."""
    print("Loading documents...")
    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from documents")
    embeddings = FastEmbedEmbeddings()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )
    print("Vector store created successfully!")
    return vector_store

def load_vector_store():
    """Load existing vector store from disk."""
    embeddings = FastEmbedEmbeddings()
    vector_store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )
    return vector_store
def get_retriever():
    """Get a retriever that finds relevant document chunks."""
    if not CHROMA_DIR.exists():
        create_vector_store()
    vector_store = load_vector_store()
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

if __name__ == "__main__":
    print("Creating vector store from documents...")
    create_vector_store()
    print("Done! Vector store created.")