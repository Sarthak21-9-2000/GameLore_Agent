import os
from langchain import embeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore[import]
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"

DB_DIR = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_documents():
    loader = DirectoryLoader(
        DATA_DIR,
        glob ="**/*.md",
        loader_cls = UnstructuredMarkdownLoader
    )
    return loader.load()

def main():
    
    print("Loading documents...")
    documents=load_documents()
    print(documents)
    print(f"Loaded {len(documents)} documents")
    
    splitter =RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    
    chunks = splitter.split_documents(documents)
    
    print(f"Creaated {len(chunks)} chunks")
    
    embeddings = HuggingFaceEmbeddings(
        model_name = EMBEDDING_MODEL
    )
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    vectordb.persist()
    
    print("Vector database created")

if __name__ == "__main__":
    main()