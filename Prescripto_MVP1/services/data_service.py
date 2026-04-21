import pandas as pd
import PyPDF2
import os


def load_meds_database(csv_path="data/medicamente.csv"):
    """Încarcă CSV-ul cu medicamente folosind Pandas."""
    try:
        # Folosim index_col=False și tratăm posibilele erori de formatare
        df = pd.read_csv(csv_path, on_bad_lines='skip', sep=None, engine='python')
        return df
    except Exception as e:
        print(f"Eroare la citirea medicamentelor: {e}")
        return None


def find_alternatives_by_dci(dci_name, df):
    """Caută în DataFrame toate medicamentele care au același DCI."""
    if df is None or dci_name is None:
        return []

    # Presupunem că aveți o coloană numită 'DCI' sau 'Substanta activa' în CSV.
    # Va trebui să ajustați numele coloanei ('DCI') cu cel real din CSV-ul vostru!
    try:
        # Căutăm (case-insensitive) în coloana DCI
        rezultate = df[df['DCI'].str.contains(dci_name, case=False, na=False)]
        return rezultate.to_dict('records')  # Returnăm ca listă de dicționare
    except KeyError:
        return [{"eroare": "Nu am găsit coloana DCI în CSV. Verificați numele coloanelor!"}]


def get_disease_from_pdf(disease_code, pdf_path="data/coduri_boala.pdf"):
    """Caută un cod de boală și extrage exact rândul unde se află denumirea oficială."""
    if not os.path.exists(pdf_path):
        return None

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                if text:
                    # Spargem pagina în rânduri
                    randuri = text.split('\n')
                    for rand in randuri:
                        # Dacă găsește codul pe rândul respectiv, returnează tot rândul
                        if disease_code.upper() in rand.upper():
                            return rand.strip()
            return None  # Dacă nu găsește codul deloc
    except Exception as e:
        print(f"Eroare la citirea PDF-ului: {e}")
        return None