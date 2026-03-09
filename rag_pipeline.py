from vector_store import get_vector_store

def retrieve_docs(query):

    db = get_vector_store()

    docs = db.similarity_search(query, k=3)

    return docs
