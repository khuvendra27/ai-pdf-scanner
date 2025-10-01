from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import URLSerializer
import requests
import pdfplumber
from pathlib import Path
from google import genai  # LLM client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize LLM client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not set in environment variables")

# Simple in-memory log for audit
audit_log = {}

# Initialize the LLM client (expects GEMINI_API_KEY in environment variables)
client = genai.Client()

class SummarizePDFView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']

            # Step 1: Download PDF
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/140.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                }
                response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Failed to download PDF: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the PDF temporarily
            temp_pdf_path = Path("temp.pdf")
            with open(temp_pdf_path, "wb") as f:
                f.write(response.content)

            # Step 2: Extract text using pdfplumber
            try:
                extracted_text = ""
                with pdfplumber.open(temp_pdf_path) as pdf:
                    for page in pdf.pages:
                        extracted_text += page.extract_text() or ""
            except Exception as e:
                return Response(
                    {"error": f"Failed to extract text from PDF: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Step 3: Summarize text using LLM
            try:
                prompt = (
                    "Summarize the following corporate filing PDF text in short and clear sentences. "
                    "Focus on the main outcomes of the board meeting and key decisions:\n\n"
                    f"{extracted_text}"
                )

                llm_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                summary_text = llm_response.text.strip()
            except Exception as e:
                return Response(
                    {"error": f"Failed to summarize text: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Step 4: Log extracted text and summary
            audit_log[url] = {
                "extracted_text": extracted_text,
                "summary": summary_text
            }

            # Step 5: Return JSON response
            return Response(
                {
                    "url_received": url,
                    "summary": summary_text,
                    "message": "PDF processed and summarized successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
