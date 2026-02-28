import feedparser
import sqlite3
import requests
from datetime import datetime

# Exemple minimal collecteur RSS
RSS_FEEDS = [
    "https://www.emploi.ma/rss",
    "https://www.dimajob.com/rss"
]

# Connexion SQLite
conn = sqlite3.connect("jobs.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS offers
             (date TEXT, site TEXT, title TEXT, company TEXT, location TEXT, description TEXT, link TEXT, score INTEGER)''')
conn.commit()

# Fonction simplifiée scoring
def calculate_score(text):
    score = 0
    keywords = ["chef de projet","marketing","commercial","vente","communication"]
    for k in keywords:
        if k in text.lower():
            score += 20
    if score > 100: score = 100
    return score

# Collecte RSS
for feed in RSS_FEEDS:
    d = feedparser.parse(feed)
    for entry in d.entries:
        title = entry.title
        link = entry.link
        description = entry.get("description","")
        score = calculate_score(title + " " + description)
        c.execute("INSERT INTO offers VALUES (?,?,?,?,?,?,?,?)",
                  (datetime.now(), feed, title, "Inconnue", "Inconnue", description, link, score))
conn.commit()
conn.close()
print("Collecte terminée")
