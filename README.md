# 🎮 GameLore Agent

An AI-powered Anime & Gaming Lore Assistant built with Flask, Groq, LangChain, and ChromaDB.

## ✨ Features

* Anime Lore Q&A
* Gaming Lore Q&A
* Retrieval-Augmented Generation (RAG)
* ChromaDB Vector Database
* HuggingFace Embeddings
* Groq LLM Integration
* DuckDuckGo Search Fallback
* Modern Flask Web Interface
* Source-Aware Responses

---

## 🌍 Supported Universes

### Anime

* Naruto
* Boruto
* Jujutsu Kaisen
* Demon Slayer
* Bleach
* One Piece
* Dragon Ball

### Games

* Elden Ring

---

## 🛠️ Tech Stack

* Python
* Flask
* LangChain
* Groq
* ChromaDB
* HuggingFace Embeddings
* Sentence Transformers
* DuckDuckGo Search

---

## 📂 Project Structure

```text
GameLore_Agent/
│
├── data/
│   └── lore markdown files
│
├── chroma_db/
│   └── vector database
│
├── static/
│   ├── Naruto.png
│   ├── Gojo.png
│   ├── Sukuna.png
│   └── Tanjiro.png
│
├── templates/
│   └── index.html
│
├── app.py
├── agent.py
├── ingest.py
├── requirements.txt
└── README.md
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Sarthak21-9-2000/GameLore_Agent.git
cd GameLore_Agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 📚 Create Vector Database

Run:

```bash
python ingest.py
```

This will:

* Load lore documents from the `data/` folder
* Split them into chunks
* Generate embeddings
* Store vectors in ChromaDB

---

## ▶️ Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔎 How It Works

1. User asks a lore question.
2. ChromaDB searches the knowledge base.
3. Relevant context is retrieved.
4. Groq LLM generates an answer.
5. If no relevant context exists, DuckDuckGo search is used as fallback.
6. Response is returned with source information.

---

## 📸 Example Questions

* Who is Gojo Satoru?
* Explain Sukuna's powers.
* What is the history of the Akatsuki?
* How does Bankai work in Bleach?
* Who is the strongest Elden Ring demigod?
* What is Gear 5 in One Piece?

---

## 👨‍💻 Author

Sarthak Kapila

GitHub: [Sarthak21-9-2000](https://github.com/Sarthak21-9-2000)

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
