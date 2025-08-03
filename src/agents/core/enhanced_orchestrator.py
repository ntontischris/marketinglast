"""
Enhanced Orchestrator integrating MasterAIOrchestrator with enhanced agents
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent
from src.agents.specialists.enhanced_trend_analysis import EnhancedTrendAnalysisAgent
from src.agents.core.enhanced_content_strategy import EnhancedContentStrategyAgent
from src.agents.core.content_writer import ContentWriterAgent
from src.agents.specialists.social_media import SocialMediaAgent
from src.agents.specialists.image_generation import ImageGenerationAgent
from src.agents.specialists.visual_suggestion import VisualSuggestionAgent
from src.agents.specialists.client_briefing import ClientBriefingAgent

class EnhancedOrchestrator:
    """
    Enhanced orchestrator that coordinates multiple agents with advanced features
    """
    
    def __init__(self):
        self.logger = logging.getLogger("EnhancedOrchestrator")
        self.agents = {}
        self.workflow_history = []
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all enhanced agents"""
        
        self.agents = {
            "trend_analysis": EnhancedTrendAnalysisAgent(),
            "content_strategy": EnhancedContentStrategyAgent(),
            "content_writer": ContentWriterAgent(),
            "social_media": SocialMediaAgent(),
            "image_generation": ImageGenerationAgent(),
            "visual_suggestion": VisualSuggestionAgent(),
            "client_briefing": ClientBriefingAgent()
        }
        
        self.logger.info("All enhanced agents initialized successfully")
    
    async def execute_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute complete marketing workflow with enhanced agents
        
        Args:
            workflow_config: Configuration for the workflow including:
                - topic: Main topic for content
                - target_audience: Target audience definition
                - content_goals: List of content goals
                - platforms: Target platforms
                - duration: Campaign duration (days)
                - budget: Available budget
        
        Returns:
            Complete workflow results with all agent outputs
        """
        
        start_time = datetime.now()
        workflow_id = f"workflow_{int(start_time.timestamp())}"
        
        self.logger.info(f"Starting enhanced workflow: {workflow_id}")
        
        try:
            # Initialize state
            state = {
                "workflow_id": workflow_id,
                "start_time": start_time.isoformat(),
                "config": workflow_config,
                "topic": workflow_config.get("topic"),
                "target_audience": workflow_config.get("target_audience", "general"),
                "content_goals": workflow_config.get("content_goals", ["engagement"]),
                "platforms": workflow_config.get("platforms", ["instagram", "facebook"]),
                "duration": workflow_config.get("duration", 30),
                "budget": workflow_config.get("budget", 1000)
            }
            
            # Execute workflow phases
            results = await self._execute_phases(state)
            
            # Compile final results
            final_results = self._compile_results(results, workflow_id)
            
            # Store in history
            self.workflow_history.append(final_results)
            
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            return final_results
            
        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            return self._handle_workflow_error(workflow_id, str(e))
    
    async def _execute_phases(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow in phases"""
        
        results = {"phases": {}}
        
        # Phase 1: Trend Analysis
        self.logger.info("Phase 1: Trend Analysis")
        trend_result = await self.agents["trend_analysis"].execute_with_metrics(state)
        results["phases"]["trend_analysis"] = {
            "output": trend_result,
            "metrics": self.agents["trend_analysis"].get_metrics()
        }
        
        # Phase 2: Content Strategy
        self.logger.info("Phase 2: Content Strategy")
        strategy_result = await self.agents["content_strategy"].execute_with_metrics(trend_result)
        results["phases"]["content_strategy"] = {
            "output": strategy_result,
            "metrics": self.agents["content_strategy"].get_metrics()
        }
        
        # Phase 3: Content Creation
        self.logger.info("Phase 3: Content Creation")
        content_results = await self._create_content_batch(strategy_result)
        results["phases"]["content_creation"] = content_results
        
        # Phase 4: Visual Assets
        self.logger.info("Phase 4: Visual Assets")
        visual_results = await self._create_visual_assets(strategy_result, content_results)
        results["phases"]["visual_assets"] = visual_results
        
        # Phase 5: Social Media Optimization
        self.logger.info("Phase 5: Social Media Optimization")
        social_results = await self.agents["social_media"].execute_with_metrics({
            **strategy_result,
            "content": content_results.get("content", []),
            "visuals": visual_results.get("visuals", [])
        })
        results["phases"]["social_media"] = {
            "output": social_results,
            "metrics": self.agents["social_media"].get_metrics()
        }
        
        # Phase 6: Client Briefing
        self.logger.info("Phase 6: Client Briefing")
        briefing_result = await self.agents["client_briefing"].execute_with_metrics({
            **strategy_result,
            "content": content_results.get("content", []),
            "visuals": visual_results.get("visuals", []),
            "social_optimization": social_results
        })
        results["phases"]["client_briefing"] = {
            "output": briefing_result,
            "metrics": self.agents["client_briefing"].get_metrics()
        }
        
        return results
    
    async def _create_content_batch(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create multiple content pieces based on strategy"""
        
        calendar = state.get("content_calendar", [])
        content_pieces = []
        
        # Create content for first 5 days as sample
        sample_days = calendar[:5]
        
        for day_content in sample_days:
            try:
                content_state = {
                    **state,
                    "content_type": day_content.get("type", "post"),
                    "platform": day_content.get("platform", "instagram"),
                    "theme": day_content.get("theme", "general")
                }
                
                content_result = await self.agents["content_writer"].execute_with_metrics(content_state)
                content_pieces.append({
                    "day": day_content.get("day"),
                    "content": content_result.get("content", ""),
                    "metadata": content_result
                })
                
            except Exception as e:
                self.logger.warning(f"Failed to create content for day {day_content.get('day')}: {str(e)}")
        
        return {
            "content": content_pieces,
            "total_created": len(content_pieces),
            "total_planned": len(calendar)
        }
    
    async def _create_visual_assets(self, state: Dict[str, Any], 
                                  content_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create visual assets for content"""
        
        visuals = []
        content_pieces = content_results.get("content", [])
        
        for content in content_pieces[:3]:  # Create visuals for first 3 pieces
            try:
                visual_state = {
                    **state,
                    "content": content.get("content", ""),
                    "content_type": "social_media_post"
                }
                
                visual_result = await self.agents["image_generation"].execute_with_metrics(visual_state)
                visuals.append({
                    "content_id": content.get("day"),
                    "visual_prompt": visual_result.get("image_prompt", ""),
                    "suggestions": visual_result.get("suggestions", [])
                })
                
            except Exception as e:
                self.logger.warning(f"Failed to create visual for content {content.get('day')}: {str(e)}")
        
        return {
            "visuals": visuals,
            "total_created": len(visuals)
        }
    
    def _compile_results(self, results: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Compile all results into final workflow output"""
        
        end_time = datetime.now()
        duration = (end_time - datetime.fromisoformat(
            results["phases"]["trend_analysis"]["output"].get("start_time", end_time.isoformat())
        )).total_seconds()
        
        # Calculate aggregate metrics
        total_agents = len(self.agents)
        successful_phases = sum(1 for phase in results["phases"].values() 
                              if "error" not in str(phase))
        
        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "duration_seconds": duration,
            "phases": results["phases"],
            "summary": {
                "total_agents": total_agents,
                "successful_phases": successful_phases,
                "success_rate": successful_phases / total_agents,
                "content_pieces_created": results["phases"]["content_creation"]["total_created"],
                "visuals_created": results["phases"]["visual_assets"]["total_created"]
            },
            "timestamp": end_time.isoformat()
        }
    
    def _handle_workflow_error(self, workflow_id: str, error: str) -> Dict[str, Any]:
        """Handle workflow errors gracefully"""
        
        return {
            "workflow_id": workflow_id,
            "status": "failed",
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workflow history"""
        
        return self.workflow_history[-limit:] if self.workflow_history else []
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics for all agents"""
        
        return {
            agent_name: agent.get_metrics()
            for agent_name, agent in self.agents.items()
        }
    
    async def execute_single_phase(self, phase: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single phase of the workflow"""
        
        if phase not in self.agents:
            raise ValueError(f"Unknown phase: {phase}")
        
        agent = self.agents[phase]
        return await agent.execute_with_metrics(state)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        
        return {
            "agents_initialized": len(self.agents),
            "total_workflows": len(self.workflow_history),
            "last_workflow": self.workflow_history[-1]["workflow_id"] if self.workflow_history else None,
            "agent_metrics": self.get_agent_metrics(),
            "system_health": "healthy" if all(
                agent.get_metrics()["success_rate"] > 0.8 
                for agent in self.agents.values()
            ) else "degraded"
        }

# Example usage
async def test_enhanced_orchestrator():
    """Test the enhanced orchestrator"""
    
    orchestrator = EnhancedOrchestrator()
    
    workflow_config = {
        "topic": "Sustainable Fashion",
        "target_audience": "eco-conscious millennials aged 25-35",
        "content_goals": ["brand_awareness", "community_engagement", "sales_conversion"],
        "platforms": ["instagram", "tiktok", "facebook"],
        "duration": 30,
        "budget": 2000
    }
    
    try:
        print("Starting enhanced workflow...")
        results = await orchestrator.execute_workflow(workflow_config)
        
        print(f"\n{'='*60}")
        print("WORKFLOW COMPLETED")
        print('='*60)
        print(f"Workflow ID: {results['workflow_id']}")
        print(f"Duration: {results['duration_seconds']:.2f} seconds")
        print(f"Success Rate: {results['summary']['success_rate']:.2%}")
        print(f"Content Pieces: {results['summary']['content_pieces_created']}")
        print(f"Visual Assets: {results['summary']['visuals_created']}")
        
        # Display agent metrics
        print("\nAgent Performance:")
        for agent_name, metrics in results.get("agent_metrics", {}).items():
            print(f"  {agent_name}: {metrics['success_rate']:.2%} success rate")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_orchestrator())
