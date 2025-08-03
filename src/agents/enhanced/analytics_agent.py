import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent
from src.agents.enhanced.memory_manager import MemoryManager

load_dotenv()

class AnalyticsAgent(BaseAgent):
    """
    Advanced analytics agent that provides performance insights,
    A/B testing suggestions, and optimization recommendations.
    """
    
    def __init__(self):
        super().__init__(name="Analytics & Optimization Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        self.memory = MemoryManager()
        
        # Configure Groq API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.client = Groq(api_key=api_key)
        
        print(f"'{self.name}' initialized with advanced analytics capabilities.")
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content and provide optimization insights.
        """
        content = state.get("final_content", "")
        topic = state.get("topic", "")
        user_id = state.get("user_id", "default_user")
        
        if not content:
            return {**state, "analytics": "No content provided for analysis."}
        
        print(f"-- '{self.name}' analyzing content for optimization opportunities... --")
        
        # Get user profile for personalized analysis
        user_profile = self.memory.get_user_profile(user_id)
        similar_campaigns = self.memory.get_similar_campaigns(topic)
        
        # Perform comprehensive analysis
        engagement_prediction = self._predict_engagement(content, user_profile)
        platform_optimization = self._suggest_platform_optimization(content)
        ab_test_suggestions = self._generate_ab_test_ideas(content)
        timing_recommendations = self._suggest_optimal_timing(topic, user_profile)
        hashtag_analysis = self._analyze_hashtags(content)
        
        analytics_report = {
            "engagement_prediction": engagement_prediction,
            "platform_optimization": platform_optimization,
            "ab_test_suggestions": ab_test_suggestions,
            "timing_recommendations": timing_recommendations,
            "hashtag_analysis": hashtag_analysis,
            "performance_benchmarks": self._get_performance_benchmarks(similar_campaigns),
            "improvement_suggestions": self._generate_improvement_suggestions(content, user_profile)
        }
        
        return {**state, "analytics": analytics_report}
    
    def _predict_engagement(self, content: str, user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Predict engagement metrics for the content."""
        prompt = f"""
        You are an advanced social media analytics expert. Analyze the following content and predict its engagement potential.
        
        Content: "{content}"
        User Profile: {json.dumps(user_profile) if user_profile else "No profile data"}
        
        Provide predictions for:
        1. Engagement Rate (0-100%)
        2. Reach Potential (Low/Medium/High)
        3. Virality Score (1-10)
        4. Best Performing Platform
        5. Key engagement drivers
        6. Potential weaknesses
        
        Format as JSON with numerical scores and explanations.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            prediction_text = response.choices[0].message.content
            return {
                "raw_analysis": prediction_text,
                "confidence": "high",
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Prediction failed: {e}"}
    
    def _suggest_platform_optimization(self, content: str) -> Dict[str, Any]:
        """Suggest optimizations for different platforms."""
        prompt = f"""
        As a platform optimization specialist, analyze this content and suggest specific optimizations for each major platform:
        
        Content: "{content}"
        
        For each platform (Instagram, Facebook, Twitter, TikTok, LinkedIn), provide:
        1. Content modifications needed
        2. Optimal post format
        3. Best hashtag strategy
        4. Visual recommendations
        5. Engagement tactics
        
        Return as structured JSON with platform-specific recommendations.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            optimization_text = response.choices[0].message.content
            return {
                "platform_recommendations": optimization_text,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Platform optimization failed: {e}"}
    
    def _generate_ab_test_ideas(self, content: str) -> List[Dict[str, Any]]:
        """Generate A/B testing ideas for the content."""
        prompt = f"""
        You are an A/B testing strategist. Create 5 different A/B test ideas for this content:
        
        Original Content: "{content}"
        
        For each test, provide:
        1. Test hypothesis
        2. Variable being tested
        3. Alternative version
        4. Success metrics
        5. Expected outcome
        
        Focus on testing: headlines, CTAs, emojis, tone, length, timing.
        Return as structured JSON array.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            ab_tests = response.choices[0].message.content
            return [{
                "ab_test_suggestions": ab_tests,
                "generated_at": datetime.now().isoformat()
            }]
        except Exception as e:
            return [{"error": f"A/B test generation failed: {e}"}]
    
    def _suggest_optimal_timing(self, topic: str, user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Suggest optimal posting times based on topic and audience."""
        industry = user_profile.get('industry', 'general') if user_profile else 'general'
        target_audience = user_profile.get('target_audience', 'general') if user_profile else 'general'
        
        prompt = f"""
        As a social media timing expert, suggest optimal posting times for:
        
        Topic: "{topic}"
        Industry: "{industry}"
        Target Audience: "{target_audience}"
        
        Provide:
        1. Best days of the week
        2. Optimal hours for each platform
        3. Time zone considerations
        4. Seasonal factors
        5. Audience behavior patterns
        
        Return as structured recommendations with reasoning.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            timing_advice = response.choices[0].message.content
            return {
                "timing_recommendations": timing_advice,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Timing analysis failed: {e}"}
    
    def _analyze_hashtags(self, content: str) -> Dict[str, Any]:
        """Analyze and optimize hashtag strategy."""
        prompt = f"""
        As a hashtag optimization expert, analyze this content and provide hashtag strategy:
        
        Content: "{content}"
        
        Provide:
        1. Current hashtag analysis (if any)
        2. Trending hashtag suggestions
        3. Niche-specific hashtags
        4. Hashtag mix strategy (popular vs niche)
        5. Platform-specific hashtag recommendations
        6. Hashtag performance predictions
        
        Return as structured analysis with specific recommendations.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            hashtag_analysis = response.choices[0].message.content
            return {
                "hashtag_strategy": hashtag_analysis,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Hashtag analysis failed: {e}"}
    
    def _get_performance_benchmarks(self, similar_campaigns: List[Dict]) -> Dict[str, Any]:
        """Get performance benchmarks from similar campaigns."""
        if not similar_campaigns:
            return {"message": "No historical data available for benchmarking"}
        
        total_engagement = sum(camp.get('engagement_score', 0) for camp in similar_campaigns)
        avg_engagement = total_engagement / len(similar_campaigns) if similar_campaigns else 0
        
        return {
            "similar_campaigns_count": len(similar_campaigns),
            "average_engagement": avg_engagement,
            "top_performing_campaign": max(similar_campaigns, key=lambda x: x.get('engagement_score', 0)),
            "benchmarks": {
                "good_engagement": avg_engagement * 1.2,
                "excellent_engagement": avg_engagement * 1.5
            }
        }
    
    def _generate_improvement_suggestions(self, content: str, user_profile: Optional[Dict]) -> List[str]:
        """Generate specific improvement suggestions."""
        prompt = f"""
        As a content optimization consultant, provide 5 specific, actionable improvement suggestions for this content:
        
        Content: "{content}"
        User Profile: {json.dumps(user_profile) if user_profile else "No profile available"}
        
        Focus on:
        1. Engagement optimization
        2. Call-to-action improvements
        3. Emotional appeal enhancement
        4. Clarity and readability
        5. Brand voice alignment
        
        Provide concrete, implementable suggestions.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            
            suggestions_text = response.choices[0].message.content
            # Parse the suggestions into a list (simplified)
            suggestions = [line.strip() for line in suggestions_text.split('\n') if line.strip() and (line.strip().startswith(('1.', '2.', '3.', '4.', '5.')) or line.strip().startswith('-'))]
            
            return suggestions[:5]  # Return top 5 suggestions
        except Exception as e:
            return [f"Error generating suggestions: {e}"]
