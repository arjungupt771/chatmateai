
# ChatMate AI

ChatMate AI is a Python-based chatbot built with Streamlit and Google's Gemini API. It supports conversational interaction and lets users upload PDF documents and ask questions using their extracted text as context.

## Features

- Conversational AI powered by Gemini.
- Multiple PDF uploads.
- PDF text extraction and document-based question answering.
- In-memory PDF processing without permanently saving uploaded files.
- Session-based conversation history.
- File-size validation and document-processing error handling.

## Tech Stack

- Python
- Streamlit
- Google Gen AI SDK
- Gemini
- pypdf
- python-dotenv

## Prerequisites

- Python 3.11 or a compatible Python version.
- A Google AI API key with access to the configured Gemini model.
- Git (optional, for cloning the repository).

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/arjungupt771/chatmateai.git
cd chatmateai
```

### 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the API key

Copy `.env.example` to `.env` and replace the placeholder with your own Gemini API key.

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

## How to Use

1. Start the application.
2. Upload one or more PDF documents using the sidebar.
3. Ask a question in the chat input.
4. Review the generated response, using the uploaded document text when available.

Each PDF must be no larger than 10 MB. Extracted document text is capped at 100,000 characters across the uploaded files.

## Limitations

- Scanned PDFs without an extractable text layer may not work.
- The application does not perform OCR.
- Answers may be inaccurate and should be checked against the original documents.
- Large documents may be truncated before being sent to the model.
- Responses require API connectivity, valid credentials, and available model quota.

## Troubleshooting

**Missing API key:** Verify that `.env` exists in the project root and contains `GEMINI_API_KEY`.

**Model or API error:** Verify your API key, model access, network connection, and quota.

**No text extracted:** Check whether the PDF contains selectable text or consists entirely of scanned images.

## License

No license has been specified. Check the repository's intended licensing before adding a license file.
