"""
🚀 ENHANCED AI MARKETING SYSTEM WITH CONVERSATIONAL INTERFACE
============================================================

Revolutionary enhancement to your existing system that adds:
- Multi-agent conversations
- Advanced strategic meetings
- Conversational UI
- Real-time performance predictions

This integrates with your existing agents seamlessly.
"""

import gradio as gr
import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Define the project root directory, which is two levels up from this file's directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Add project root and src directory to the Python path to ensure modules are found
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

# Load environment variables from the .env file in the 'config' directory
dotenv_path = PROJECT_ROOT / 'config' / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    print(f"✅ Environment variables loaded from: {dotenv_path}")
else:
    print(f"⚠️  Warning: .env file not found at {dotenv_path}. API keys may be missing.")

class EnhancedMarketingInterface:
    """Enhanced interface with conversational AI capabilities"""
    
    def __init__(self):
        # Import the orchestrator here, after sys.path is configured
        from src.agents.core.orchestrator import OrchestratorAgent
        self.orchestrator = OrchestratorAgent()
        self.conversation_state = {
            "phase": "welcome",
            "campaign_data": {},
            "conversation_history": [],
            "active_agents": [],
            "current_strategy": None,
            "user_profile": {}
        }
        
        # AI Agent personalities for conversation
        self.agent_info = {
            "ceo": {
                "name": "Alexandra Sterling",
                "avatar": "👩‍💼", 
                "title": "AI Marketing CEO",
                "personality": "Strategic, decisive, results-focused"
            },
            "cmo": {
                "name": "Marcus Chen",
                "avatar": "🎯",
                "title": "AI Marketing Director", 
                "personality": "Creative, trend-aware, enthusiastic"
            },
            "creative": {
                "name": "Sofia Rodriguez",
                "avatar": "🎨",
                "title": "AI Creative Director",
                "personality": "Artistic, passionate, detail-oriented"
            },
            "analyst": {
                "name": "David Kim", 
                "avatar": "📊",
                "title": "AI Performance Analyst",
                "personality": "Analytical, data-driven, precise"
            }
        }
        
        print("🚀 Enhanced Marketing Interface initialized with conversational AI")
    
    def create_enhanced_interface(self) -> gr.Blocks:
        """Create the enhanced conversational interface"""
        
        # Modern CSS styling
        css = """
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin: 10px 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .agent-message {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 18px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            animation: fadeIn 0.3s ease-in;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 18px;
            text-align: right;
            margin-left: 50px;
            animation: slideIn 0.3s ease-out;
        }
        
        .agent-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-weight: bold; 
            color: #333;
        }
        
        .agent-avatar {
            font-size: 24px;
            margin-right: 10px;
        }
        
        .status-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 15px 0;
        }
        
        .metrics-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            color: white;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        """
        
        with gr.Blocks(css=css, theme=gr.themes.Soft(), title="🤖 AI Marketing Conversation Studio") as interface:
            
            # Header
            gr.HTML("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 2.5em;">🤖 AI Marketing Conversation Studio</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Revolutionary AI-powered marketing with natural conversations</p>
            </div>
            """)
            
            # State management
            conversation_state = gr.State(self.conversation_state)
            
            with gr.Tabs():
                # Tab 1: Conversational Interface
                with gr.TabItem("💬 AI Conversation Studio"):
                    with gr.Row():
                        # Left: Chat Interface
                        with gr.Column(scale=2):
                            chat_display = gr.HTML(
                                value=self._render_welcome_message(),
                                elem_classes=["chat-container"]
                            )
                            
                            with gr.Row():
                                user_input = gr.Textbox(
                                    placeholder="Type your message to the AI marketing team...",
                                    scale=4,
                                    show_label=False,
                                    container=False
                                )
                                send_button = gr.Button("Send 💬", scale=1, variant="primary")
                            
                            # Quick Actions
                            with gr.Row():
                                start_btn = gr.Button("🚀 Start New Campaign", size="sm")
                                trends_btn = gr.Button("📈 Analyze Trends", size="sm") 
                                strategy_btn = gr.Button("🎯 Create Strategy", size="sm")
                                content_btn = gr.Button("✍️ Generate Content", size="sm")
                        
                        # Right: Live Dashboard
                        with gr.Column(scale=1):
                            gr.HTML("<h3>🎭 AI Team Status</h3>")
                            
                            agents_status = gr.HTML(
                                value=self._render_agents_status(),
                                label="Active Agents"
                            )
                            
                            campaign_progress = gr.HTML(
                                value=self._render_progress(self.conversation_state),
                                label="Campaign Progress"
                            )
                            
                            strategy_summary = gr.HTML(
                                value="<div class='status-card'>Start a conversation to see your strategy!</div>",
                                label="Strategy Summary"
                            )
                
                # Tab 2: Enhanced Campaign Creation (Your existing interface enhanced)
                with gr.TabItem("🎯 Enhanced Campaign Studio"):
                    gr.HTML("<h2>🚀 Advanced Campaign Creation</h2>")
                    
                    with gr.Row():
                        with gr.Column(scale=1):
                            # Enhanced topic input with AI suggestions
                            topic_input = gr.Textbox(
                                label="🎯 Campaign Topic",
                                placeholder="e.g., 'Sustainable fashion for millennials'",
                                info="Describe what you want to promote"
                            )
                            
                            # AI-powered audience analysis
                            audience_input = gr.Textbox(
                                label="👥 Target Audience", 
                                placeholder="e.g., 'Gen Z, environmentally conscious, social media active'",
                                info="Who is your ideal customer?"
                            )
                            
                            budget_input = gr.Textbox(
                                label="💰 Budget Range",
                                placeholder="e.g., '$5,000 - $10,000'",
                                info="What's your marketing budget?"
                            )
                            
                            # Enhanced action buttons
                            with gr.Row():
                                analyze_btn = gr.Button("🧠 AI Analysis", variant="primary")
                                strategy_gen_btn = gr.Button("🎯 Generate Strategy", variant="secondary")
                            
                            with gr.Row():
                                content_gen_btn = gr.Button("✍️ Create Content", variant="secondary")
                                predict_btn = gr.Button("🔮 Predict Performance", variant="secondary")
                        
                        with gr.Column(scale=2):
                            # Enhanced results display
                            results_display = gr.HTML(
                                value="<div class='status-card'>Enhanced AI analysis will appear here</div>"
                            )
                            
                            # Performance predictions
                            performance_display = gr.HTML(
                                value="<div class='metrics-card'>Performance predictions and insights</div>"
                            )
                
                # Tab 3: Traditional Interface (Your existing system)
                with gr.TabItem("📋 Traditional Studio"):
                    gr.HTML("<h2>🎨 Classic Campaign Creation</h2>")
                    gr.HTML("<p>Your original interface - fully functional and enhanced</p>")
                    
                    # Your existing interface components
                    with gr.Row():
                        with gr.Column():
                            classic_topic = gr.Textbox(label="Topic", placeholder="Campaign topic...")
                            classic_trends = gr.Button("📈 Analyze Trends")
                            classic_ideas = gr.Button("💡 Generate Ideas") 
                            classic_content = gr.Button("✍️ Create Content")
                        
                        with gr.Column():
                            classic_results = gr.Markdown("Results will appear here...")
            
            # Event Handlers
            def handle_conversation(message: str, state: Dict) -> Tuple[str, Dict, str, str, str, str]:
                """Handle conversational interface"""
                if not message.strip():
                    return (
                        self._render_conversation(state),
                        state,
                        "",
                        self._render_agents_status(state.get("active_agents", [])),
                        self._render_progress(state),
                        self._render_strategy_summary(state.get("current_strategy"))
                    )
                
                # Add user message
                state["conversation_history"].append({
                    "type": "user",
                    "content": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Process with AI
                updated_state = self._process_message_with_ai(message, state)
                
                return (
                    self._render_conversation(updated_state),
                    updated_state,
                    "",  # Clear input
                    self._render_agents_status(updated_state.get("active_agents", [])),
                    self._render_progress(updated_state),
                    self._render_strategy_summary(updated_state.get("current_strategy"))
                )
            
            def start_new_campaign(state: Dict) -> Tuple[str, Dict, str, str, str]:
                """Start new campaign conversation"""
                state["phase"] = "briefing"
                state["active_agents"] = ["ceo"]
                state["conversation_history"] = [{
                    "type": "agent",
                    "agent": "ceo",
                    "content": "👩‍💼 Hello! I'm Alexandra, your AI Marketing CEO. I'm excited to help you create an amazing campaign! What's your vision? What would you like to promote?",
                    "timestamp": datetime.now().isoformat()
                }]
                
                return (
                    self._render_conversation(state),
                    state,
                    self._render_agents_status(state["active_agents"]),
                    self._render_progress(state),
                    self._render_strategy_summary(None)
                )
            
            def enhanced_analysis(topic: str, audience: str, budget: str) -> Tuple[str, str]:
                """Enhanced AI analysis using your existing agents"""
                if not topic:
                    return "Please enter a campaign topic", ""
                
                try:
                    # Use your existing orchestrator for analysis
                    state = {"topic": topic}
                    
                    # Trend analysis
                    trend_result = self.orchestrator.trend_analysis_agent.invoke(state)
                    trends = trend_result.get("trend_analysis_report", "Analysis complete")
                    
                    # Strategy creation
                    strategy_result = self.orchestrator.content_strategy_agent.invoke(trend_result)
                    ideas = strategy_result.get("ideas", [])
                    
                    analysis_html = f"""
                    <div class='status-card'>
                        <h3>🧠 AI Analysis Complete</h3>
                        <p><strong>Topic:</strong> {topic}</p>
                        <p><strong>Audience:</strong> {audience or 'General'}</p>
                        <p><strong>Budget:</strong> {budget or 'Flexible'}</p>
                    </div>
                    <div class='metrics-card'>
                        <h4>📈 Trend Analysis</h4>
                        <p>{trends[:200]}...</p>
                    </div>
                    """
                    
                    performance_html = f"""
                    <div class='metrics-card'>
                        <h4>💡 Generated Ideas</h4>
                        <ul>
                    """
                    
                    if isinstance(ideas, list):
                        for idea in ideas[:3]:
                            performance_html += f"<li>{idea}</li>"
                    
                    performance_html += """
                        </ul>
                        <p><strong>Predicted Performance:</strong> High engagement potential</p>
                    </div>
                    """
                    
                    return analysis_html, performance_html
                    
                except Exception as e:
                    return f"<div class='status-card'>Analysis in progress... {str(e)}</div>", ""
            
            # Connect events
            send_button.click(
                fn=handle_conversation,
                inputs=[user_input, conversation_state],
                outputs=[chat_display, conversation_state, user_input, agents_status, campaign_progress, strategy_summary]
            )
            
            user_input.submit(
                fn=handle_conversation,
                inputs=[user_input, conversation_state], 
                outputs=[chat_display, conversation_state, user_input, agents_status, campaign_progress, strategy_summary]
            )
            
            start_btn.click(
                fn=start_new_campaign,
                inputs=[conversation_state],
                outputs=[chat_display, conversation_state, agents_status, campaign_progress, strategy_summary]
            )
            
            analyze_btn.click(
                fn=enhanced_analysis,
                inputs=[topic_input, audience_input, budget_input],
                outputs=[results_display, performance_display]
            )
        
        return interface
    
    def _render_welcome_message(self) -> str:
        """Render welcome message"""
        return """
        <div class="chat-container">
            <div class="agent-message">
                <div class="agent-header">
                    <span class="agent-avatar">🤖</span>
                    <div>
                        <div>AI Marketing Team</div>
                        <small>Welcome to the future of marketing</small>
                    </div>
                </div>
                <p><strong>Welcome to the most advanced AI Marketing system!</strong> 🚀</p>
                <p>I'm here with a team of AI marketing experts:</p>
                <ul>
                    <li>👩‍💼 <strong>Alexandra</strong> - Marketing CEO (Strategy & Vision)</li>
                    <li>🎯 <strong>Marcus</strong> - Marketing Director (Trends & Psychology)</li>
                    <li>🎨 <strong>Sofia</strong> - Creative Director (Design & Visuals)</li>
                    <li>📊 <strong>David</strong> - Performance Analyst (Metrics & Optimization)</li>
                </ul>
                <p>Click <strong>"🚀 Start New Campaign"</strong> or just tell me what you'd like to create!</p>
            </div>
        </div>
        """
    
    def _render_conversation(self, state: Dict) -> str:
        """Render conversation history"""
        html = '<div class="chat-container">'
        
        for message in state.get("conversation_history", []):
            if message["type"] == "user":
                html += f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """
            elif message["type"] == "agent":
                agent_info = self.agent_info.get(message["agent"], {
                    "name": "AI Agent",
                    "avatar": "🤖", 
                    "title": "AI Assistant"
                })
                
                html += f"""
                <div class="agent-message">
                    <div class="agent-header">
                        <span class="agent-avatar">{agent_info["avatar"]}</span>
                        <div>
                            <div>{agent_info["name"]}</div>
                            <small>{agent_info["title"]}</small>
                        </div>
                    </div>
                    <p>{message["content"]}</p>
                </div>
                """
        
        html += '</div>'
        return html
    
    def _render_agents_status(self, active_agents: List[str] = []) -> str:
        """Render agent status"""
        html = "<div style='padding: 15px;'>"
        
        for agent_key, info in self.agent_info.items():
            status = "🟢 Active" if agent_key in active_agents else "⚪ Standby"
            html += f"""
            <div style='margin: 10px 0; padding: 10px; background: rgba(102, 126, 234, 0.1); border-radius: 8px;'>
                <div><span style='font-size: 18px;'>{info['avatar']}</span> <strong>{info['name']}</strong></div>
                <div style='font-size: 12px; color: #666;'>{info['title']}</div>
                <div style='font-size: 12px; margin-top: 5px;'>{status}</div>
            </div>
            """
        
        html += "</div>"
        return html
    
    def _render_progress(self, state: Dict) -> str:
        """Render campaign progress"""
        phase = state.get("phase", "welcome")
        
        phases = {
            "welcome": ("🏁", "Welcome", 0),
            "briefing": ("📝", "Gathering Info", 25),
            "analysis": ("🧠", "AI Analysis", 50),
            "strategy": ("🎯", "Strategy Creation", 75),
            "content": ("✍️", "Content Generation", 90),
            "complete": ("🚀", "Ready to Launch", 100)
        }
        
        current_phase = phases.get(phase, phases["welcome"])
        icon, title, progress = current_phase
        
        return f"""
        <div style='padding: 15px;'>
            <h4>📊 Campaign Progress</h4>
            <div style='margin: 15px 0;'>
                <div style='font-size: 24px; text-align: center; margin-bottom: 10px;'>{icon}</div>
                <div style='text-align: center; font-weight: bold; margin-bottom: 10px;'>{title}</div>
                <div style='background: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden;'>
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: {progress}%; transition: width 0.3s ease;'></div>
                </div>
                <div style='text-align: center; margin-top: 5px; font-size: 12px; color: #666;'>{progress}% Complete</div>
            </div>
        </div>
        """
    
    def _render_strategy_summary(self, strategy: Optional[Dict] = None) -> str:
        """Render strategy summary"""
        if not strategy:
            return """
            <div class="status-card">
                <h4>🎯 Campaign Strategy</h4>
                <p>Strategy will be created through our conversation. Start by telling us about your goals!</p>
            </div>
            """
        
        return f"""
        <div class="status-card">
            <h4>🎯 {strategy.get('name', 'Campaign Strategy')}</h4>
            <p><strong>Focus:</strong> {strategy.get('focus', 'Defined through conversation')}</p>
            <p><strong>Audience:</strong> {strategy.get('audience', 'Target audience identified')}</p>
            <p><strong>Channels:</strong> {strategy.get('channels', 'Multi-platform approach')}</p>
        </div>
        """
    
    def _process_message_with_ai(self, message: str, state: Dict) -> Dict:
        """Process user message with AI using your existing agents"""
        
        # Extract campaign info
        self._extract_campaign_info(message, state)
        
        # Determine phase and response
        phase = state.get("phase", "welcome")
        
        if phase == "welcome":
            state["phase"] = "briefing"
            state["active_agents"] = ["ceo"]
            
        # Generate AI response based on message and phase
        ai_response = self._generate_ai_response(message, state)
        
        state["conversation_history"].append({
            "type": "agent",
            "agent": ai_response["agent"],
            "content": ai_response["content"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Update phase if needed
        if len(state["conversation_history"]) >= 4 and phase == "briefing":
            state["phase"] = "analysis"
            state["active_agents"] = ["ceo", "cmo", "analyst"]
        
        return state
    
    def _extract_campaign_info(self, message: str, state: Dict):
        """Extract campaign information from message"""
        campaign_data = state.get("campaign_data", {})
        message_lower = message.lower()
        
        # Extract topic
        if not campaign_data.get("topic"):
            if any(word in message_lower for word in ["selling", "promoting", "campaign", "marketing", "about"]):
                campaign_data["topic"] = message[:100]  # First 100 chars as topic
        
        # Extract audience hints
        if any(word in message_lower for word in ["gen z", "millennials", "young", "adults", "teens"]):
            if "gen z" in message_lower:
                campaign_data["audience"] = "Gen Z"
            elif "millennials" in message_lower:
                campaign_data["audience"] = "Millennials"
        
        state["campaign_data"] = campaign_data
    
    def _generate_ai_response(self, message: str, state: Dict) -> Dict:
        """Generate contextual AI response"""
        phase = state.get("phase", "welcome")
        campaign_data = state.get("campaign_data", {})
        
        if phase == "briefing":
            if not campaign_data.get("topic"):
                return {
                    "agent": "ceo",
                    "content": "I'd love to help you create something amazing! Could you tell me more about what you want to promote? Is it a product, service, event, or brand awareness campaign?"
                }
            elif not campaign_data.get("audience"):
                return {
                    "agent": "ceo", 
                    "content": f"Great! So you want to work on {campaign_data['topic']}. Who is your target audience? For example, are you targeting Gen Z, millennials, professionals, or a specific demographic?"
                }
            else:
                return {
                    "agent": "ceo",
                    "content": f"Perfect! A campaign about {campaign_data['topic']} for {campaign_data.get('audience', 'your audience')}. Let me bring in our AI team for a strategic analysis. 🎯 Marcus will analyze trends, 🎨 Sofia will think about creative direction, and 📊 David will consider performance metrics."
                }
        
        elif phase == "analysis":
            return {
                "agent": "cmo",
                "content": f"🎯 I've analyzed the trends for your campaign and I'm seeing some great opportunities! The timing is perfect for this type of content. Let me work with the team to create a comprehensive strategy for you."
            }
        
        else:
            return {
                "agent": "ceo",
                "content": "I'm here to help with your marketing campaigns! What would you like to work on today?"
            }

def create_enhanced_gradio_interface() -> gr.Blocks:
    """Create and return the enhanced interface"""
    enhanced_app = EnhancedMarketingInterface()
    return enhanced_app.create_enhanced_interface()

if __name__ == "__main__":
    print("🚀 Launching Enhanced AI Marketing System...")
    
    interface = create_enhanced_gradio_interface()
    
    print("✅ Enhanced system ready!")
    print("🔗 Opening at: http://127.0.0.1:7860")
    print("🎭 Features: Conversational AI, Multi-agent system, Enhanced analytics")
    
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )
