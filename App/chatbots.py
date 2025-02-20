import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
# Charger la clé API
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
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
    # Assurer que la session est initialisée
    init_chat()

    # Obtenir la réponse du chatbot
    chat_session = st.session_state.chat_session
    response = chat_session.send_message(user_input)
    return response.text  # Retourne simplement le texte de la réponse
