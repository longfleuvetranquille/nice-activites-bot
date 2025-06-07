import requests
import datetime
import openai
import os

# Clés récupérées depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Générer la date du jour
today = datetime.date.today()
prompt = f"Quelles sont les activités à Nice et aux alentours le {today.day}/{today.month}/{today.year} ? Donne un résumé clair, trié par type d’activité si possible (concert, expo, événement gratuit, etc)."

# Appel à OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

message = response.choices[0].message.content

# Envoi sur Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

send_telegram_message(message)
