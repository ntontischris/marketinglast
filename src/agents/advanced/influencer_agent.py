import os
import json
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

load_dotenv()

class InfluencerAgent(BaseAgent):
    """
    Πράκτορας Ανάλυσης Επιρροής
    Εντοπίζει και προτείνει στρατηγικές συνεργασίας με influencers
    """
    
    def __init__(self):
        super().__init__(name="Πράκτορας Επιρροής")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY δεν βρέθηκε στο .env αρχείο")
        self.client = Groq(api_key=api_key)
        
        print(f"'{self.name}' αρχικοποιήθηκε με το μοντέλο: {self.model_name}")
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Αναλύει επιρροές και προτείνει συνεργασίες με influencers
        """
        topic = state.get("topic", "")
        industry = state.get("user_profile", {}).get("industry", "γενικό")
        if not topic:
            return {**state, "influencer_analysis": "Δεν υπάρχει θέμα ανάλυσης επιρροής"}
        
        print(f"-- '{self.name}' εντοπίζει top influencers για το θέμα '{topic}'... --")
        
        top_influencers = self._find_top_influencers(topic, industry)
        collaboration_strategies = self._suggest_collaboration_strategies(topic)
        
        influencer_report = {
            "top_influencers": top_influencers,
            "collaboration_strategies": collaboration_strategies,
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {**state, "influencer_analysis": influencer_report}
    
    def _find_top_influencers(self, topic: str, industry: str) -> List[Dict[str, str]]:
        """Εντοπίζει κορυφαίους influencers"""
        prompt = f"""
        Ως ειδικός στη διαχείριση επιρροής, εντόπισε τους top 5 influencers για το θέμα "{topic}" 
        στον κλάδο "{industry}". Για κάθε influencer, περιέγραψε:

        1. Όνομα
        2. Ειδικότητα
        3. Ακολουθίες (πλατφόρμες)
        4. Engagement Rate

        Μορφή:
        ΟΝΟΜΑ: [όνομα]
        ΕΙΔΙΚΟΤΗΤΑ: [ειδικότητα]
        ΠΛΑΤΦΟΡΜΕΣ: [πλατφόρμες]
        ENGAGEMENT: [ποσοστό]
        ---
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_influencers(response.choices[0].message.content)
        except Exception as e:
            return [{"error": f"Σφάλμα αναζήτησης influencers: {e}"}]
    
    def _suggest_collaboration_strategies(self, topic: str) -> List[str]:
        """Προτείνει συνεργασίες με influencers"""
        prompt = f"""
        Ως digital strategist, πρότεινε 5 στρατηγικές συνεργασίας για το θέμα "{topic}" 
        με influencers.

        Εστίασε σε:
        - Δημιουργία Περιεχομένου
        - Εκδηλώσεις και Διαγωνισμοί
        - Κοινά Projects
        - Καμπάνιες Κοινωνικής Ευθύνης
        - Χορηγούμενο Περιεχόμενο

        Μία στρατηγική ανά γραμμή με σύντομη περιγραφή.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                    if line.strip() and len(line.strip()) > 10]
        except Exception as e:
            return [f"Σφάλμα συνεργασιών: {e}"]
    
    def _parse_influencers(self, text: str) -> List[Dict[str, str]]:
        """Αναλύει λίστα influencers από το κείμενο"""
        influencers = []
        current_influencer = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('ΟΝΟΜΑ:'):
                if current_influencer:
                    influencers.append(current_influencer)
                current_influencer = {'name': line.replace('ΟΝΟΜΑ:', '').strip()}
            elif line.startswith('ΕΙΔΙΚΟΤΗΤΑ:'):
                current_influencer['specialty'] = line.replace('ΕΙΔΙΚΟΤΗΤΑ:', '').strip()
            elif line.startswith('ΠΛΑΤΦΟΡΜΕΣ:'):
                current_influencer['platforms'] = line.replace('ΠΛΑΤΦΟΡΜΕΣ:', '').strip()
            elif line.startswith('ENGAGEMENT:'):
                current_influencer['engagement'] = line.replace('ENGAGEMENT:', '').strip()
            elif line.startswith('---') and current_influencer:
                influencers.append(current_influencer)
                current_influencer = {}
        
        if current_influencer:
            influencers.append(current_influencer)
        
        return influencers




