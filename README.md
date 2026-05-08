# 💊 Prescripto | AI Health Assistant

**Prescripto** is an end-to-end AI solution developed during **AI Hackathon Cluj 2026**, designed to digitize hand-written medical prescriptions and enhance patient adherence through automation and simplification.

## 🚀 The Problem
Illegible medical handwriting and complex jargon (disease codes, technical terms) often lead to confusion among patients. Prescripto eliminates these barriers by transforming a simple photo of a prescription into a digital, clear, and schedulable treatment plan.

## 🛠️ Architecture & Tech Stack
The project uses a modular architecture, separating AI processing from official data management:

* **Frontend:** [Streamlit](https://streamlit.io/) – for a fast, interactive user dashboard.
* **AI Engine:** [Google Gemini 1.5 Flash](https://ai.google.dev/) – utilized for:
    * **Multimodal OCR:** Extracting text from difficult handwritten images.
    * **Medical NLP:** Translating medical jargon into natural, empathetic language.
    * **Structured Output:** Generating JSON responses for seamless code integration.
* **Data Processing:** * `Pandas`: For searching and filtering through the official pharmaceutical database (CSV).
    * `PyPDF2`: For extracting definitions from the national disease code nomenclator (PDF).
* **Integrations:** Google Calendar API (for automated synchronization of medication hours).

## ✨ Key Features

### 1. Multi-Modal Prescription Analysis
The system processes the image and automatically extracts:
- Brand names and active ingredients (DCI).
- Dosages and administration frequency.
- Diagnostic codes (e.g., 462, J06).

### 2. Human-in-the-Loop (Data Validation)
For maximum safety, users can validate and edit the AI-extracted data. The app provides real-time suggestions from the official database as the user types, ensuring the correctness of commercial names.

### 3. "Medical to Human" Translator
Using LLM capabilities, we transform cold diagnostics like *"Unspecified acute pharyngitis"* into calm explanations: *"Your throat is inflamed and red, but with rest and hydration, you will feel better soon."*

### 4. Cost Optimization
The application automatically identifies **generic alternatives (DCI)** for prescribed medications, helping patients find more affordable options.

### 5. Smart Google Calendar Sync
Once validated, the prescription is transformed into recurring events in the patient's calendar, providing precise notifications for every dose.

## 📂 Project Structure
* `main.py`: User interface and service coordination logic.
* `services/ai_service.py`: Logic for Gemini API communication and prompt engineering.
* `services/data_service.py`: Handling of local databases (CSV/PDF).
* `data/`: Contains the medical nomenclators used.

