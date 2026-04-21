import google.generativeai as genai
from utils.config import GEMINI_API_KEY

print("Se verifică cheia API...")
genai.configure(api_key=GEMINI_API_KEY)

try:
    print("\nModelele disponibile pentru cheia ta sunt:")
    modele_gasite = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
            modele_gasite = True

    if not modele_gasite:
        print("Atenție: Cheia ta API este validă, dar nu are acces la niciun model de generare text/imagini!")
except Exception as e:
    print(f"\nEroare la conectarea cu Google: {e}")