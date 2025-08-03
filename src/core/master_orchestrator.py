"""
🧠 MASTER AI ORCHESTRATOR
========================

The ultimate AI conductor that manages all agents with human-like reasoning,
multi-agent conversations, and predictive campaign analysis.

This is the brain of the new AI Marketing System.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class AgentRole(Enum):
    CEO = "ceo"
    CMO = "cmo"
    CTO = "cto"
    CFO = "cfo"
    CREATIVE_DIRECTOR = "creative_director"
    CONTENT_MANAGER = "content_manager"
    PERFORMANCE_MANAGER = "performance_manager"
    BRAND_GUARDIAN = "brand_guardian"

@dataclass
class AgentPersonality:
    name: str
    role: AgentRole
    expertise: List[str]
    communication_style: str
    decision_making_approach: str
    key_concerns: List[str]

@dataclass
class ConversationMessage:
    agent: str
    message: str
    timestamp: datetime
    confidence: float
    reasoning: str
    suggested_actions: List[str]

class MasterAIOrchestrator:
    """
    The Master AI Orchestrator - Revolutionary AI system that coordinates
    multiple specialized agents through simulated conversations and human-like reasoning.
    """
    
    def __init__(self):
        self.client = self._initialize_groq_client()
        self.active_agents = {}
        self.conversation_history = []
        self.campaign_state = {}
        self.performance_metrics = {}
        
        # Initialize AI Agent Personalities
        self.agent_personalities = self._initialize_agent_personalities()
        
        print("🧠 Master AI Orchestrator initialized with advanced reasoning capabilities")
    
    def _initialize_groq_client(self) -> Groq:
        """Initialize Groq client with enhanced error handling"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please configure your .env file.")
        return Groq(api_key=api_key)
    
    def _initialize_agent_personalities(self) -> Dict[AgentRole, AgentPersonality]:
        """Create distinct AI personalities for each agent role"""
        return {
            AgentRole.CEO: AgentPersonality(
                name="Alexandra Sterling",
                role=AgentRole.CEO,
                expertise=["Strategic Vision", "Market Analysis", "ROI Optimization"],
                communication_style="Visionary, decisive, results-focused",
                decision_making_approach="Data-driven with intuitive insights",
                key_concerns=["Brand reputation", "Long-term growth", "Market positioning"]
            ),
            AgentRole.CMO: AgentPersonality(
                name="Marcus Chen",
                role=AgentRole.CMO,
                expertise=["Marketing Strategy", "Consumer Psychology", "Trend Analysis"],
                communication_style="Creative, enthusiastic, trend-aware",
                decision_making_approach="Consumer-centric with creative flair",
                key_concerns=["Audience engagement", "Brand awareness", "Campaign effectiveness"]
            ),
            AgentRole.CREATIVE_DIRECTOR: AgentPersonality(
                name="Sofia Rodriguez",
                role=AgentRole.CREATIVE_DIRECTOR,
                expertise=["Visual Design", "Brand Aesthetics", "Creative Campaigns"],
                communication_style="Artistic, passionate, detail-oriented",
                decision_making_approach="Aesthetics-first with strategic backing",
                key_concerns=["Visual impact", "Brand consistency", "Creative innovation"]
            ),
            AgentRole.PERFORMANCE_MANAGER: AgentPersonality(
                name="David Kim",
                role=AgentRole.PERFORMANCE_MANAGER,
                expertise=["Analytics", "Performance Optimization", "A/B Testing"],
                communication_style="Analytical, precise, data-focused",
                decision_making_approach="Evidence-based with predictive modeling",
                key_concerns=["Conversion rates", "Performance metrics", "ROI maximization"]
            )
        }
    
    async def simulate_strategic_meeting(self, campaign_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        🎭 Simulates a high-level strategic meeting between AI agents
        
        This is where the magic happens - AI agents actually "discuss" the campaign
        like a real marketing team would.
        """
        print(f"🎭 Initiating Strategic AI Meeting for: {campaign_brief.get('topic', 'New Campaign')}")
        
        meeting_participants = [
            AgentRole.CEO,
            AgentRole.CMO, 
            AgentRole.CREATIVE_DIRECTOR,
            AgentRole.PERFORMANCE_MANAGER
        ]
        
        # Phase 1: Individual Analysis
        individual_analyses = await self._gather_individual_analyses(campaign_brief, meeting_participants)
        
        # Phase 2: Collaborative Discussion
        discussion_flow = await self._simulate_collaborative_discussion(campaign_brief, individual_analyses)
        
        # Phase 3: Strategic Synthesis
        final_strategy = await self._synthesize_final_strategy(campaign_brief, discussion_flow)
        
        return {
            "campaign_brief": campaign_brief,
            "individual_analyses": individual_analyses,
            "discussion_flow": discussion_flow,
            "final_strategy": final_strategy,
            "meeting_timestamp": datetime.now().isoformat(),
            "participants": [role.value for role in meeting_participants]
        }
    
    async def _gather_individual_analyses(self, brief: Dict[str, Any], participants: List[AgentRole]) -> Dict[str, Dict]:
        """Each agent provides their individual perspective"""
        analyses = {}
        
        for role in participants:
            personality = self.agent_personalities[role]
            analysis = await self._get_agent_analysis(brief, personality)
            analyses[role.value] = analysis
            
        return analyses
    
    async def _get_agent_analysis(self, brief: Dict[str, Any], personality: AgentPersonality) -> Dict[str, Any]:
        """Get individual agent analysis based on their personality and expertise"""
        
        prompt = f"""
        You are {personality.name}, a {personality.role.value.replace('_', ' ').title()} with expertise in {', '.join(personality.expertise)}.
        
        Your communication style: {personality.communication_style}
        Your decision-making approach: {personality.decision_making_approach}
        Your key concerns: {', '.join(personality.key_concerns)}
        
        Analyze this campaign brief from your unique perspective:
        
        CAMPAIGN BRIEF:
        Topic: {brief.get('topic', 'Not specified')}
        Target Audience: {brief.get('target_audience', 'Not specified')}
        Budget: {brief.get('budget', 'Not specified')}
        Timeline: {brief.get('timeline', 'Not specified')}
        Goals: {brief.get('goals', 'Not specified')}
        
        Provide your analysis in this JSON format:
        {{
            "initial_reaction": "Your immediate thoughts on this brief",
            "key_opportunities": ["List 3-5 opportunities you see"],
            "potential_risks": ["List 2-3 risks or concerns"],
            "strategic_recommendations": ["List 3-5 specific recommendations"],
            "success_metrics": ["What metrics would you use to measure success"],
            "confidence_level": "High/Medium/Low and why",
            "next_steps": ["What should happen next"]
        }}
        
        Think like the expert you are. Be specific, actionable, and true to your personality.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.7
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse JSON, fallback to structured text if needed
            try:
                analysis_json = json.loads(analysis_text)
                return {
                    "agent": personality.name,
                    "role": personality.role.value,
                    "analysis": analysis_json,
                    "raw_response": analysis_text
                }
            except json.JSONDecodeError:
                return {
                    "agent": personality.name,
                    "role": personality.role.value,
                    "analysis": {"raw_analysis": analysis_text},
                    "raw_response": analysis_text
                }
                
        except Exception as e:
            return {
                "agent": personality.name,
                "role": personality.role.value,
                "analysis": {"error": f"Analysis failed: {str(e)}"},
                "raw_response": ""
            }
    
    async def _simulate_collaborative_discussion(self, brief: Dict[str, Any], analyses: Dict[str, Dict]) -> List[ConversationMessage]:
        """
        🗣️ Simulate a realistic discussion between agents
        This is where agents "respond" to each other's ideas
        """
        discussion = []
        
        # CEO kicks off the meeting
        ceo_opening = await self._generate_agent_response(
            AgentRole.CEO,
            f"Let's discuss this campaign: {brief.get('topic')}. I've reviewed everyone's analysis.",
            {"brief": brief, "all_analyses": analyses},
            discussion
        )
        discussion.append(ceo_opening)
        
        # CMO responds with marketing perspective
        cmo_response = await self._generate_agent_response(
            AgentRole.CMO,
            "From a marketing standpoint, I see some interesting opportunities here.",
            {"brief": brief, "previous_messages": discussion[-3:]},
            discussion
        )
        discussion.append(cmo_response)
        
        # Creative Director adds creative vision
        creative_response = await self._generate_agent_response(
            AgentRole.CREATIVE_DIRECTOR,
            "I'm visualizing some compelling creative directions for this campaign.",
            {"brief": brief, "previous_messages": discussion[-3:]},
            discussion
        )
        discussion.append(creative_response)
        
        # Performance Manager discusses metrics
        performance_response = await self._generate_agent_response(
            AgentRole.PERFORMANCE_MANAGER,
            "Let me address the analytics and performance expectations.",
            {"brief": brief, "previous_messages": discussion[-3:]},
            discussion
        )
        discussion.append(performance_response)
        
        # CEO synthesizes and makes decisions
        ceo_conclusion = await self._generate_agent_response(
            AgentRole.CEO,
            "Based on our discussion, here's what we're going to do.",
            {"brief": brief, "full_discussion": discussion},
            discussion
        )
        discussion.append(ceo_conclusion)
        
        return discussion
    
    async def _generate_agent_response(
        self, 
        role: AgentRole, 
        context: str, 
        data: Dict[str, Any],
        conversation_history: List[ConversationMessage]
    ) -> ConversationMessage:
        """Generate a realistic response from a specific agent"""
        
        personality = self.agent_personalities[role]
        
        # Build conversation context
        recent_messages = ""
        if conversation_history:
            recent_messages = "\n".join([
                f"{msg.agent}: {msg.message[:200]}..." 
                for msg in conversation_history[-3:]
            ])
        
        prompt = f"""
        You are {personality.name}, {personality.role.value.replace('_', ' ').title()}.
        
        Your personality: {personality.communication_style}
        Your expertise: {', '.join(personality.expertise)}
        Your concerns: {', '.join(personality.key_concerns)}
        
        CONTEXT: {context}
        
        RECENT CONVERSATION:
        {recent_messages}
        
        CAMPAIGN BRIEF: {data.get('brief', {})}
        
        Respond as {personality.name} would in a marketing strategy meeting. Be:
        - True to your personality and expertise
        - Specific and actionable
        - Collaborative but assertive about your domain
        - Under 150 words
        
        Your response:
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.8
            )
            
            message_content = response.choices[0].message.content.strip()
            
            return ConversationMessage(
                agent=personality.name,
                message=message_content,
                timestamp=datetime.now(),
                confidence=0.85,  # Could be calculated based on response quality
                reasoning=f"Response generated based on {role.value} expertise",
                suggested_actions=self._extract_action_items(message_content)
            )
            
        except Exception as e:
            return ConversationMessage(
                agent=personality.name,
                message=f"I need a moment to process this information. [Error: {str(e)}]",
                timestamp=datetime.now(),
                confidence=0.1,
                reasoning="Error in response generation",
                suggested_actions=[]
            )
    
    def _extract_action_items(self, message: str) -> List[str]:
        """Extract actionable items from agent messages"""
        # Simple extraction - could be enhanced with NLP
        action_keywords = ["should", "need to", "must", "recommend", "suggest", "propose"]
        actions = []
        
        sentences = message.split('. ')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                actions.append(sentence.strip())
        
        return actions[:3]  # Return top 3 actions
    
    async def _synthesize_final_strategy(self, brief: Dict[str, Any], discussion: List[ConversationMessage]) -> Dict[str, Any]:
        """
        🎯 Synthesize all agent discussions into a coherent final strategy
        """
        
        # Combine all agent insights
        all_messages = "\n\n".join([
            f"**{msg.agent}**: {msg.message}"
            for msg in discussion
        ])
        
        synthesis_prompt = f"""
        You are an AI Strategy Synthesizer. You've observed a strategic meeting between marketing experts.
        
        CAMPAIGN BRIEF:
        {json.dumps(brief, indent=2)}
        
        FULL DISCUSSION:
        {all_messages}
        
        Synthesize this into a comprehensive campaign strategy in this JSON format:
        {{
            "campaign_name": "Creative campaign name",
            "executive_summary": "2-3 sentence overview",
            "target_audience": {{
                "primary": "Main target segment",
                "secondary": "Secondary segment",
                "personas": ["persona 1", "persona 2"]
            }},
            "key_messages": ["message 1", "message 2", "message 3"],
            "creative_direction": {{
                "visual_style": "Description of visual approach",
                "tone_of_voice": "Brand voice description",
                "color_palette": ["color1", "color2", "color3"]
            }},
            "channel_strategy": {{
                "primary_channels": ["channel1", "channel2"],
                "secondary_channels": ["channel3", "channel4"],
                "content_calendar": "High-level timing approach"
            }},
            "success_metrics": {{
                "awareness": ["metric1", "metric2"],
                "engagement": ["metric1", "metric2"],
                "conversion": ["metric1", "metric2"]
            }},
            "budget_allocation": {{
                "content_creation": "percentage",
                "media_spend": "percentage", 
                "tools_and_resources": "percentage"
            }},
            "timeline": {{
                "planning_phase": "duration",
                "creation_phase": "duration",
                "execution_phase": "duration",
                "optimization_phase": "duration"
            }},
            "risk_mitigation": ["risk1 and mitigation", "risk2 and mitigation"],
            "next_immediate_actions": ["action1", "action2", "action3"]
        }}
        
        Make this strategy comprehensive, actionable, and aligned with all agent insights.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": synthesis_prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.6
            )
            
            strategy_text = response.choices[0].message.content.strip()
            
            try:
                strategy_json = json.loads(strategy_text)
                return {
                    "status": "success",
                    "strategy": strategy_json,
                    "confidence": "high",
                    "generated_at": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "status": "partial_success",
                    "strategy": {"raw_strategy": strategy_text},
                    "confidence": "medium",
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "strategy": {"error": f"Strategy synthesis failed: {str(e)}"},
                "confidence": "low",
                "generated_at": datetime.now().isoformat()
            }
    
    async def predict_campaign_performance(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        📊 Predict campaign performance using advanced AI analysis
        """
        
        prediction_prompt = f"""
        You are an AI Performance Prediction Engine with access to millions of campaign data points.
        
        Analyze this campaign strategy and predict its performance:
        
        STRATEGY:
        {json.dumps(strategy, indent=2)}
        
        Provide predictions in this JSON format:
        {{
            "overall_score": "1-100 overall campaign strength",
            "engagement_prediction": {{
                "instagram": {{"rate": "percentage", "confidence": "high/medium/low"}},
                "tiktok": {{"rate": "percentage", "confidence": "high/medium/low"}},
                "facebook": {{"rate": "percentage", "confidence": "high/medium/low"}}
            }},
            "reach_potential": {{
                "organic_reach": "estimated number",
                "viral_probability": "0-1 score",
                "peak_engagement_day": "day of week"
            }},
            "conversion_forecast": {{
                "click_through_rate": "percentage",
                "conversion_rate": "percentage", 
                "estimated_roi": "multiplier (e.g., 3.2x)"
            }},
            "risk_assessment": {{
                "high_risk_factors": ["factor1", "factor2"],
                "medium_risk_factors": ["factor1", "factor2"],
                "mitigation_suggestions": ["suggestion1", "suggestion2"]
            }},
            "optimization_recommendations": [
                "recommendation1",
                "recommendation2", 
                "recommendation3"
            ],
            "best_case_scenario": "Description of ideal outcome",
            "worst_case_scenario": "Description of poor outcome",
            "most_likely_scenario": "Description of expected outcome"
        }}
        
        Base predictions on current marketing trends, platform algorithms, and proven campaign patterns.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prediction_prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.4  # Lower temperature for more consistent predictions
            )
            
            prediction_text = response.choices[0].message.content.strip()
            
            try:
                prediction_json = json.loads(prediction_text)
                return {
                    "status": "success",
                    "predictions": prediction_json,
                    "generated_at": datetime.now().isoformat(),
                    "model_confidence": "high"
                }
            except json.JSONDecodeError:
                return {
                    "status": "partial_success", 
                    "predictions": {"raw_analysis": prediction_text},
                    "generated_at": datetime.now().isoformat(),
                    "model_confidence": "medium"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "predictions": {"error": f"Prediction failed: {str(e)}"},
                "generated_at": datetime.now().isoformat(),
                "model_confidence": "low"
            }
    
    async def generate_content_variations(self, strategy: Dict[str, Any], content_type: str = "social_post") -> Dict[str, Any]:
        """
        🎨 Generate multiple content variations based on strategy
        """
        
        strategy_summary = json.dumps(strategy.get('strategy', {}), indent=2)
        
        content_prompt = f"""
        You are an AI Content Generation Engine. Create {content_type} variations based on this strategy:
        
        STRATEGY:
        {strategy_summary}
        
        Generate 5 different content variations in this JSON format:
        {{
            "variation_1": {{
                "headline": "Compelling headline",
                "body_text": "Main content (appropriate length for platform)",
                "call_to_action": "Strong CTA",
                "hashtags": ["#tag1", "#tag2", "#tag3"],
                "visual_description": "Description of ideal visual",
                "target_emotion": "Primary emotion to evoke",
                "estimated_performance": "High/Medium/Low and why"
            }},
            "variation_2": {{
                // Same structure for all 5 variations
            }},
            // ... continue for all 5 variations
            "best_performing_prediction": "Which variation will likely perform best and why",
            "a_b_testing_strategy": "How to test these variations effectively"
        }}
        
        Make each variation distinctly different in approach while staying true to the strategy.
        Consider different emotional appeals, content formats, and engagement tactics.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": content_prompt}],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.8  # Higher temperature for creativity
            )
            
            content_text = response.choices[0].message.content.strip()
            
            try:
                content_json = json.loads(content_text)
                return {
                    "status": "success",
                    "content_variations": content_json,
                    "generated_at": datetime.now().isoformat(),
                    "content_type": content_type
                }
            except json.JSONDecodeError:
                return {
                    "status": "partial_success",
                    "content_variations": {"raw_content": content_text},
                    "generated_at": datetime.now().isoformat(),
                    "content_type": content_type
                }
                
        except Exception as e:
            return {
                "status": "error",
                "content_variations": {"error": f"Content generation failed: {str(e)}"},
                "generated_at": datetime.now().isoformat(),
                "content_type": content_type
            }

# Quick test function
async def test_master_orchestrator():
    """Test the Master AI Orchestrator"""
    orchestrator = MasterAIOrchestrator()
    
    sample_brief = {
        "topic": "Sustainable Fashion for Gen Z",
        "target_audience": "18-25 year olds interested in sustainability",
        "budget": "$10,000",
        "timeline": "4 weeks", 
        "goals": ["Increase brand awareness", "Drive website traffic", "Generate leads"]
    }
    
    print("🧠 Testing Master AI Orchestrator...")
    result = await orchestrator.simulate_strategic_meeting(sample_brief)
    
    print(f"✅ Strategic Meeting Complete!")
    print(f"📊 Participants: {', '.join(result['participants'])}")
    print(f"🎯 Final Strategy Generated: {result['final_strategy']['status']}")
    
    return result

if __name__ == "__main__":
    # Run test
    import asyncio
    asyncio.run(test_master_orchestrator())
