import streamlit as st
from PIL import Image
import pandas as pd

from services.ai_service import analyze_prescription, explain_diagnosis
from services.data_service import load_meds_database, find_alternatives_by_dci, get_disease_from_pdf

st.set_page_config(page_title="Prescripto MVP", layout="wide")

st.title("💊 Prescripto - Traducătorul tău de rețete medicale")
st.markdown("Încarcă o poză cu rețeta. AI-ul o va citi, iar tu validezi datele înainte să le punem în Google Calendar.")


@st.cache_data
def incarca_date():
    return load_meds_database("data/medicamente.csv")


@st.cache_data(show_spinner=False)
def traducere_diagnostic_salvata(text_medical):
    return explain_diagnosis(text_medical)



df_meds = incarca_date()

uploaded_file = st.file_uploader("Fă o poză la rețetă sau încarcă un fișier (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Rețeta Originală")
        image = Image.open(uploaded_file)
        st.image(image, caption="Verifică textul de pe poză", use_container_width=True)

    with col2:
        st.subheader("🤖 Analiza AI & Human-in-the-Loop")

        if st.button("Analizează Rețeta", type="primary"):
            with st.spinner("AI-ul citește scrisul de medic... Te rugăm să aștepți."):
                rezultat_ai = analyze_prescription(uploaded_file)
                st.session_state['date_reteta'] = rezultat_ai

        if 'date_reteta' in st.session_state:
            datele = st.session_state['date_reteta']

            if "eroare" in datele:
                st.error(datele["eroare"])
            else:
                st.success("Date extrase cu succes! Te rugăm să le validezi mai jos.")

                st.markdown("### 🩺 Diagnostic")
                valoare_initiala_cod = str(datele.get("cod_diagnostic", ""))
                if valoare_initiala_cod.lower() in ["none", "null"]:
                    valoare_initiala_cod = ""

                cod_boala_editat = st.text_input("Cod Diagnostic (Modifică/Șterge dacă AI-ul a luat prea mult text)",
                                                 value=valoare_initiala_cod)

                if cod_boala_editat:
                    coduri_individuale = [c.strip() for c in cod_boala_editat.split(",")]

                    for cod in coduri_individuale:
                        if cod:
                            st.info(f"🔍 Căutăm codul: **{cod}** în baza de date...")
                            text_brut_boala = get_disease_from_pdf(cod, "data/coduri_boala.pdf")

                            if text_brut_boala:
                                st.write(f"📄 *Jargon oficial extras:* {text_brut_boala}")
                                with st.spinner("AI-ul traduce diagnosticul pe înțelesul tău..."):
                                    explicatie_simpla = traducere_diagnostic_salvata(text_brut_boala)
                                    st.success(f"🩺 **Pe scurt:** {explicatie_simpla}")
                            else:
                                st.warning(f"Codul '{cod}' nu a fost găsit în nomenclator. Verifică dacă este corect.")
                else:
                    st.warning("Nu a fost introdus un cod de boală valid.")

                st.markdown("### 💊 Plan de Tratament (Editează dacă AI-ul a greșit)")

                with st.form("formular_validare"):
                    medicamente_confirmate = []

                    for i, med in enumerate(datele.get("medicamente", [])):
                        st.markdown(f"**Medicament {i + 1}**")

                        nume_citit_ai = med.get("nume_brand_citit", "")
                        st.info(f"🧐 **AI-ul a citit de pe foaie:** {nume_citit_ai}")

                        termen_cautare = st.text_input(
                            f"Caută manual medicamentul (sau corectează AI-ul):",
                            value=nume_citit_ai,
                            key=f"search_{i}"
                        )

                        if len(termen_cautare) >= 3:

                            termen_baza = termen_cautare[:4].upper()
                            match_df = df_meds[
                                df_meds['Denumire comerciala'].str.contains(termen_baza, case=False, na=False)]
                        else:
                            match_df = pd.DataFrame()

                        nume_ales_din_baza = None
                        if not match_df.empty:
                            optiuni_gasite = match_df['Denumire comerciala'].unique().tolist()
                            nume_ales_din_baza = st.selectbox(
                                "👉 Alege varianta exactă din nomenclator:",
                                options=optiuni_gasite,
                                key=f"select_{i}"
                            )
                        else:
                            st.warning(
                                f"⚠️ Nu am găsit '{termen_cautare}' în baza de date. Încearcă să schimbi literele.")

                        nume_final_de_salvat = termen_cautare

                        if nume_ales_din_baza:
                            nume_final_de_salvat = nume_ales_din_baza
                            rand_selectat = match_df[match_df['Denumire comerciala'] == nume_ales_din_baza].iloc[0]
                            dci_gasit = rand_selectat['DCI']

                            st.success(f"🔬 Substanță activă (DCI) confirmată: **{dci_gasit}**")

                            alternative = find_alternatives_by_dci(dci_gasit, df_meds)
                            if len(alternative) > 1:
                                optiuni_brand = list(
                                    set([str(alt.get('Denumire comerciala', '')) for alt in alternative if
                                         alt.get('Denumire comerciala') != nume_ales_din_baza][:5]))
                                if optiuni_brand:
                                    st.write(f"💡 Alternative mai ieftine/similare: {', '.join(optiuni_brand)}")

                        doza = st.text_input("Dozaj", value=med.get("doza", ""), key=f"doza_{i}")
                        instructiuni = st.text_area("Instrucțiuni Pacient", value=med.get("instructiuni_pacient", ""),
                                                    key=f"inst_{i}")

                        st.divider()

                        medicamente_confirmate.append({
                            "nume": nume_final_de_salvat,
                            "doza": doza,
                            "instructiuni": instructiuni,
                            "ore": med.get("ore_sugerate", [])
                        })

                    submit = st.form_submit_button("✅ Datele sunt corecte. Salvează în Calendar!")

                    if submit:
                        st.balloons()
                        st.success("Perfect! Datele validate sunt gata de a fi trimise în Google Calendar.")
                        st.json(medicamente_confirmate)