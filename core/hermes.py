import requests

class Messenger:
    def __init__(self):
        # ✅ YOUR CREDENTIALS (PRE-FILLED)
        self.bot_token = "8532957676:AAH2GL8pMIVqrNTdyfCgi31t_JOwhgn-nGw"
        self.chat_id = "6463516752"

    def send_alert(self, message):
        """Sends a message to your Telegram App"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✔ MESSAGE SENT TO TELEGRAM")
                return True
            else:
                print(f"❌ TELEGRAM ERROR: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ CONNECTION ERROR: {e}")
            return False

# Self-test block
if __name__ == "__main__":
    bot = Messenger()
    print("📡 SENDING TEST SIGNAL...")
    bot.send_alert("🚨 *SYSTEM ALERT*\n\n**Universal Matrix Protocol**\nConnection Verified.\nUser: @Airneytech")