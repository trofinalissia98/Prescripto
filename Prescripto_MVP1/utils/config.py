import os
from dotenv import load_dotenv

# Încărcăm variabilele din fișierul .env
load_dotenv()

# Salvăm cheia într-o variabilă Python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Atenție! Nu am găsit GEMINI_API_KEY în fișierul .env. Verifică dacă l-ai creat corect.")