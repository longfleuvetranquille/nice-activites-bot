# Bot Telegram - Résumé quotidien d'activités à Nice

Ce projet contient un script Python qui envoie chaque jour, via Telegram, un résumé des activités à faire à Nice et dans ses alentours pour la date du jour. Il utilise l'API OpenAI (modèle GPT-4 ou GPT-3.5) pour générer le texte du résumé, et l'API Telegram pour envoyer ce texte sous forme de message.

## Configuration des variables d'environnement

Avant d'exécuter le script, vous devez configurer trois variables d'environnement indispensables :

- **OPENAI_API_KEY** : votre clé API OpenAI (elle commence généralement par `sk-...`).
- **TELEGRAM_BOT_TOKEN** : le token HTTP API de votre bot Telegram (fourni par [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot%3F) lors de la création du bot).
- **TELEGRAM_CHAT_ID** : l'identifiant du chat Telegram où envoyer le message (votre identifiant d'utilisateur Telegram si vous envoyez le message à vous-même, ou l'ID d'un groupe/canal).

Vous pouvez définir ces variables de deux manières :
- En créant un fichier `.env` à la racine du projet (en copiant le modèle `.env.example`) et en y renseignant les valeurs.
- Ou en définissant ces variables directement dans votre environnement d'exécution (par exemple via le panneau d'administration de Render ou des variables système).

## Installation des dépendances

Assurez-vous d'utiliser Python 3.7 ou une version ultérieure. Installez les dépendances du projet à l'aide de la commande suivante :

```bash
pip install -r requirements.txt
```

Cela installera les packages `openai`, `requests` et `python-dotenv` nécessaires à l'exécution du script.

## Exécution du script

Une fois les variables d'environnement configurées et les dépendances installées, vous pouvez exécuter le script manuellement en lançant :

```bash
python main.py
```

Le script génère dynamiquement un prompt avec la date du jour (format **jour/mois/année**, par exemple "Quelles sont les activités à Nice et aux alentours le 07/06/2025 ?"). Il envoie ce prompt à l'API d'OpenAI (GPT-4 par défaut) pour obtenir un résumé des événements/activités, puis envoie le résultat sur Telegram via l'API Bot. Si le modèle GPT-4 n'est pas disponible, le script basculera automatiquement sur GPT-3.5-turbo. 

## Utilisation avec un Cron Job sur Render

Pour automatiser l'envoi quotidien via la plateforme [Render.com](https://render.com), suivez ces étapes :

1. **Déploiement du code** : Poussez ce projet sur un dépôt Git (GitHub, GitLab, etc.) afin que Render puisse y accéder.
2. **Création du Cron Job** : Sur le tableau de bord Render, créez un nouveau *Cron Job*. Lors de la configuration :
    - Connectez le Cron Job à votre dépôt Git et sélectionnez la branche appropriée (par exemple `main`).
    - Indiquez la commande de lancement du script, par exemple : `python main.py`.
3. **Configuration des variables d'environnement sur Render** : Dans les paramètres du Cron Job, ajoutez les variables `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` (vous pouvez les ajouter manuellement ou utiliser l'option "Add from .env" et importer votre fichier `.env` local en veillant à ne pas committer vos secrets).
4. **Planification** : Définissez la fréquence d'exécution en fournissant une expression cron. Par exemple, `0 7 * * *` pour un envoi tous les jours à 7h00 UTC (ce qui correspond à 9h00, heure de Paris). Ajustez l'horaire selon vos besoins.
5. **Déploiement** : Validez et lancez le déploiement du Cron Job. Render va installer les dépendances définies dans `requirements.txt` et planifier l'exécution du script.
6. **Test initial** : Vous pouvez effectuer un test en déclenchant manuellement le Cron Job via l'interface Render (bouton *"Trigger Run"* dans la page du service Cron Job) afin de vérifier que le message s'envoie correctement sur Telegram.

Une fois ces étapes réalisées, le script s'exécutera automatiquement selon la planification définie, et vous recevrez chaque jour sur Telegram le résumé des activités à faire à Nice et aux alentours pour la date du jour.
