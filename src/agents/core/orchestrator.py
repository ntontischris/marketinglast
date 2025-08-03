from .content_strategy import ContentStrategyAgent
from .content_writer import ContentWriterAgent

from ..specialists.visual_suggestion import VisualSuggestionAgent
from ..specialists.image_generation import ImageGenerationAgent
from ..specialists.client_briefing import ClientBriefingAgent
from ..specialists.trend_analysis import TrendAnalysisAgent
from ..specialists.campaign_strategist import CampaignStrategistAgent
from ..specialists.brand_voice import BrandVoiceAgent
from ..specialists.performance_optimizer import PerformanceOptimizerAgent

# Import enhanced components
try:
    from ..enhanced.memory_manager import MemoryManager
    from ..enhanced.analytics_agent import AnalyticsAgent
    ENHANCED_FEATURES = True
except ImportError:
    print("Enhanced features not available - running in basic mode")
    ENHANCED_FEATURES = False

class OrchestratorAgent:
    """
    Enhanced orchestrator agent that coordinates workflow between specialized agents.
    Now includes memory management and analytics capabilities.
    """
    def __init__(self):
        """
        Initialize the Orchestrator and all coordinated agents.
        """
        print("🎭 Orchestrator: Initializing enhanced agent system...")

        # Core agents
        self.content_strategy_agent = ContentStrategyAgent()
        self.content_writer_agent = ContentWriterAgent()
        self.visual_suggestion_agent = VisualSuggestionAgent()
        self.image_generation_agent = ImageGenerationAgent()
        self.client_briefing_agent = ClientBriefingAgent()
        self.trend_analysis_agent = TrendAnalysisAgent()
        
        # New collaborative agents
        self.campaign_strategist_agent = CampaignStrategistAgent()
        self.brand_voice_agent = BrandVoiceAgent()
        self.performance_optimizer_agent = PerformanceOptimizerAgent()
        
        # Enhanced features (if available)
        if ENHANCED_FEATURES:
            try:
                self.memory_manager = MemoryManager()
                self.analytics_agent = AnalyticsAgent()
                print("✅ Enhanced features loaded: Memory management and Analytics")
            except Exception as e:
                print(f"⚠️ Enhanced features failed to load: {e}")
                self.memory_manager = None
                self.analytics_agent = None
        else:
            self.memory_manager = None
            self.analytics_agent = None
        
        print("🎭 Orchestrator: All agents initialized successfully.")
    
    def get_user_context(self, user_id: str):
        """Get user context from memory if available."""
        if self.memory_manager:
            return self.memory_manager.get_user_profile(user_id)
        return None
    
    def save_campaign_to_memory(self, user_id: str, campaign_data: dict):
        """Save campaign to memory if available."""
        if self.memory_manager:
            self.memory_manager.save_campaign(user_id, campaign_data)
    
    def analyze_content_performance(self, state: dict):
        """Analyze content using analytics agent if available."""
        if self.analytics_agent:
            return self.analytics_agent.invoke(state)
        return state


