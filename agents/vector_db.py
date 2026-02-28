import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_text():
    # Define paths
    kb_path = os.path.join("data")  # your text files folder
    persist_dir = os.path.join("data", "embeddings")

    # if exist
    os.makedirs(kb_path, exist_ok=True)
    os.makedirs(persist_dir, exist_ok=True)

    # Load all text files from folder
    loader = DirectoryLoader(kb_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("⚠️ No text files found in data folder!")
        return

    # Split long text into chunks for embedding
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Load embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create FAISS vector DB from documents
    vectordb = FAISS.from_documents(chunks, embeddings)

    # Save it locally
    vectordb.save_local(persist_dir)

    print("vector database created", persist_dir)
    return vectordb


