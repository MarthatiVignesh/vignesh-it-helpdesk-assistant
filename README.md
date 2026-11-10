# Vignesh – IT Helpdesk Assistant

An AI-powered IT Helpdesk Assistant built with Python, Groq, Retrieval-Augmented Generation (RAG), Sentence Transformers, and FAISS.

The project demonstrates how an AI agent can answer common IT support questions from a knowledge guide and classify support requests by category and priority.

## Features

- **Groq LLM integration:** Uses the `openai/gpt-oss-20b` model through the Groq API.
- **Ticket classification:** Uses zero-shot and few-shot prompt engineering to classify IT issues into Password, VPN, Email, or Unknown categories and assign Low, Medium, or High priority.
- **RAG knowledge search:** Splits the IT Helpdesk Guide into overlapping text chunks, creates embeddings with `all-MiniLM-L6-v2`, stores them in FAISS, and retrieves the top three relevant chunks.
- **Tool-using agent:** Automatically selects document search for IT how-to questions or ticket classification when the user explicitly asks to raise a ticket.
- **Guardrails:** Refuses unrelated questions and is instructed not to request or disclose passwords.

> **Scope note:** This is an educational prototype using fictional TechNova Solutions policies. Ticket classification does not create, submit, or assign a real support ticket. The `.example` portal addresses in the sample guide are placeholders, not live company services.

## Project Structure

```text
vignesh-it-helpdesk-assistant/
├── data/
│   └── tickets.csv
├── documents/
│   └── it_helpdesk_guide.md
├── results/
│   ├── prompt_comparison.md
│   ├── rag_results.md
│   ├── spec.md
│   └── testing_results.md
├── agent.py
├── classify.py
├── llm.py
├── rag.py
├── test_questions.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Technology Stack

- Python 3.13
- Groq API and `openai/gpt-oss-20b`
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS CPU
- pandas
- python-dotenv

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MarthatiVignesh/vignesh-it-helpdesk-assistant.git
cd vignesh-it-helpdesk-assistant
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get an API key from the [Groq Console](https://console.groq.com/). Keep the key private. Do not commit `.env` to Git.

## Run the Project

Run the standalone LLM test:

```bash
python llm.py
```

Run ticket classification and prompt comparison:

```bash
python classify.py
```

Run the RAG demonstration:

```bash
python rag.py
```

Run the interactive AI Helpdesk Agent:

```bash
python agent.py
```

Type `exit` to close the interactive agent.

## Example Questions

| User question | Expected agent action |
|---|---|
| How do I reset my password? | Search the IT Helpdesk Guide |
| What should I do if the VPN shows connection timed out? | Search the IT Helpdesk Guide |
| What is the size limit for my mailbox? | Search the IT Helpdesk Guide |
| My VPN keeps disconnecting; please raise a ticket. | Classify the issue and priority |
| I clicked a strange link in an email; please raise a ticket. | Classify the issue and priority |
| What is the company leave policy? | Refuse because it is outside IT support scope |

## Evaluation Notes

The recorded prompt comparison evaluated the first five tickets in `data/tickets.csv`:

- Zero-shot prompting: 4/5 correct (80%)
- Few-shot prompting: 5/5 correct (100%)

These figures describe that five-ticket comparison only; they are not a full-dataset benchmark.

See the `results/` directory for the prompt comparison, RAG examples, agent specification, and testing report.

## Security

- Store the Groq API key only in the local `.env` file.
- The `.gitignore` excludes `.env`, the virtual environment, and Python cache files.
- Never ask users to share passwords.
- This prototype is for learning and demonstration; review and strengthen security controls before any real deployment.

## Author

**Vignesh Marthati**  
GitHub: [@MarthatiVignesh](https://github.com/MarthatiVignesh)
