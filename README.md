import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations sensibles depuis les variables d'environnement
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Vérifier la présence des variables d'environnement requises
if not openai_api_key or not telegram_token or not telegram_chat_id:
    raise RuntimeError("Des variables d'environnement requises sont manquantes. Veuillez vérifier le fichier .env ou la configuration de votre environnement.")

# Initialiser le client OpenAI avec la clé d'API
client = OpenAI(api_key=openai_api_key)

# Générer la date d'aujourd'hui au format jour/mois/année
today = datetime.now()
date_str = today.strftime("%d/%m/%Y")

# Créer le prompt en français avec la date du jour
prompt = f"Quelles sont les activités à Nice et aux alentours le {date_str} ?"

# Préparer le message pour l'appel de l'API OpenAI
messages = [
    {"role": "user", "content": prompt}
]

try:
    # Appeler l'API OpenAI (modèle GPT-4 par défaut)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
except Exception as e:
    # En cas d'erreur (par exemple si GPT-4 n'est pas disponible), utiliser GPT-3.5
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

# Extraire le texte de la réponse de l'assistant
reply_text = response.choices[0].message.content.strip()

# Envoyer le texte via l'API du bot Telegram
telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
payload = {"chat_id": telegram_chat_id, "text": reply_text}
result = requests.post(telegram_url, json=payload)

# Vérifier que l'envoi du message a réussi (sinon, lever une exception)
result.raise_for_status()
