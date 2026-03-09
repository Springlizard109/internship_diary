import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_store import get_vector_store

documents = []

data_folder = "data"

for file in os.listdir(data_folder):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(data_folder, file))
        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

db = get_vector_store()
db.add_documents(docs)

print("Documents added!")