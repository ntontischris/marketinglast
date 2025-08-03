"""
Enhanced Content Strategy Agent with unified architecture
"""

import os
import re
import asyncio
from typing import Dict, Any, List
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent, AgentConfig

load_dotenv()

class EnhancedContentStrategyAgent(EnhancedBaseAgent):
    """
    Enhanced content strategy agent with trend integration and advanced planning
    """
    
    def __init__(self, config: AgentConfig = None):
        super().__init__("Enhanced Content Strategy Agent", config)
        
        # Initialize Groq client
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
            
        self.client = Groq(api_key=self.api_key)
        self.logger.info("Enhanced Content Strategy Agent initialized successfully")
    
    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Core content strategy logic with trend integration"""
        topic = state.get("topic")
        trend_analysis = state.get("trend_analysis_report", "")
        target_audience = state.get("target_audience", "general")
        content_goals = state.get("content_goals", ["engagement", "brand_awareness"])
        
        if not topic:
            raise ValueError("Topic not provided in state")
        
        self.logger.info(f"Creating content strategy for: {topic}")
        
        # Generate comprehensive content strategy
        strategy = await self._generate_content_strategy(
            topic, trend_analysis, target_audience, content_goals
        )
        
        # Create content calendar
        content_calendar = await self._create_content_calendar(strategy)
        
        # Generate campaign brief
        campaign_brief = await self._create_campaign_brief(
            topic, strategy, content_calendar
        )
        
        return {
            **state,
            "content_strategy": strategy,
            "content_calendar": content_calendar,
            "campaign_brief": campaign_brief,
            "strategy_timestamp": self.metrics.last_execution.isoformat()
        }
    
    async def _generate_content_strategy(self, topic: str, trends: str, 
                                     audience: str, goals: List[str]) -> Dict[str, Any]:
        """Generate comprehensive content strategy"""
        
        prompt = f"""
        You are a world-class content strategist with expertise in data-driven marketing.
        
        Create a comprehensive content strategy for:
        Topic: {topic}
        Target Audience: {audience}
        Goals: {', '.join(goals)}
        
        {f"Trend Analysis Context:\n{trends}" if trends else ""}
        
        Structure your response as:
        
        ## 🎯 Στρατηγική Στόχευσης
        - Primary audience personas
        - Key messaging pillars
        - Brand voice guidelines
        
        ## 📋 Content Pillars
        5-7 distinct content themes with:
        - Description and purpose
        - Content formats for each
        - Posting frequency recommendations
        
        ## 🎨 Content Formats & Channels
        - Platform-specific recommendations
        - Format mix (video, carousel, stories, etc.)
        - Optimal posting times
        
        ## 📊 KPIs & Metrics
        - Success metrics for each goal
        - Benchmark targets
        - Tracking methodology
        
        ## 🔄 Content Lifecycle
        - Creation workflow
        - Approval process
        - Repurposing strategy
        
        Make it actionable, specific, and tailored to Greek audiences.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            strategy_text = response.choices[0].message.content
            cleaned_strategy = self._clean_response(strategy_text)
            
            # Parse into structured format
            return self._parse_strategy(cleaned_strategy)
            
        except Exception as e:
            self.logger.error(f"Failed to generate content strategy: {str(e)}")
            raise
    
    async def _create_content_calendar(self, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a 30-day content calendar based on strategy"""
        
        prompt = f"""
        Based on the following content strategy:
        {strategy.get('raw_text', '')}
        
        Create a 30-day content calendar with:
        - Daily content ideas (mix of formats)
        - Platform recommendations
        - Key themes rotation
        - Special dates/holidays consideration
        
        Format as a structured list with:
        Day | Content Type | Platform | Theme | Brief Description
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.config.model_name,
                temperature=0.6,
                max_tokens=2000
            )
            
            calendar_text = response.choices[0].message.content
            return self._parse_calendar(calendar_text)
            
        except Exception as e:
            self.logger.error(f"Failed to create content calendar: {str(e)}")
            return []
    
    async def _create_campaign_brief(self, topic: str, strategy: Dict[str, Any], 
                                   calendar: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create comprehensive campaign brief"""
        
        return {
            "campaign_name": f"{topic} Content Campaign",
            "duration": "30 days",
            "objectives": strategy.get("objectives", []),
            "target_audience": strategy.get("target_audience", "general"),
            "key_messages": strategy.get("key_messages", []),
            "content_pillars": strategy.get("content_pillars", []),
            "total_posts": len(calendar),
            "estimated_reach": self._estimate_reach(calendar),
            "budget_allocation": self._suggest_budget(strategy)
        }
    
    def _parse_strategy(self, strategy_text: str) -> Dict[str, Any]:
        """Parse strategy text into structured format"""
        
        sections = {
            "raw_text": strategy_text,
            "objectives": [],
            "target_audience": "",
            "content_pillars": [],
            "platforms": [],
            "kpis": [],
            "workflow": ""
        }
        
        # Simple parsing based on headers
        lines = strategy_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('##'):
                current_section = line.lower()
            elif line.startswith('-') or line.startswith('•'):
                content = line[1:].strip()
                
                if 'στόχευσης' in str(current_section):
                    sections["objectives"].append(content)
                elif 'pillars' in str(current_section) or 'θέματα' in str(current_section):
                    sections["content_pillars"].append(content)
                elif 'platforms' in str(current_section) or 'κανάλια' in str(current_section):
                    sections["platforms"].append(content)
                elif 'kpi' in str(current_section) or 'μετρήσεις' in str(current_section):
                    sections["kpis"].append(content)
        
        return sections
    
    def _parse_calendar(self, calendar_text: str) -> List[Dict[str, Any]]:
        """Parse calendar text into structured format"""
        
        calendar = []
        lines = calendar_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if '|' in line and not line.startswith('Day'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:
                    calendar.append({
                        "day": parts[0],
                        "type": parts[1],
                        "platform": parts[2],
                        "theme": parts[3],
                        "description": parts[4]
                    })
        
        return calendar
    
    def _estimate_reach(self, calendar: List[Dict[str, Any]]) -> Dict[str, int]:
        """Estimate potential reach based on content calendar"""
        
        total_posts = len(calendar)
        estimated_reach = total_posts * 1000  # Conservative estimate
        
        return {
            "total_posts": total_posts,
            "estimated_reach": estimated_reach,
            "estimated_engagement": int(estimated_reach * 0.05)  # 5% engagement rate
        }
    
    def _suggest_budget(self, strategy: Dict[str, Any]) -> Dict[str, float]:
        """Suggest budget allocation based on strategy"""
        
        platforms = strategy.get("platforms", [])
        total_budget = 1000  # Base budget
        
        allocation = {}
        if platforms:
            per_platform = total_budget / len(platforms)
            for platform in platforms:
                allocation[platform] = per_platform
        
        return {
            "total": total_budget,
            "allocation": allocation,
            "breakdown": {
                "content_creation": total_budget * 0.4,
                "promotion": total_budget * 0.5,
                "tools": total_budget * 0.1
            }
        }
    
    def _clean_response(self, text: str) -> str:
        """Clean and format API response"""
        if "</think>" in text:
            text = text.split("</think>", 1)[1].strip()
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    async def get_strategy_summary(self, topic: str, **kwargs) -> Dict[str, Any]:
        """Get quick strategy summary for dashboard"""
        
        state = {
            "topic": topic,
            **kwargs
        }
        
        result = await self.execute_with_metrics(state)
        
        return {
            "topic": topic,
            "strategy": result.get("content_strategy", {}),
            "calendar_length": len(result.get("content_calendar", [])),
            "campaign_brief": result.get("campaign_brief", {}),
            "metrics": self.get_metrics()
        }

# Example usage
async def test_enhanced_strategy_agent():
    """Test the enhanced content strategy agent"""
    
    agent = EnhancedContentStrategyAgent(
        AgentConfig(
            temperature=0.7,
            max_tokens=2000,
            timeout=60
        )
    )
    
    test_topic = "Sustainable Fashion"
    
    try:
        result = await agent.get_strategy_summary(
            test_topic,
            target_audience="eco-conscious millennials",
            content_goals=["brand_awareness", "community_building", "sales"]
        )
        
        print(f"\n{'='*60}")
        print(f"Strategy Summary for: {test_topic}")
        print('='*60)
        print(f"Content Pillars: {len(result['strategy'].get('content_pillars', []))}")
        print(f"Calendar Posts: {result['calendar_length']}")
        print(f"Estimated Reach: {result['campaign_brief'].get('estimated_reach', {}).get('estimated_reach', 0)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_strategy_agent())
