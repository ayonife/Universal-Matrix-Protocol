import feedparser
from textblob import TextBlob
import re

class NewsAgent:
    def __init__(self):
        # 📡 REAL DATA SOURCES (RSS)
        self.sources = [
            "https://news.google.com/rss/search?q=Lagos+Nigeria&hl=en-NG&gl=NG&ceid=NG:en", # Lagos News
            "https://cointelegraph.com/rss" # Crypto News
        ]
        
        # ⚠️ PANIC TRIGGERS (If these words appear, Panic goes UP)
        self.panic_keywords = [
            "crash", "collapse", "crisis", "riot", "protest", "scarcity", 
            "shortage", "blackout", "explosion", "kill", "attack", "plunge", 
            "ban", "shutdown", "strike"
        ]
        
        # ✅ CALM TRIGGERS (If these words appear, Panic goes DOWN)
        self.calm_keywords = [
            "growth", "stable", "profit", "launch", "success", 
            "restore", "peace", "agreement", "record", "bull"
        ]

    def scan_network(self):
        """
        Scans the internet for real headlines.
        Returns: { 'headline': str, 'sentiment': float, 'panic_factor': float }
        """
        headlines = []
        panic_score = 0.0
        
        # 1. Fetch Headlines
        for url in self.sources:
            try:
                feed = feedparser.parse(url)
                # Get top 3 stories from each source
                for entry in feed.entries[:3]:
                    headlines.append(entry.title)
            except:
                pass

        # 2. Analyze the "Vibe" of Lagos
        if not headlines:
            return {"headline": "NO SIGNAL", "panic_factor": 0.5} # Default neutral

        total_sentiment = 0
        trigger_count = 0
        
        latest_headline = headlines[0] # The breaking news

        for title in headlines:
            # Check for Panic Words
            for word in self.panic_keywords:
                if word in title.lower():
                    trigger_count += 0.2 # Each bad word adds 20% Panic
            
            # Check for Calm Words
            for word in self.calm_keywords:
                if word in title.lower():
                    trigger_count -= 0.1 # Each good word reduces Panic

        # Cap the Panic (0.0 to 1.0)
        final_panic = 0.5 + trigger_count
        final_panic = max(0.0, min(1.0, final_panic))
        
        return {
            "headline": latest_headline,
            "panic_factor": final_panic
        }