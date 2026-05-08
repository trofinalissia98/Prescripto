import google.generativeai as genai
import json
from utils.config import GEMINI_API_KEY
from PIL import Image


genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel('gemini-flash-latest')



def analyze_prescription(image_file):

    try:
        img = Image.open(image_file)
    except Exception as e:
        return {"eroare": f"Nu am putut deschide imaginea: {e}"}


    prompt = """
    Ești un asistent medical expert în citirea rețetelor medicale scrise de mână sau printate.
    Te rog să analizezi imaginea acestei rețete și să extragi lista de medicamente.
    Dacă pe rețetă apare și un diagnostic (sau un cod de boală, mereu este format din cifre, un numar de la 1 la 999), extrage-l și pe acela.

    Traduce jargonul medical în limbaj uman simplu, pe care l-ar înțelege un pacient fără pregătire medicală.
    Nu pune diagnostice noi, limitează-te strict la ce scrie pe rețetă.

    TREBUIE OBLIGATORIU să răspunzi DOAR cu un obiect JSON valid, fără niciun alt text înainte sau după.
    Structura JSON-ului trebuie să fie exact aceasta:
    {
      "cod_diagnostic": "Extrage DOAR codurile scurte de boală (ex: 462, E11, J06). IGNORĂ texte adiacente precum 'CIC', 'reteta', date sau numere de ordine. Dacă nu ești 100% sigur că e cod de boală, pune null.",
      "medicamente": [
        {
          "nume_brand_citit": "numele medicamentului de pe rețetă",
          "doza": "ex: 500mg, 10ml",
          "frecventa_pe_zi": "numărul de administrări, ex: 2, 3",
          "instructiuni_pacient": "ex: Luni ora 08:00 - ia o pastilă. Evită sucul de grepfrut.",
          "ore_sugerate": ["08:00", "20:00"]
        }
      ]
    }
    """

    try:
        response = model.generate_content([prompt, img])
        text_response = response.text

        text_response = text_response.replace('```json', '').replace('```', '').strip()

        date_structurate = json.loads(text_response)
        return date_structurate

    except json.JSONDecodeError:
        return {
            "eroare": "AI-ul nu a returnat un JSON valid. S-a încurcat la citirea scrisului. Încearcă o poză mai clară!"}
    except Exception as e:
        return {"eroare": f"Eroare la procesarea AI: {str(e)}"}


def explain_diagnosis(medical_text):
    if not medical_text:
        return "Nu am putut extrage textul diagnosticului."

    prompt = f"""
    Ești un medic empatic. Am extras din nomenclatorul oficial următorul diagnostic (care conține jargon și probabil un cod):
    "{medical_text}"

    Te rog să explici pe scurt, în 1-2 propoziții, ce înseamnă această afecțiune, folosind un limbaj extrem de simplu, pe care l-ar înțelege un pacient fără pregătire medicală sau un copil. Fii calm și nu folosi termeni alarmanti.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Eroare la generarea explicației: {e}"