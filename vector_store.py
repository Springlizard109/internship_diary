from langchain_chroma import Chroma
from embeddings import get_embeddings

def get_vector_store():
    embeddings = get_embeddings()

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return db