# 🎮 GameLore Agent

An AI-powered Anime & Gaming Lore Assistant built with Flask, Groq, LangChain, and ChromaDB.

## Features

* Anime lore Q&A
* Gaming lore Q&A
* ChromaDB vector search
* Groq LLM integration
* DuckDuckGo fallback search
* Modern Flask UI
* Source-aware responses

## Supported Universes

* Naruto
* Boruto
* Jujutsu Kaisen
* Demon Slayer
* Bleach
* One Piece
* Dragon Ball
* Elden Ring

## Tech Stack

* Python
* Flask
* LangChain
* Groq
* ChromaDB
* HuggingFace Embeddings
* DuckDuckGo Search

## Installation

```bash
git clone https://github.com/Sarthak21-9-2000/GameLore_Agent.git
cd GameLore_Agent
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
GameLore_Agent/
├── app.py
├── agent.py
├── ingest.py
├── requirements.txt
├── data/
├── static/
└── templates/
```

## Author

Sarthak Kapila

GitHub:
https://github.com/Sarthak21-9-2000
