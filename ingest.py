import os
import shutil

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_huggingface import (
    HuggingFaceEmbeddings,
)

from langchain_chroma import Chroma


# -----------------------------------
# Config
# -----------------------------------

DATA_DIR = "data"
DB_DIR = "chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("RUNNING FILE:", os.path.abspath(__file__))
print("DB PATH:", os.path.abspath(DB_DIR))


# -----------------------------------
# Load Documents
# -----------------------------------

def load_documents():

    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
    )

    return loader.load()


# -----------------------------------
# Main
# -----------------------------------

def main():

    print("\nLoading documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents"
    )

    if len(documents) == 0:

        print(
            "\nNo markdown files found."
        )

        print(
            f"Check folder: {DATA_DIR}"
        )

        return

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    print(
        "\nLoading embeddings..."
    )

    embeddings = (
        HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    )

    if os.path.exists(DB_DIR):

        print(
            "\nRemoving old database..."
        )

        shutil.rmtree(DB_DIR)

    print(
        "\nCreating Chroma database..."
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
    )

    print(
        "\nDatabase created successfully!"
    )

    print(
        "Total Chunks Stored:",
        vectordb._collection.count()
    )


if __name__ == "__main__":
    main()
