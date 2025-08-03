import gradio as gr
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Add root folder to path for proper imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.core.orchestrator import OrchestratorAgent

class EnhancedMarketingAI:
    """
    Enhanced AI Marketing Interface with collaborative agents and streamlined workflow.
    """
    
    def __init__(self):
        print("🚀 Initializing Enhanced Marketing AI System...")
        self.orchestrator = OrchestratorAgent()
        self.session_state: Dict[str, Any] = {}
        self.workflow_step = 0
        print("✅ System ready!")

    def start_intelligent_campaign(self, topic: str, target_audience: str = "", campaign_goals: str = "") -> Tuple[str, str, str, str]:
        """Intelligent campaign creation with collaborative agents."""
        if not topic.strip():
            return "❌ Παρακαλώ εισάγετε ένα θέμα", "", "", ""
        
        print(f"🎯 Starting intelligent campaign for: {topic}")
        
        # Reset session state for new campaign
        self.session_state = {
            "topic": topic.strip(),
            "target_audience": target_audience.strip() if target_audience else "",
            "campaign_goals": campaign_goals.strip() if campaign_goals else "",
            "workflow_step": 1
        }
        
        status_messages = []
        
        # Step 1: Trend Analysis
        status_messages.append("📈 Analyzing market trends...")
        state_with_trends = self.orchestrator.trend_analysis_agent.invoke(self.session_state)
        self.session_state.update(state_with_trends)
        
        # Step 2: Campaign Strategy Development
        status_messages.append("🎯 Developing comprehensive campaign strategy...")
        state_with_strategy = self.orchestrator.campaign_strategist_agent.invoke(self.session_state)
        self.session_state.update(state_with_strategy)
        
        # Step 3: Brand Voice Development
        status_messages.append("🎭 Creating brand voice guidelines...")
        state_with_voice = self.orchestrator.brand_voice_agent.invoke(self.session_state)
        self.session_state.update(state_with_voice)
        
        # Step 4: Content Ideas Generation
        status_messages.append("💡 Generating content ideas...")
        state_with_ideas = self.orchestrator.content_strategy_agent.invoke(self.session_state)
        self.session_state.update(state_with_ideas)
        
        final_status = "✅ Intelligent campaign analysis complete! Review the results below."
        
        return (
            final_status,
            self.session_state.get("trend_analysis_report", "No trend analysis available"),
            self.session_state.get("campaign_strategy", "No campaign strategy available"),
            self.session_state.get("brand_voice_guide", "No brand voice guide available")
        )

    def generate_optimized_content(self, selected_idea: str) -> Tuple[str, str, str]:
        """Generate content with performance optimization."""
        if not selected_idea or "ideas" not in self.session_state:
            return "❌ Παρακαλώ επιλέξτε μια ιδέα από τη λίστα", "", ""
        
        print(f"✍️ Generating optimized content for: {selected_idea}")
        
        # Generate content with brand voice context
        self.session_state["selected_idea"] = selected_idea
        state_with_content = self.orchestrator.content_writer_agent.invoke(self.session_state)
        self.session_state.update(state_with_content)
        
        # Generate performance optimization recommendations
        state_with_optimization = self.orchestrator.performance_optimizer_agent.invoke(self.session_state)
        self.session_state.update(state_with_optimization)
        
        # Generate visual suggestions
        state_with_visuals = self.orchestrator.visual_suggestion_agent.invoke(self.session_state)
        self.session_state.update(state_with_visuals)
        
        visual_suggestions = ""
        suggestions = self.session_state.get("visual_suggestions", [])
        if suggestions:
            visual_suggestions = "## 🎨 Visual Suggestions\n\n"
            for i, sug in enumerate(suggestions[:3]):  # Show top 3
                visual_suggestions += f"**{i+1}. {sug.get('description', 'Visual idea')}**\n"
                visual_suggestions += f"*Prompt:* `{sug.get('prompt', 'No prompt available')}`\n\n"
        
        return (
            "✅ Optimized content generated successfully!",
            self.session_state.get("final_content", "No content generated"),
            self.session_state.get("performance_recommendations", "No optimization recommendations available") + "\n\n" + visual_suggestions
        )

    def get_content_ideas(self) -> List[str]:
        """Get content ideas from current session."""
        return self.session_state.get("ideas", [])

    def get_campaign_summary(self) -> str:
        """Generate comprehensive campaign summary."""
        if not self.session_state:
            return "No campaign data available. Please start a campaign first."
        
        summary = f"""
# 📊 Campaign Summary Report

**Topic:** {self.session_state.get('topic', 'N/A')}
**Target Audience:** {self.session_state.get('target_audience', 'Not specified')}
**Campaign Goals:** {self.session_state.get('campaign_goals', 'Not specified')}

## 🎯 Strategy Overview
{self.session_state.get('campaign_strategy', 'Strategy not available')[:500]}...

## 🎭 Brand Voice
{self.session_state.get('brand_voice_guide', 'Brand voice not available')[:500]}...

## 💡 Content Ideas Generated
{len(self.session_state.get('ideas', []))} unique content ideas created

## 📈 Performance Insights
{self.session_state.get('performance_recommendations', 'Performance insights not available')[:300]}...

---
*Generated by Enhanced AI Marketing System*
        """
        return summary

def create_enhanced_interface():
    """Create the enhanced Gradio interface with better UX."""
    app = EnhancedMarketingAI()
    
    # Load custom CSS
    css_path = os.path.join(os.path.dirname(__file__), "static", "theme.css")
    css = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

    # Enhanced CSS for better UX
    enhanced_css = css + """
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .step-card {
        background: linear-gradient(135deg, rgba(30, 60, 114, 0.1), rgba(42, 82, 152, 0.1));
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .progress-indicator {
        background: linear-gradient(90deg, #1e88e5, #64b5f6);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
    }
    
    .result-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(100, 181, 246, 0.4);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    """

    with gr.Blocks(css=enhanced_css, title="🤖 Enhanced AI Marketing System", theme=gr.themes.Soft()) as interface:
        
        # Main header
        gr.HTML("""
        <div class='section-header'>
            <h1>🚀 Enhanced AI Marketing System</h1>
            <p>Συνεργατικοί AI Agents για Εξυπνη Δημιουργία Περιεχομένου</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Campaign Input Section
                gr.HTML('<div class="progress-indicator">🎯 Step 1: Campaign Setup</div>')
                
                with gr.Group():
                    topic_input = gr.Textbox(
                        label="💡 Campaign Topic", 
                        placeholder="e.g., 'Sustainable Fashion', 'AI in Healthcare', 'Remote Work Tools'...",
                        lines=1
                    )
                    
                    with gr.Row():
                        audience_input = gr.Textbox(
                            label="👥 Target Audience (Optional)", 
                            placeholder="e.g., 'Young professionals 25-35, tech-savvy'",
                            lines=1
                        )
                        goals_input = gr.Textbox(
                            label="🎯 Campaign Goals (Optional)", 
                            placeholder="e.g., 'Increase brand awareness, drive sales'",
                            lines=1
                        )
                
                start_campaign_btn = gr.Button("🚀 Start Intelligent Campaign", variant="primary", size="lg")
                
                # Progress and status
                campaign_status = gr.Textbox(label="📊 Campaign Status", interactive=False)
                
            with gr.Column(scale=1):
                # Quick Campaign Summary
                gr.HTML('<div class="progress-indicator">📋 Campaign Overview</div>')
                campaign_summary = gr.Markdown("Start a campaign to see the overview here...")
        
        # Results Section
        gr.HTML('<div class="progress-indicator">📈 Analysis Results</div>')
        
        with gr.Tabs():
            with gr.TabItem("📊 Market Analysis"):
                trends_output = gr.Markdown()
            
            with gr.TabItem("🎯 Campaign Strategy"):
                strategy_output = gr.Markdown()
            
            with gr.TabItem("🎭 Brand Voice Guide"):
                brand_voice_output = gr.Markdown()
        
        # Content Generation Section
        gr.HTML('<div class="progress-indicator">✍️ Content Creation</div>')
        
        with gr.Row():
            with gr.Column(scale=2):
                content_ideas_dropdown = gr.Dropdown(
                    label="💡 Select Content Idea", 
                    choices=[], 
                    interactive=True
                )
                generate_content_btn = gr.Button("✍️ Generate Optimized Content", variant="primary")
                
                content_status = gr.Textbox(label="✍️ Content Status", interactive=False)
                
            with gr.Column(scale=3):
                with gr.Tabs():
                    with gr.TabItem("📝 Final Content"):
                        final_content_output = gr.Markdown()
                    
                    with gr.TabItem("🚀 Optimization & Visuals"):
                        optimization_output = gr.Markdown()
        
        # Event handlers
        def update_campaign_data(topic, audience, goals):
            status, trends, strategy, brand_voice = app.start_intelligent_campaign(topic, audience, goals)
            ideas = app.get_content_ideas()
            summary = app.get_campaign_summary()
            
            return (
                status,
                trends,
                strategy, 
                brand_voice,
                gr.update(choices=ideas, value=ideas[0] if ideas else None),
                summary
            )
        
        start_campaign_btn.click(
            update_campaign_data,
            inputs=[topic_input, audience_input, goals_input],
            outputs=[campaign_status, trends_output, strategy_output, brand_voice_output, content_ideas_dropdown, campaign_summary]
        )
        
        generate_content_btn.click(
            app.generate_optimized_content,
            inputs=[content_ideas_dropdown],
            outputs=[content_status, final_content_output, optimization_output]
        )
        
        # Footer
        gr.HTML("""
        <div class='footer'>
            <p><strong>🤖 Enhanced AI Marketing System v2.0</strong></p>
            <p>Powered by DeepSeek R1 • Collaborative AI Agents • Advanced UX</p>
        </div>
        """)
    
    return interface

if __name__ == "__main__":
    demo = create_enhanced_interface()
    
    # Auto port detection
    import socket
    def find_free_port(start_port=7860):
        for port in range(start_port, start_port + 10):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        return None
    
    port = find_free_port()
    if port is None:
        print("❌ No available port found. Please close other applications.")
        exit(1)
    
    print(f"""
🚀 Enhanced AI Marketing System v2.0 Starting...
🔗 Open your browser: http://127.0.0.1:{port}
🛑 Press Ctrl+C to stop

Features:
✅ 3 New Collaborative Agents
✅ Intelligent Campaign Workflow  
✅ Enhanced User Experience
✅ Performance Optimization
✅ DeepSeek R1 Integration
    """)
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        debug=False,
        show_error=True,
        quiet=False
    )
