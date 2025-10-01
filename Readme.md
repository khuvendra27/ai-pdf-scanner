
# AI PDF Scanner – PDF API Project

This project is a Django-based API service that extracts and summarizes text from PDF documents, leveraging Large Language Models (LLMs) for intelligent summarization. It is designed for processing corporate filings, disclosures, and other structured documents.

## 🧩 Features

- **PDF Download & Parsing**: Fetches PDF files from provided URLs and extracts textual content.
- **Text Summarization**: Utilizes LLMs to generate concise summaries of extracted text.
- **Audit Logging**: Stores summaries and original text in a SQLite database for auditing purposes.
- **RESTful API**: Exposes endpoints for PDF processing and retrieval of audit logs.

## ⚙️ Technologies

- **Backend**: Django REST Framework
- **PDF Parsing**: pdfplumber
- **LLM Integration**: Google Gemini API (via `google-genai` client)
- **Environment Management**: dotenv for environment variables
- **Database**: SQLite (default in Django)

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/khuvendra27/ai-pdf-scanner.git
cd ai-pdf-scanner/pdf_api_project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# On Windows
.env\Scriptsctivate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000`.

## 🧪 Usage

### Summarize a PDF

Send a POST request to `/api/summarize/` with a JSON payload containing the PDF URL:

```json
{
  "url": "https://example.com/path/to/document.pdf"
}
```

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/summarize/   -H "Content-Type: application/json"   -d '{"url": "https://example.com/path/to/document.pdf"}'
```

### Retrieve Audit Logs

Send a GET request to `/api/audit/` to retrieve stored summaries:

```bash
curl http://127.0.0.1:8000/api/audit/
```

## 🛠️ API Endpoints

- `POST /api/summarize/`: Accepts a PDF URL, processes the document, and returns a summary.
- `GET /api/audit/`: Retrieves a list of all processed documents with their summaries.

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
