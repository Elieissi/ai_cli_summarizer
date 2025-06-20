# AI Note Summarizer CLI

A command-line application that uses the OpenAI API to summarize large text inputs into concise summaries. Built with modular object-oriented Python design. Notes and their summaries are stored in memory and can be saved to or loaded from disk.

---

## 🧠 Features

- Accepts long user-inputted text
- Automatically splits and summarizes using AI
- Stores notes as {"text": ..., "summary": ...}
- View all stored notes
- Save and load notes from notes.json

---

## 📦 Project Structure

```
summarizer/
├── main.py            # CLI entry point
├── summarizer.py      # Summarizer class + chunking
├── note_manager.py    # NoteManager class
├── notes.json         # Optional saved notes
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies
pip install openai

### 2. Set your OpenAI API key

You can input it at runtime, or store it in an .env file and load it with python-dotenv (optional extension).

### 3. Run the program
python main.py

---

## ✅ CLI Menu Options

1. Add new note → Enter text, get summary  
2. View notes → List all saved notes  
3. Save notes → Write to notes.json  
4. Exit → End program

---

## 🧱 Tech Stack

- Python 3.x  
- OpenAI SDK  
- JSON for persistence  
- Object-Oriented Design (no external frameworks)

---

