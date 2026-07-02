import requests
from bs4 import BeautifulSoup
import os
import httpx
from dotenv import load_dotenv

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

        return f"""🏦 BoursoBank Parrainage Tracker

📅 Prochaine offre : {date}
💰 Prime filleul : {prime_filleul}
🎁 Prime parrain : {prime_parrain}

🔗 detective-banque.fr"""
        
    except Exception as e:
        return f"❌ Erreur : {e}"

def job():
    print("Scraping en cours...")
    resultat = scrape_taux()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    httpx.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": resultat})
    print("Message envoyé !")

job()