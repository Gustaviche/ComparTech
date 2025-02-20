import streamlit as st
import google.generativeai as genai

# Charger la clé API depuis les secrets de Streamlit Cloud
GOOGLE_API_KEY = st.secrets["google"]["api_key"]

# Configurer l'API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialiser le modèle
model = genai.GenerativeModel('gemini-1.5-flash')

# Création du prompt système
system_prompt = """
Tu es expert des matériels informatiques, en particulier les télévisions, ordinateurs, écrans PC, tablettes et smartphones.
Tu es très gentil, sympathique et patient.
"""

# Fonction d'initialisation de la session de chat (utilisé dans Streamlit)
def init_chat():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[{'role': 'user', 'parts': [system_prompt]}])

# Fonction pour obtenir la réponse du chatbot
def chatbot_response(user_input):
    try:
        # Assurer que la session est initialisée
        init_chat()

        # Obtenir la réponse du chatbot
        chat_session = st.session_state.chat_session
        response = chat_session.send_message(user_input)
        return response.text  # Retourne simplement le texte de la réponse
    except Exception as e:
        return f"Erreur lors de la génération de la réponse : {e}"
