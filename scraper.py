import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def scrape_taux():
    url = "https://www.detective-banque.fr/banque/boursorama-banque/prochain-parrainage-booste-boursorama/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        texte = soup.get_text()
        date = ""
        prime_filleul = ""
        prime_parrain = ""
        
        lignes = [l.strip() for l in texte.split('\n') if l.strip()]
        
        for i, ligne in enumerate(lignes):
            if "Du " in ligne and "2026" in ligne and not date:
                date = ligne.replace("DateDu ", "Du ")
            if "PrimeJusqu" in ligne and not prime_filleul:
                prime_filleul = "Jusqu'à 200€"
            if "80€" in ligne and "110€" in ligne and not prime_parrain:
                prime_parrain = ligne.replace("PrimeEntre", "Entre")

        message = f"""🏦 BoursoBank Parrainage Tracker

📅 Prochaine offre : {date}
💰 Prime filleul : {prime_filleul}
🎁 Prime parrain : {prime_parrain}

🔗 detective-banque.fr"""
        
        return message
        
    except Exception as e:
        return f"❌ Erreur : {e}"

async def envoyer_message(texte):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=texte)

def job():
    print("Scraping en cours...")
    resultat = scrape_taux()
    asyncio.run(envoyer_message(resultat))
    print("Message envoyé !")

schedule.every().day.at("09:00").do(job)
print("✅ Tracker démarré - notification chaque matin à 9h")

while True:
    schedule.run_pending()
    time.sleep(60)