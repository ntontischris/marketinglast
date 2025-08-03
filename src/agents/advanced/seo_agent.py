import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

load_dotenv()

class SEOAgent(BaseAgent):
    """
    Προηγμένος Πράκτορας SEO για Βελτιστοποίηση Περιεχομένου
    Αναλύει και βελτιστοποιεί το περιεχόμενο για μηχανές αναζήτησης
    """
    
    def __init__(self):
        super().__init__(name="Πράκτορας SEO και Βελτιστοποίησης")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        
        # Configure Groq API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY δεν βρέθηκε στο .env αρχείο")
        self.client = Groq(api_key=api_key)
        
        print(f"'{self.name}' αρχικοποιήθηκε με μοντέλο: {self.model_name}")
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Αναλύει και βελτιστοποιεί το περιεχόμενο για SEO
        """
        content = state.get("final_content", "")
        topic = state.get("topic", "")
        
        if not content:
            return {**state, "seo_analysis": "Δεν υπάρχει περιεχόμενο για ανάλυση SEO"}
        
        print(f"-- '{self.name}' αναλύει το περιεχόμενο για SEO... --")
        
        # Ανάλυση SEO
        seo_analysis = self._analyze_seo(content, topic)
        keyword_suggestions = self._suggest_keywords(content, topic)
        meta_data = self._generate_metadata(content, topic)
        optimization_tips = self._get_optimization_tips(content)
        
        seo_report = {
            "seo_score": seo_analysis,
            "keyword_suggestions": keyword_suggestions,
            "meta_data": meta_data,
            "optimization_tips": optimization_tips,
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {**state, "seo_analysis": seo_report}
    
    def _analyze_seo(self, content: str, topic: str) -> Dict[str, Any]:
        """Αναλύει την SEO απόδοση του περιεχομένου"""
        prompt = f"""
        Είσαι ειδικός SEO. Αξιολόγησε το παρακάτω περιεχόμενο για το θέμα "{topic}":

        ΠΕΡΙΕΧΟΜΕΝΟ:
        {content}

        Δώσε αναλυτική αξιολόγηση για:
        1. SEO Score (0-100)
        2. Πυκνότητα λέξεων-κλειδιών
        3. Δομή περιεχομένου
        4. Αναγνωσιμότητα
        5. Βελτιώσεις που χρειάζονται

        Απάντησε στα ελληνικά με συγκεκριμένες προτάσεις.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "score": self._extract_seo_score(response.choices[0].message.content)
            }
        except Exception as e:
            return {"error": f"Σφάλμα ανάλυσης SEO: {e}"}
    
    def _suggest_keywords(self, content: str, topic: str) -> List[str]:
        """Προτείνει λέξεις-κλειδιά"""
        prompt = f"""
        Ως ειδικός SEO, πρότεινε 10 λέξεις-κλειδιά για το θέμα "{topic}" βασισμένες στο περιεχόμενο:

        {content}

        Συμπεριέλαβε:
        - Κύριες λέξεις-κλειδιά (3-4)
        - Δευτερεύουσες λέξεις-κλειδιά (3-4)
        - Long-tail keywords (3-4)

        Δώσε μόνο τη λίστα, μία λέξη-κλειδί ανά γραμμή.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            keywords = [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                        if line.strip() and not line.strip().startswith('-')]
            return keywords[:10]
        except Exception as e:
            return [f"Σφάλμα λέξεων-κλειδιών: {e}"]
    
    def _generate_metadata(self, content: str, topic: str) -> Dict[str, str]:
        """Δημιουργεί metadata για SEO"""
        prompt = f"""
        Δημιούργησε SEO metadata για το θέμα "{topic}" και περιεχόμενο:

        {content[:200]}...

        Δημιούργησε:
        1. Title tag (μέχρι 60 χαρακτήρες)
        2. Meta description (μέχρι 160 χαρακτήρες)
        3. Meta keywords (5-8 λέξεις)

        Μορφή απάντησης:
        TITLE: [τίτλος]
        DESCRIPTION: [περιγραφή]
        KEYWORDS: [λέξεις-κλειδιά]
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_metadata(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Σφάλμα metadata: {e}"}
    
    def _get_optimization_tips(self, content: str) -> List[str]:
        """Παρέχει συμβουλές βελτιστοποίησης"""
        prompt = f"""
        Ως SEO consultant, δώσε 5 συγκεκριμένες συμβουλές για βελτίωση του περιεχομένου:

        {content}

        Εστίασε σε:
        - Δομή κειμένου
        - Λέξεις-κλειδιά
        - Εσωτερικούς συνδέσμους
        - User experience
        - Τεχνικό SEO

        Μία συμβουλή ανά γραμμή.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            tips = [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                   if line.strip() and len(line.strip()) > 10]
            return tips[:5]
        except Exception as e:
            return [f"Σφάλμα συμβουλών: {e}"]
    
    def _extract_seo_score(self, text: str) -> int:
        """Εξάγει το SEO score από το κείμενο"""
        import re
        score_match = re.search(r'(\d+)(?:/100|\%|)', text)
        if score_match:
            return min(int(score_match.group(1)), 100)
        return 75  # Default score
    
    def _parse_metadata(self, text: str) -> Dict[str, str]:
        """Εξάγει metadata από το κείμενο"""
        metadata = {}
        lines = text.split('\n')
        
        for line in lines:
            if line.startswith('TITLE:'):
                metadata['title'] = line.replace('TITLE:', '').strip()
            elif line.startswith('DESCRIPTION:'):
                metadata['description'] = line.replace('DESCRIPTION:', '').strip()
            elif line.startswith('KEYWORDS:'):
                metadata['keywords'] = line.replace('KEYWORDS:', '').strip()
        
        return metadata
