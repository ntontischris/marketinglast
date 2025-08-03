import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

load_dotenv()

class CompetitorAnalysisAgent(BaseAgent):
    """
    Πράκτορας Ανάλυσης Ανταγωνισμού
    Αναλύει τον ανταγωνισμό και προτείνει στρατηγικές διαφοροποίησης
    """
    
    def __init__(self):
        super().__init__(name="Πράκτορας Ανάλυσης Ανταγωνισμού")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        
        # Configure Groq API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY δεν βρέθηκε στο .env αρχείο")
        self.client = Groq(api_key=api_key)
        
        print(f"'{self.name}' αρχικοποιήθηκε με μοντέλο: {self.model_name}")
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Αναλύει τον ανταγωνισμό και προτείνει στρατηγικές
        """
        topic = state.get("topic", "")
        industry = state.get("user_profile", {}).get("industry", "γενικό")
        content = state.get("final_content", "")
        
        if not topic:
            return {**state, "competitor_analysis": "Δεν υπάρχει θέμα για ανάλυση ανταγωνισμού"}
        
        print(f"-- '{self.name}' αναλύει τον ανταγωνισμό για '{topic}'... --")
        
        # Ανάλυση ανταγωνισμού
        market_analysis = self._analyze_market(topic, industry)
        competitor_strategies = self._identify_competitor_strategies(topic, industry)
        differentiation_opportunities = self._find_differentiation_opportunities(topic, content, industry)
        competitive_positioning = self._suggest_competitive_positioning(topic, content)
        
        competitor_report = {
            "market_analysis": market_analysis,
            "competitor_strategies": competitor_strategies,
            "differentiation_opportunities": differentiation_opportunities,
            "competitive_positioning": competitive_positioning,
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {**state, "competitor_analysis": competitor_report}
    
    def _analyze_market(self, topic: str, industry: str) -> Dict[str, Any]:
        """Αναλύει την αγορά και τον ανταγωνισμό"""
        prompt = f"""
        Είσαι ειδικός market research. Αναλύοις την αγορά για το θέμα "{topic}" στον κλάδο "{industry}".

        Παρέχε ανάλυση για:
        1. Μέγεθος αγοράς και τάσεις
        2. Κύριοι ανταγωνιστές (5-7)
        3. Δυνάμεις και αδυναμίες ανταγωνιστών
        4. Ευκαιρίες στην αγορά
        5. Απειλές και προκλήσεις

        Απάντησε στα ελληνικά με αναλυτικές πληροφορίες.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "market_size": self._extract_market_insights(response.choices[0].message.content)
            }
        except Exception as e:
            return {"error": f"Σφάλμα ανάλυσης αγοράς: {e}"}
    
    def _identify_competitor_strategies(self, topic: str, industry: str) -> List[Dict[str, str]]:
        """Εντοπίζει στρατηγικές ανταγωνιστών"""
        prompt = f"""
        Ως strategic analyst, εντόπισε τις κύριες στρατηγικές που χρησιμοποιούν οι ανταγωνιστές 
        στο θέμα "{topic}" στον κλάδο "{industry}".

        Για κάθε στρατηγική δώσε:
        - Όνομα στρατηγικής
        - Περιγραφή (2-3 γραμμές)
        - Ποιοι την χρησιμοποιούν
        - Αποτελεσματικότητα (Υψηλή/Μεσαία/Χαμηλή)

        Μορφή:
        ΣΤΡΑΤΗΓΙΚΗ: [όνομα]
        ΠΕΡΙΓΡΑΦΗ: [περιγραφή]
        ΧΡΗΣΤΕΣ: [εταιρείες]
        ΑΠΟΤΕΛΕΣΜΑΤΙΚΟΤΗΤΑ: [επίπεδο]
        ---
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_strategies(response.choices[0].message.content)
        except Exception as e:
            return [{"error": f"Σφάλμα στρατηγικών: {e}"}]
    
    def _find_differentiation_opportunities(self, topic: str, content: str, industry: str) -> List[str]:
        """Βρίσκει ευκαιρίες διαφοροποίησης"""
        prompt = f"""
        Ως innovation consultant, εντόπισε 7 ευκαιρίες διαφοροποίησης για το θέμα "{topic}" 
        στον κλάδο "{industry}" βασισμένες στο περιεχόμενό μας:

        ΠΕΡΙΕΧΟΜΕΝΟ ΜΑΣ:
        {content}

        Εστίασε σε:
        - Μοναδικές προσεγγίσεις
        - Ανεκμετάλλευτα κομμάτια αγοράς
        - Τεχνολογικές καινοτομίες
        - Εμπειρία χρήστη
        - Τιμολογιακές στρατηγικές
        - Κανάλια διανομής
        - Brand positioning

        Μία ευκαιρία ανά γραμμή με σύντομη εξήγηση.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            opportunities = [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                           if line.strip() and len(line.strip()) > 15]
            return opportunities[:7]
        except Exception as e:
            return [f"Σφάλμα ευκαιριών: {e}"]
    
    def _suggest_competitive_positioning(self, topic: str, content: str) -> Dict[str, str]:
        """Προτείνει ανταγωνιστική τοποθέτηση"""
        prompt = f"""
        Ως brand strategist, πρότεινε ανταγωνιστική τοποθέτηση για το θέμα "{topic}" 
        βασισμένη στο περιεχόμενό μας:

        {content}

        Δημιούργησε:
        1. Unique Value Proposition (1 γραμμή)
        2. Key Differentiators (3 σημεία)
        3. Target Position (σε τι θέλουμε να είμαστε #1)
        4. Competitive Advantage (η μεγαλύτερη δύναμή μας)
        5. Brand Promise (τι υπόσχεται το brand μας)

        Μορφή:
        UVP: [πρόταση αξίας]
        DIFFERENTIATORS: [διαφοροποιητές]
        POSITION: [θέση]
        ADVANTAGE: [πλεονέκτημα]
        PROMISE: [υπόσχεση]
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_positioning(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Σφάλμα positioning: {e}"}
    
    def _extract_market_insights(self, text: str) -> Dict[str, str]:
        """Εξάγει βασικές πληροφορίες αγοράς"""
        insights = {}
        lines = text.split('\n')
        
        for line in lines:
            if 'μέγεθος' in line.lower() or 'αγορά' in line.lower():
                insights['market_size'] = line.strip()
            elif 'τάση' in line.lower() or 'trend' in line.lower():
                insights['trends'] = line.strip()
        
        return insights
    
    def _parse_strategies(self, text: str) -> List[Dict[str, str]]:
        """Εξάγει στρατηγικές από το κείμενο"""
        strategies = []
        current_strategy = {}
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('ΣΤΡΑΤΗΓΙΚΗ:'):
                if current_strategy:
                    strategies.append(current_strategy)
                current_strategy = {'name': line.replace('ΣΤΡΑΤΗΓΙΚΗ:', '').strip()}
            elif line.startswith('ΠΕΡΙΓΡΑΦΗ:'):
                current_strategy['description'] = line.replace('ΠΕΡΙΓΡΑΦΗ:', '').strip()
            elif line.startswith('ΧΡΗΣΤΕΣ:'):
                current_strategy['users'] = line.replace('ΧΡΗΣΤΕΣ:', '').strip()
            elif line.startswith('ΑΠΟΤΕΛΕΣΜΑΤΙΚΟΤΗΤΑ:'):
                current_strategy['effectiveness'] = line.replace('ΑΠΟΤΕΛΕΣΜΑΤΙΚΟΤΗΤΑ:', '').strip()
            elif line == '---' and current_strategy:
                strategies.append(current_strategy)
                current_strategy = {}
        
        if current_strategy:
            strategies.append(current_strategy)
        
        return strategies
    
    def _parse_positioning(self, text: str) -> Dict[str, str]:
        """Εξάγει positioning από το κείμενο"""
        positioning = {}
        lines = text.split('\n')
        
        for line in lines:
            if line.startswith('UVP:'):
                positioning['uvp'] = line.replace('UVP:', '').strip()
            elif line.startswith('DIFFERENTIATORS:'):
                positioning['differentiators'] = line.replace('DIFFERENTIATORS:', '').strip()
            elif line.startswith('POSITION:'):
                positioning['position'] = line.replace('POSITION:', '').strip()
            elif line.startswith('ADVANTAGE:'):
                positioning['advantage'] = line.replace('ADVANTAGE:', '').strip()
            elif line.startswith('PROMISE:'):
                positioning['promise'] = line.replace('PROMISE:', '').strip()
        
        return positioning
