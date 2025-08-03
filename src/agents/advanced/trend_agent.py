import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

load_dotenv()

class TrendAnalysisAgent(BaseAgent):
    """
    Πράκτορας Ανάλυσης Τάσεων
    Εντοπίζει και αναλύει τρέχουσες τάσεις στο marketing και social media
    """
    
    def __init__(self):
        super().__init__(name="Πράκτορας Ανάλυσης Τάσεων")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY δεν βρέθηκε στο .env αρχείο")
        self.client = Groq(api_key=api_key)
        
        print(f"'{self.name}' αρχικοποιήθηκε με το μοντέλο: {self.model_name}")
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Αναλύει τάσεις και προτείνει στρατηγικές
        """
        topic = state.get("topic", "")
        industry = state.get("user_profile", {}).get("industry", "γενικό")
        
        if not topic:
            return {**state, "trend_analysis": "Δεν υπάρχει θέμα για ανάλυση τάσεων"}
        
        print(f"-- '{self.name}' αναλύει τάσεις για το θέμα '{topic}'... --")
        
        current_trends = self._identify_current_trends(topic, industry)
        emerging_trends = self._predict_emerging_trends(topic, industry)
        seasonal_patterns = self._analyze_seasonal_patterns(topic)
        trend_opportunities = self._find_trend_opportunities(topic, current_trends)
        
        trend_report = {
            "current_trends": current_trends,
            "emerging_trends": emerging_trends,
            "seasonal_patterns": seasonal_patterns,
            "trend_opportunities": trend_opportunities,
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {**state, "trend_analysis": trend_report}
    
    def _identify_current_trends(self, topic: str, industry: str) -> List[Dict[str, str]]:
        """Εντοπίζει τρέχουσες τάσεις"""
        prompt = f"""
        Ως trend analyst, εντόπισε τις 5 κυριότερες τάσεις για το θέμα "{topic}" 
        στον κλάδο "{industry}" για το 2025.

        Για κάθε τάση δώσε:
        - Όνομα τάσης
        - Περιγραφή (2-3 γραμμές)
        - Επίπεδο υιοθέτησης (Αρχική/Αναπτυσσόμενη/Ώριμη)
        - Πλατφόρμες όπου είναι δημοφιλής

        Μορφή:
        ΤΑΣΗ: [όνομα]
        ΠΕΡΙΓΡΑΦΗ: [περιγραφή]
        ΕΠΙΠΕΔΟ: [επίπεδο]
        ΠΛΑΤΦΟΡΜΕΣ: [πλατφόρμες]
        ---
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_trends(response.choices[0].message.content)
        except Exception as e:
            return [{"error": f"Σφάλμα ανάλυσης τάσεων: {e}"}]
    
    def _predict_emerging_trends(self, topic: str, industry: str) -> List[str]:
        """Προβλέπει αναδυόμενες τάσεις"""
        prompt = f"""
        Ως futurist και trend forecaster, πρόβλεψε 5 αναδυόμενες τάσεις 
        για το θέμα "{topic}" στον κλάδο "{industry}" για τους επόμενους 6-12 μήνες.

        Εστίασε σε:
        - Τεχνολογικές καινοτομίες
        - Αλλαγές στη συμπεριφορά καταναλωτών
        - Νέες πλατφόρμες και εργαλεία
        - Αλλαγές στο regulatory περιβάλλον
        - Κοινωνικές και πολιτιστικές μεταβολές

        Μία τάση ανά γραμμή με σύντομη εξήγηση.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            trends = [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                     if line.strip() and len(line.strip()) > 15]
            return trends[:5]
        except Exception as e:
            return [f"Σφάλμα πρόβλεψης τάσεων: {e}"]
    
    def _analyze_seasonal_patterns(self, topic: str) -> Dict[str, str]:
        """Αναλύει εποχιακά μοτίβα"""
        prompt = f"""
        Ως seasonality expert, αναλύε τα εποχιακά μοτίβα για το θέμα "{topic}".

        Δώσε ανάλυση για:
        1. Άνοιξη (Μάρτιος-Μάιος)
        2. Καλοκαίρι (Ιούνιος-Αύγουστος)
        3. Φθινόπωρο (Σεπτέμβριος-Νοέμβριος)
        4. Χειμώνας (Δεκέμβριος-Φεβρουάριος)

        Για κάθε εποχή περίγραψε:
        - Επίπεδο ενδιαφέροντος (Υψηλό/Μεσαίο/Χαμηλό)
        - Κύριες ευκαιρίες
        - Προτεινόμενες στρατηγικές

        Μορφή:
        ΆΝΟΙΞΗ: [ανάλυση]
        ΚΑΛΟΚΑΊΡΙ: [ανάλυση]
        ΦΘΙΝΌΠΩΡΟ: [ανάλυση]
        ΧΕΙΜΏΝΑΣ: [ανάλυση]
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            return self._parse_seasonal_patterns(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Σφάλμα εποχιακής ανάλυσης: {e}"}
    
    def _find_trend_opportunities(self, topic: str, current_trends: List[Dict[str, str]]) -> List[str]:
        """Εντοπίζει ευκαιρίες από τάσεις"""
        trends_text = "\n".join([f"- {trend.get('name', ''): {trend.get('description', '')}}" 
                                for trend in current_trends if isinstance(trend, dict)])
        
        prompt = f"""
        Ως opportunity spotter, εντόπισε 5 συγκεκριμένες ευκαιρίες για το θέμα "{topic}" 
        βασισμένες στις τρέχουσες τάσεις:

        ΤΡΕΧΟΥΣΕΣ ΤΑΣΕΙΣ:
        {trends_text}

        Για κάθε ευκαιρία δώσε:
        - Περιγραφή ευκαιρίας
        - Πώς να την εκμεταλλευτούμε
        - Χρονικό πλαίσιο υλοποίησης

        Μία ευκαιρία ανά γραμμή.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            opportunities = [line.strip() for line in response.choices[0].message.content.strip().split('\n') 
                           if line.strip() and len(line.strip()) > 20]
            return opportunities[:5]
        except Exception as e:
            return [f"Σφάλμα ευκαιριών: {e}"]
    
    def _parse_trends(self, text: str) -> List[Dict[str, str]]:
        """Εξάγει τάσεις από το κείμενο"""
        trends = []
        current_trend = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('ΤΑΣΗ:'):
                if current_trend:
                    trends.append(current_trend)
                current_trend = {'name': line.replace('ΤΑΣΗ:', '').strip()}
            elif line.startswith('ΠΕΡΙΓΡΑΦΗ:'):
                current_trend['description'] = line.replace('ΠΕΡΙΓΡΑΦΗ:', '').strip()
            elif line.startswith('ΕΠΙΠΕΔΟ:'):
                current_trend['level'] = line.replace('ΕΠΙΠΕΔΟ:', '').strip()
            elif line.startswith('ΠΛΑΤΦΟΡΜΕΣ:'):
                current_trend['platforms'] = line.replace('ΠΛΑΤΦΟΡΜΕΣ:', '').strip()
            elif line.startswith('---') and current_trend:
                trends.append(current_trend)
                current_trend = {}
        
        if current_trend:
            trends.append(current_trend)
        
        return trends
    
    def _parse_seasonal_patterns(self, text: str) -> Dict[str, str]:
        """Εξάγει εποχιακά μοτίβα από το κείμενο"""
        patterns = {}
        
        for line in text.split('\n'):
            if line.startswith('ΆΝΟΙΞΗ:'):
                patterns['spring'] = line.replace('ΆΝΟΙΞΗ:', '').strip()
            elif line.startswith('ΚΑΛΟΚΑΊΡΙ:'):
                patterns['summer'] = line.replace('ΚΑΛΟΚΑΊΡΙ:', '').strip()
            elif line.startswith('ΦΘΙΝΌΠΩΡΟ:'):
                patterns['autumn'] = line.replace('ΦΘΙΝΌΠΩΡΟ:', '').strip()
            elif line.startswith('ΧΕΙΜΏΝΑΣ:'):
                patterns['winter'] = line.replace('ΧΕΙΜΏΝΑΣ:', '').strip()
        
        return patterns
