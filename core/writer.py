import random
from datetime import datetime

class PropagandaEngine:
    def __init__(self):
        self.hashtags = ["#LagosTraffic", "#UniversalMatrix", "#EconomicCrisis", "#Nigeria"]

    def generate_report(self, location, burn_rate, delay):
        # Format the money cleanly (e.g., ₦ 127,000,000)
        money = f"₦{burn_rate:,.0f}"
        
        current_time = datetime.now().strftime("%I:%M %p")

        # 1. THE ALARMIST (Twitter/X Style)
        tweet = (
            f"🚨 URGENT: {location} is currently bleeding {money} per hour in lost productivity.\n"
            f"⏱ Delay: {int(delay/60)} mins.\n"
            f"The economy is leaking. Who is fixing this?\n"
            f"{random.choice(self.hashtags)} {random.choice(self.hashtags)}"
        )

        # 2. THE ANALYST (Investor Report)
        report = (
            f"📊 MARKET UPDATE | {current_time}\n"
            f"Sector: {location}\n"
            f"Inefficiency Index: {money}/hr loss detected.\n"
            f"Recommendation: Infrastructure investment required immediately."
        )

        # 3. THE REVOLUTION (TikTok Script)
        script = (
            f"Video Hook: 'Stop scrolling. You are losing money right now.'\n"
            f"Visual: Show the Red Map of {location}.\n"
            f"Voiceover: 'It looks like just traffic. But the Universal Matrix proves that {location} "
            f"is burning {money} every single hour. That is YOUR money vanishing into thin air.'\n"
            f"Call to Action: 'Comment MATRIX if you want the full report.'"
        )

        return tweet, report, script