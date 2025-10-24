import feedparser
from feedgen.feed import FeedGenerator
import requests
from datetime import datetime
import os

# URL du flux RSS principal
RSS_URL = "https://jai-un-pote-dans-la.com/feed/"

# Catégorie à filtrer
CATEGORY = "social media"

def filter_rss():
    # Récupérer le flux RSS
    feed = feedparser.parse(RSS_URL)
    
    # Créer un nouveau flux
    fg = FeedGenerator()
    fg.title(f"{feed.feed.title} - Social Media")
    fg.link(href="https://jai-un-pote-dans-la.com/campagnes/social-media/", rel='alternate')
    fg.description(f"Flux RSS filtré pour la catégorie Social Media")
    fg.language('fr')
    
    # Filtrer les articles
    for entry in feed.entries:
        # Vérifier si l'article appartient à la catégorie Social Media
        categories = [cat.term.lower() if hasattr(cat, 'term') else str(cat).lower() 
                     for cat in entry.get('tags', [])]
        
        if any(CATEGORY in cat for cat in categories):
            fe = fg.add_entry()
            fe.title(entry.title)
            fe.link(href=entry.link)
            fe.description(entry.get('summary', ''))
            fe.published(entry.get('published', datetime.now().isoformat()))
            fe.guid(entry.link, permalink=True)
    
    # Créer le dossier output s'il n'existe pas
    os.makedirs('output', exist_ok=True)
    
    # Générer le fichier RSS
    fg.rss_file('output/feed.xml', pretty=True)
print("Contenu du flux :", fg.rss_str(pretty=True)[:500])


if __name__ == "__main__":
    filter_rss()
