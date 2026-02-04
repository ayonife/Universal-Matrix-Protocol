import random
import time

class SkillsAgent:
    def __init__(self):
        # REAL JOBS scraped from Lagos market (Feb 2026)
        self.real_jobs = [
            {"role": "Python Trainee (Intern)", "company": "Bincom Dev Center", "location": "Lagos", "salary": "₦80k - ₦120k", "link": "https://bincom.net/trainee"},
            {"role": "Data Analyst Entry Level", "company": "Kuda Bank", "location": "Lagos (Hybrid)", "salary": "₦250k - ₦400k", "link": "https://kuda.com/careers"},
            {"role": "Junior Backend Eng", "company": "Moniepoint", "location": "Lekki", "salary": "₦500k+", "link": "https://moniepoint.com/careers"},
            {"role": "IT Support Intern", "company": "Dangote Group", "location": "Ikoyi", "salary": "₦150k", "link": "#"},
            {"role": "AI Research Intern", "company": "Omnix Labs", "location": "Yaba", "salary": "₦200k", "link": "#"}
        ]

    def verify_identity(self, nin_id):
        # SIMULATION OF REAL VERIFICATION (We can't access NIMC legally)
        time.sleep(2.0) # Fake "Connecting to Server..." delay
        
        # Valid Test IDs for Demo
        if nin_id == "11111111111":
            return {"name": "Ayonife (Architect)", "status": "VERIFIED", "school": "LASUSTECH", "level": "200L Math"}
        elif len(str(nin_id)) == 11 and nin_id.isdigit():
            # For any other 11-digit number, pretend it's a student
            return {"name": f"Student-{nin_id[-4:]}", "status": "VERIFIED", "school": "UNILAG", "level": "400L CS"}
        else:
            return None

    def fetch_certificates(self, nin_id):
        # REALISTIC BADGES
        return [
            {"name": "Python Essentials 1", "issuer": "Cisco", "badge": "🐍"},
            {"name": "CyberOps Associate", "issuer": "Cisco", "badge": "🛡️"},
            {"name": "Data Analytics", "issuer": "Coursera/Google", "badge": "📊"}
        ]

    def match_jobs(self, user_certs):
        # Return the Real Jobs list
        return self.real_jobs
