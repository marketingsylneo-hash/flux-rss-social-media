import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime
import os

# URL du flux RSS principal
RSS_URL = "https://jai-un-pote-dans-la.com/feed/"
CATEGORY = "social media"

def filter_rss():
    print("🔄 Récupération du flux RSS...")
    feed = feedparser.parse(RSS_URL)

    # Vérifier que le flux est bien récupéré
    if not feed.entries:
        print("⚠️ Aucun article trouvé — le flux source est peut-être temporairement inaccessible.")
    
    # Créer le nouveau flux
    fg = FeedGenerator()
    fg.title("J'ai un pote dans la com - Social Media")
    fg.link(href="https://jai-un-pote-dans-la.com/campagnes/social-media/", rel="alternate")
    fg.description("Flux RSS filtré pour la catégorie Social Media")
    fg.language('fr')

    # Filtrer les articles
    for entry in feed.entries:
        categories = [cat.term.lower() if hasattr(cat, 'term') else str(cat).lower()
                      for cat in entry.get('tags', [])]
        if any(CATEGORY in cat for cat in categories):
            fe = fg.add_entry()
            fe.title(entry.title)
            fe.link(href=entry.link)
            fe.description(entry.get('summary', ''))
            fe.published(entry.get('published', datetime.now().isoformat()))
            fe.guid(entry.link, permalink=True)

    # S'assurer que le dossier existe
    os.makedirs('output', exist_ok=True)

    # Générer le fichier RSS
    output_path = 'output/feed.xml'
    fg.rss_file(output_path, pretty=True)
    print("✅ Flux RSS filtré créé avec succès :", output_path)

    # Afficher un aperçu du contenu dans les logs
    preview = fg.rss_str(pretty=True).decode('utf-8')[:500]
    print("\n--- Aperçu du flux généré ---\n")
    print(preview)
    print("\n------------------------------\n")

if __name__ == "__main__":
    filter_rss()
