import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone

# -------------------
# CONFIG
# -------------------

PINECONE_API_KEY = "pcsk_4iwbir_MfYVPYP71BdqsBrBUXhYd1o8v6KQTpY2zM4bRKkFXYPHuwRuBDmfvWeXTMgSA6h"
INDEX_NAME = "rag-index"

# -------------------
# INIT EMBEDDINGS
# -------------------

embeddings = OllamaEmbeddings(model="nomic-embed-text")



pc = Pinecone(api_key="pcsk_4iwbir_MfYVPYP71BdqsBrBUXhYd1o8v6KQTpY2zM4bRKkFXYPHuwRuBDmfvWeXTMgSA6h")
index = pc.Index(INDEX_NAME)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)


text = """
Microservices architecture allows applications to be built as small,
independent services. It improves scalability, enables independent deployment,
and increases fault isolation.
"""

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

docs = splitter.create_documents([text])

# Add to Pinecone
vector_store.add_documents(docs)

print("Documents added successfully!")

# -------------------
# QUERY TIME
# -------------------

query = "What are the benefits of microservices?"

# Retrieve relevant docs
retrieved_docs = vector_store.similarity_search(query, k=2)

print("\nRetrieved Context:")
for doc in retrieved_docs:
    print("-", doc.page_content)

# -------------------
# LLM GENERATION
# -------------------

llm = Ollama(model="phi3:mini")

context = "\n".join([doc.page_content for doc in retrieved_docs])

final_prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

response = llm.invoke(final_prompt)

print("\nFinal Answer:")
print(response)