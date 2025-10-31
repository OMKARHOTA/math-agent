import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def setup_qdrant_vectorstore():

    #here i want to create a Qdrant VectorDB with the help of hugggingface embeddings
    kb_path=os.path.join("Backend","data")
    os.makedirs(kb_path, exist_ok=True)

    #connect local Qdrant
    client=QdrantClient(host="localhost",port=6333)

    #Loading data with directory laoder
    loader = DirectoryLoader(kb_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    #split the text data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

     #embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb=QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="http://localhost:6333",
        collection_name="math_knowledge_base"
        )

    print(" Qdrant Vector Store setup completed!")
    return vectordb

if __name__ == "__main__":
    print("Testing Qdrant Vector Store setup")

    vectordb = setup_qdrant_vectorstore()

    # simple check
    print("VectorDB successfully created!")
    print("Collections available:", vectordb.client.get_collections())
