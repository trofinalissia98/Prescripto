import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Atenție! Nu am găsit GEMINI_API_KEY în fișierul .env. Verifică dacă l-ai creat corect.")