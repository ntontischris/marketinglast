"""
Enhanced Trend Analysis Agent with unified architecture
"""

import os
import re
import asyncio
from typing import Dict, Any, List
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent, AgentConfig

load_dotenv()

class EnhancedTrendAnalysisAgent(EnhancedBaseAgent):
    """
    Enhanced trend analysis agent with improved error handling and metrics
    """
    
    def __init__(self, config: AgentConfig = None):
        super().__init__("Enhanced Trend Analysis Agent", config)
        
        # Initialize Groq client
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
            
        self.client = Groq(api_key=self.api_key)
        self.logger.info("Enhanced Trend Analysis Agent initialized successfully")
    
    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Core trend analysis logic"""
        topic = state.get("topic")
        
        if not topic:
            raise ValueError("Topic not provided in state")
        
        self.logger.info(f"Analyzing trends for topic: {topic}")
        
        # Generate comprehensive trend analysis
        trend_report = await self._generate_trend_analysis(topic)
        
        # Extract structured insights
        insights = self._extract_insights(trend_report)
        
        return {
            **state,
            "trend_analysis_report": trend_report,
            "trend_insights": insights,
            "analysis_timestamp": self.metrics.last_execution.isoformat()
        }
    
    async def _generate_trend_analysis(self, topic: str) -> str:
        """Generate detailed trend analysis using Groq API"""
        
        prompt = f"""
        You are a world-class marketing and social media analyst specializing in trend analysis.
        
        Analyze the topic: "{topic}"
        
        Provide a comprehensive trend analysis in Greek with the following structure:
        
        ## 📊 Τρέχουσες Τάσεις
        Identify 3-5 key current trends related to this topic
        
        ## 🔮 Αναδυόμενες Τάσεις  
        Predict 2-3 emerging trends that will gain traction
        
        ## 📅 Εποχιακά Μοτίβα
        Describe seasonal patterns and optimal timing opportunities
        
        ## 🎯 Ευκαιρίες Περιεχομένου
        Suggest 5-7 specific content formats and ideas based on trends
        
        ## 📈 Μετρήσεις Επιτυχίας
        Key metrics to track for trend-based content
        
        ## ⚠️ Προειδοποιήσεις
        Potential risks or declining trends to avoid
        
        Make the analysis actionable, specific, and data-driven. Use bullet points and clear formatting.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            raw_content = response.choices[0].message.content
            
            # Clean the response
            cleaned_content = self._clean_response(raw_content)
            return cleaned_content
            
        except Exception as e:
            self.logger.error(f"Failed to generate trend analysis: {str(e)}")
            raise
    
    def _clean_response(self, text: str) -> str:
        """Clean and format the API response"""
        # Remove thinking tags if present
        if "</think>" in text:
            text = text.split("</think>", 1)[1].strip()
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _extract_insights(self, report: str) -> Dict[str, Any]:
        """Extract structured insights from trend report"""
        
        insights = {
            "trend_count": 0,
            "opportunity_count": 0,
            "risk_count": 0,
            "key_themes": [],
            "recommended_formats": []
        }
        
        # Simple extraction based on patterns
        lines = report.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-'):
                if any(keyword in line.lower() for keyword in ['trend', 'τάση']):
                    insights["trend_count"] += 1
                elif any(keyword in line.lower() for keyword in ['ευκαιρία', 'opportunity']):
                    insights["opportunity_count"] += 1
                elif any(keyword in line.lower() for keyword in ['risk', 'κίνδυνος', 'προειδοποίηση']):
                    insights["risk_count"] += 1
        
        return insights
    
    async def get_trend_summary(self, topic: str) -> Dict[str, Any]:
        """Get quick trend summary for dashboard display"""
        
        state = {"topic": topic}
        result = await self.execute_with_metrics(state)
        
        return {
            "topic": topic,
            "insights": result.get("trend_insights", {}),
            "report": result.get("trend_analysis_report", ""),
            "metrics": self.get_metrics()
        }

# Example usage and testing
async def test_enhanced_trend_agent():
    """Test the enhanced trend analysis agent"""
    
    agent = EnhancedTrendAnalysisAgent(
        AgentConfig(
            temperature=0.7,
            max_tokens=1500,
            timeout=45
        )
    )
    
    test_topics = [
        "Sustainable Fashion",
        "AI in Marketing",
        "Remote Work Trends"
    ]
    
    for topic in test_topics:
        print(f"\n{'='*50}")
        print(f"Testing topic: {topic}")
        print('='*50)
        
        try:
            result = await agent.get_trend_summary(topic)
            print(f"Trends found: {result['insights']['trend_count']}")
            print(f"Opportunities: {result['insights']['opportunity_count']}")
            print(f"Report preview: {result['report'][:200]}...")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_trend_agent())
