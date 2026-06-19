
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

DB_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------
# Embeddings
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# -----------------------------
# Chroma Vector Store
# -----------------------------

vectordb = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

# -----------------------------
# Groq LLM
# -----------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

# -----------------------------
# Local Search
# -----------------------------

def search_lore(query: str):

    try:

        results = vectordb.similarity_search_with_score(
            query,
            k=3
        )

        if not results:
            return None

        relevant_docs = []

        for doc, score in results:

            print(
                f"Match Score: {score}"
            )

            # Lower score = better match
            if score < 1.0:

                relevant_docs.append(
                    doc.page_content
                )

        if not relevant_docs:
            return None

        return "\n\n".join(
            relevant_docs
        )

    except Exception as e:

        print(
            "Search Error:",
            str(e)
        )

        return None


# -----------------------------
# Main Ask Function
# -----------------------------

def ask(question: str):

    context = search_lore(question)

    source = "📚 Local Knowledge Base"

    # -----------------------------
    # DuckDuckGo Fallback
    # -----------------------------

    if context is None:

        print(
            "Using DuckDuckGo Search..."
        )

        try:

            search = DuckDuckGoSearchRun()

            context = search.run(
                f"""
Anime or gaming lore question:

{question}

Provide accurate factual information.
"""
            )

            source = "🌐 DuckDuckGo Search"

            if (
                not context
                or len(context.strip()) < 20
            ):

                context = f"""
No useful search results were found.

User Question:
{question}

Provide the best answer using anime
and gaming knowledge.
"""

                source = "🤖 Groq Model Knowledge"

        except Exception as e:

            import traceback

            print(
                "\n========== WEB SEARCH ERROR =========="
            )

            traceback.print_exc()

            print(
                "=====================================\n"
            )

            context = f"""
No external search results were available.

User Question:
{question}

Provide the best answer using general
anime and gaming knowledge.
"""

            source = "🤖 Groq Model Knowledge"

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
You are GameLore Agent.

You are an expert on:

- Naruto
- Boruto
- Jujutsu Kaisen
- Demon Slayer
- Bleach
- One Piece
- Dragon Ball
- Elden Ring
- Anime Lore
- Gaming Lore

Instructions:

1. Use the supplied context.
2. Answer clearly and accurately.
3. Explain powers, abilities,
   history, and significance.
4. Use paragraphs for readability.
5. Use bullet points when useful.
6. If information is limited,
   explain what is known.
7. Do not invent unsupported facts.

Context:

{context}

Question:

{question}

Answer:
"""

    # -----------------------------
    # LLM Response
    # -----------------------------

    response = llm.invoke(
        prompt
    )

    answer = response.content.strip()

    if not answer:

        answer = (
            "I couldn't find enough "
            "information to answer "
            "that question."
        )

    return {
        "answer": answer,
        "source": source
    }


# -----------------------------
# Flask Agent Wrapper
# -----------------------------

class GameLoreAgent:

    def invoke(self, data):

        question = data[
            "messages"
        ][0]["content"]

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


# -----------------------------
# Local Testing
# -----------------------------

if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk: "
        )

        if question.lower() in [
            "quit",
            "exit"
        ]:
            break

        result = ask(question)

        print(
            "\nSource:"
        )

        print(
            result["source"]
        )

        print(
            "\nAnswer:"
        )

        print(
            result["answer"]
        )
