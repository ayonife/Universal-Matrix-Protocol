import random
import time

class SkillsAgent:
    def __init__(self):
        # REAL JOBS with REQUIRED SKILLS
        self.real_jobs = [
            {
                "id": "J01", "role": "Python Intern", "company": "Bincom Dev Center", 
                "salary": "₦120k", "link": "https://bincom.net/trainee",
                "req_skills": ["Python", "Git", "Basic SQL"],
                "course_rec": "CS101: Intro to Programming"
            },
            {
                "id": "J02", "role": "Data Analyst (Entry)", "company": "Kuda Bank", 
                "salary": "₦350k", "link": "https://kuda.com/careers",
                "req_skills": ["Excel", "SQL", "PowerBI"],
                "course_rec": "STA202: Statistics & Probability"
            },
            {
                "id": "J03", "role": "Cybersecurity Analyst", "company": "Interswitch", 
                "salary": "₦500k", "link": "#",
                "req_skills": ["Networking", "Linux", "Ethical Hacking"],
                "course_rec": "CS304: Network Security"
            }
        ]

    def verify_identity(self, nin_id):
        # SIMULATED DB LOOKUP
        time.sleep(1.5)
        
        # DEMO USER 1: The Architect (High Match)
        if nin_id == "11111111111":
            return {
                "name": "Ayonife (Architect)", 
                "status": "VERIFIED", 
                "school": "LASUSTECH", 
                "level": "200L Math",
                "skills": ["Python", "Git", "Networking", "Linux"] # Has most skills
            }
        
        # DEMO USER 2: The Freshman (Low Match - Needs Advice)
        elif nin_id == "22222222222":
             return {
                "name": "Chinedu (Fresher)", 
                "status": "VERIFIED", 
                "school": "LASUSTECH", 
                "level": "100L CS",
                "skills": ["Excel", "Basic Math"] # Needs to learn more
            }
            
        return None

    def match_jobs(self, user_skills):
        # The Core "Matrix Matching" Logic
        results = []
        
        for job in self.real_jobs:
            reqs = set(job['req_skills'])
            user = set(user_skills)
            
            # 1. Calculate Intersection (What they have)
            has = user.intersection(reqs)
            
            # 2. Calculate Difference (The GAP)
            missing = reqs.difference(user)
            
            # 3. Score
            score = int((len(has) / len(reqs)) * 100)
            
            results.append({
                "job": job,
                "score": score,
                "missing": list(missing)
            })
            
        # Sort by best match
        return sorted(results, key=lambda x: x['score'], reverse=True)
