from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()

# -----------------------------------
# Config
# -----------------------------------

DB_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------------
# Embeddings
# -----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# -----------------------------------
# Chroma Database
# -----------------------------------

vectordb = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

print("DB Path:", os.path.abspath(DB_DIR))
print("Document Count:", vectordb._collection.count())

# -----------------------------------
# LLM
# -----------------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# -----------------------------------
# Local Search
# -----------------------------------


 


def search_lore(query):

    try:

        results = vectordb.similarity_search_with_score(
            query,
            k=1
        )

        if not results:
            return None

        doc, score = results[0]

        content = doc.page_content

        print(f"\nBest Match Score: {score}")

        print("\nRetrieved Context:")
        print(content[:300])

        # Similarity threshold

        if score > 1.2:

            print(
                "No strong local match found."
            )

            return None

        # Extract important query words

        stop_words = {
            "who", "what", "where",
            "when", "tell", "about",
            "is", "the", "a", "an"
        }

        query_words = [
            word.lower()
            for word in query.split()
            if word.lower() not in stop_words
        ]

        content_lower = content.lower()

        # Verify at least one keyword exists
        if not any(
            word in content_lower
            for word in query_words
        ):

            print(
                "Keyword not found in local document."
            )

            return None

        return content

    except Exception as e:

        print(
            "Retrieval Error:",
            str(e)
        )

        return None


# -----------------------------------
# Main Ask Function
# -----------------------------------

def ask(question):

    context = search_lore(question)

    if context:

        source = "📚 Local Knowledge Base"

    else:

        print("\nUsing Web Search...")

        try:

            search = DuckDuckGoSearchRun()

            context = search.run(question)

            source = "🌐 Web Search"

            if (
                not context
                or len(context.strip()) < 20
            ):

                context = (
                    f"Question: {question}"
                )

        except Exception as e:

            print(
                "Web Search Error:",
                str(e)
            )

            context = (
                f"Question: {question}"
            )

            source = "🌐 Web Search"

    prompt = f"""
You are GameLore Agent.

Rules:
1. Use the provided context.
2. Be accurate and concise.
3. Do not invent facts.
4. If information is limited, clearly say so.

Context:

{context}

Question:

{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content

    if not answer:

        answer = (
            "I couldn't generate a response."
        )

    return {
        "answer": answer,
        "source": source
    }

# -----------------------------------
# Flask Wrapper
# -----------------------------------

class GameLoreAgent:

    def invoke(self, data):

        question = data["messages"][0]["content"]

        result = ask(question)

        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": result["answer"]
                }
            ],
            "source": result["source"]
        }

agent = GameLoreAgent()

# -----------------------------------
# Agent Instance
# -----------------------------------

agent = GameLoreAgent()

# -----------------------------------
# Module-level invoke
# -----------------------------------

def invoke(data):
    return agent.invoke(data)

# -----------------------------------
# Local Testing
# -----------------------------------

if __name__ == "__main__":

    while True:

        question = input("\nAsk: ")

        if question.lower() in [
            "quit",
            "exit"
        ]:
            break

        result = ask(question)

        print("\nSource:")
        print(result["source"])

        print("\nAnswer:")
        print(result["answer"])

