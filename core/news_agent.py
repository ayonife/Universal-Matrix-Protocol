import feedparser
from textblob import TextBlob
import random

class NewsAgent:
    def __init__(self):
        # REAL Nigerian News Feeds
        self.sources = [
            "https://rss.punchng.com/v1/category/latest_news",
            "https://www.vanguardngr.com/feed",
            "https://dailytrust.com/feed",
            "https://gazettengr.com/feed"
        ]
        self.panic_words = ["crisis", "kill", "explosion", "collapse", "strike", "protest", "crash", "scarcity", "fuel", "tinubu"]

    def scan_network(self):
        """
        Scrapes news for panic signals AND links.
        Returns: { 
            'panic_factor': 0.0-1.0, 
            'stories': [ {'title': str, 'link': str, 'source': str}, ... ] 
        }
        """
        try:
            # Pick a random source to vary the news mix
            url = random.choice(self.sources)
            feed = feedparser.parse(url)
            
            if not feed.entries:
                return {
                    "panic_factor": 0.2, 
                    "stories": [{"title": "No Signal", "link": "#", "source": "OFFLINE"}]
                }

            # Analyze Panic & Collect Stories
            panic_score = 0.0
            stories = []
            
            # Grab Top 3 Stories
            for entry in feed.entries[:3]:
                text = entry.title
                link = entry.link
                
                # Sentiment Calc
                blob = TextBlob(text.lower())
                if blob.sentiment.polarity < -0.1: panic_score += 0.2
                for word in self.panic_words:
                    if word in text.lower(): panic_score += 0.3
                
                # Clean up source name
                source_name = "NEWS"
                if "punch" in url: source_name = "PUNCH"
                elif "vanguard" in url: source_name = "VANGUARD"
                elif "dailytrust" in url: source_name = "DAILY TRUST"
                
                stories.append({"title": text, "link": link, "source": source_name})
            
            final_score = min(0.99, max(0.1, panic_score))
            
            return {
                "panic_factor": final_score, 
                "stories": stories
            }

        except Exception as e:
            return {
                "panic_factor": 0.0, 
                "stories": [{"title": "Connection Error", "link": "#", "source": "SYSTEM"}]
            }