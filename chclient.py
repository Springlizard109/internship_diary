import chromadb

cl = chromadb.PersistentClient()

collection = cl.get_or_create_collection(name="test")


print("chromadb client created successfully")ollhey