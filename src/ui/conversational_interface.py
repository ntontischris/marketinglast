"""
🎨 CONVERSATIONAL UI SYSTEM
===========================

Revolutionary conversational interface that transforms marketing campaign creation
into natural, AI-powered conversations with multiple specialized agents.

This replaces traditional forms with intelligent, context-aware dialogue.
"""

import gradio as gr
import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os

from src.core.master_orchestrator import MasterAIOrchestrator, AgentRole

class ConversationalInterface:
    """
    Revolutionary UI that enables natural conversations with AI marketing agents
    """
    
    def __init__(self):
        self.orchestrator = MasterAIOrchestrator()
        self.conversation_state = {
            "phase": "initial",  # initial, briefing, strategy, content, execution
            "campaign_data": {},
            "conversation_history": [],
            "active_agents": [],
            "current_strategy": None
        }
        
        # Agent avatars and descriptions
        self.agent_info = {
            "ceo": {
                "name": "Alexandra Sterling",
                "avatar": "👩‍💼",
                "title": "AI Marketing CEO",
                "description": "Strategic visionary focused on ROI and growth"
            },
            "cmo": {
                "name": "Marcus Chen", 
                "avatar": "🎯",
                "title": "AI Marketing Director",
                "description": "Creative strategist and trend analyst"
            },
            "creative_director": {
                "name": "Sofia Rodriguez",
                "avatar": "🎨",
                "title": "AI Creative Director", 
                "description": "Visual designer and brand expert"
            },
            "performance_manager": {
                "name": "David Kim",
                "avatar": "📊",
                "title": "AI Performance Manager",
                "description": "Analytics expert and optimizer"
            }
        }
        
        print("🎨 Conversational Interface initialized with AI agents")
    
    def create_interface(self) -> gr.Blocks:
        """Create the revolutionary conversational interface"""
        
        # Custom CSS for modern, chat-like interface
        css = """
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin: 10px 0;
        }
        
        .agent-message {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 18px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .user-message {
            background: #667eea;
            color: white;
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 18px;
            text-align: right;
            margin-left: 50px;
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
        
        .strategy-card {
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
        
        .action-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .typing-indicator {
            background: rgba(255, 255, 255, 0.9);
            padding: 10px 20px;
            border-radius: 18px;
            margin: 10px 0;
            font-style: italic;
            color: #666;
        }
        """
        
        with gr.Blocks(css=css, theme=gr.themes.Soft(), title="🤖 AI Marketing Conversation Studio") as interface:
            
            # Header
            gr.HTML("""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 2.5em;">🤖 AI Marketing Conversation Studio</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Have natural conversations with AI marketing experts to create amazing campaigns</p>
            </div>
            """)
            
            # State management (hidden)
            conversation_state = gr.State(self.conversation_state)
            
            with gr.Row():
                # Left Column: Chat Interface
                with gr.Column(scale=2):
                    gr.HTML("<h2>💬 Conversation with AI Marketing Team</h2>")
                    
                    # Chat display
                    chat_display = gr.HTML(
                        value=self._render_welcome_message(),
                        elem_classes=["chat-container"]
                    )
                    
                    # User input
                    with gr.Row():
                        user_input = gr.Textbox(
                            placeholder="Type your message to the AI marketing team...",
                            scale=4,
                            show_label=False
                        )
                        send_button = gr.Button("Send 💬", scale=1, variant="primary")
                    
                    # Quick action buttons
                    with gr.Row():
                        start_campaign_btn = gr.Button("🚀 Start New Campaign", size="sm")
                        analyze_trends_btn = gr.Button("📈 Analyze Trends", size="sm")
                        generate_content_btn = gr.Button("✍️ Generate Content", size="sm", interactive=False)
                        predict_performance_btn = gr.Button("🔮 Predict Performance", size="sm", interactive=False)
                
                # Right Column: Live Strategy & Analytics
                with gr.Column(scale=1):
                    gr.HTML("<h2>📊 Live Strategy Dashboard</h2>")
                    
                    # Active agents display
                    active_agents_display = gr.HTML(
                        value=self._render_agents_status(),
                        label="Active AI Agents"
                    )
                    
                    # Campaign progress
                    progress_display = gr.HTML(
                        value=self._render_progress(),
                        label="Campaign Progress"
                    )
                    
                    # Live strategy display
                    strategy_display = gr.HTML(
                        value="<div class='strategy-card'>No active strategy yet. Start a conversation to begin!</div>",
                        label="Current Strategy"
                    )
                    
                    # Performance predictions
                    performance_display = gr.HTML(
                        value="<div class='metrics-card'>Performance predictions will appear here after strategy creation.</div>",
                        label="Performance Predictions"
                    )
            
            # Event handlers
            
            def handle_user_message(message: str, state: Dict) -> Tuple[str, Dict, str, str, str, str]:
                """Handle user message and generate AI responses"""
                if not message.strip():
                    return (
                        self._render_conversation(state),
                        state,
                        "",
                        self._render_agents_status(state.get("active_agents", [])),
                        self._render_progress(state),
                        self._render_strategy(state.get("current_strategy"))
                    )
                
                # Add user message to conversation
                state["conversation_history"].append({
                    "type": "user",
                    "content": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Process message and generate AI response
                ai_response, updated_state = asyncio.run(
                    self._process_user_message(message, state)
                )
                
                return (
                    self._render_conversation(updated_state),
                    updated_state,
                    "",  # Clear input
                    self._render_agents_status(updated_state.get("active_agents", [])),
                    self._render_progress(updated_state),
                    self._render_strategy(updated_state.get("current_strategy"))
                )
            
            def start_new_campaign(state: Dict) -> Tuple[str, Dict, str, str, str]:
                """Start a new campaign conversation"""
                state["phase"] = "briefing"
                state["active_agents"] = ["ceo"]
                
                welcome_message = {
                    "type": "agent",
                    "agent": "ceo",
                    "content": "👩‍💼 Hello! I'm Alexandra, your AI Marketing CEO. I'm excited to help you create an amazing campaign! Tell me, what's your vision for this new marketing campaign? What product, service, or message do you want to promote?",
                    "timestamp": datetime.now().isoformat()
                }
                
                state["conversation_history"] = [welcome_message]
                
                return (
                    self._render_conversation(state),
                    state,
                    self._render_agents_status(state["active_agents"]),
                    self._render_progress(state),
                    self._render_strategy(state.get("current_strategy"))
                )
            
            def analyze_trends(state: Dict) -> Tuple[str, Dict, str, str, str]:
                """Trigger trend analysis"""
                if not state.get("campaign_data", {}).get("topic"):
                    # Add agent message requesting topic first
                    message = {
                        "type": "agent",
                        "agent": "cmo",
                        "content": "🎯 Hi! I'm Marcus, your AI Marketing Director. To analyze trends effectively, I need to know what topic or industry you're focusing on. Could you tell me more about your campaign focus?",
                        "timestamp": datetime.now().isoformat()
                    }
                    state["conversation_history"].append(message)
                    state["active_agents"] = ["cmo"]
                else:
                    # Perform trend analysis
                    message = {
                        "type": "agent", 
                        "agent": "cmo",
                        "content": f"🎯 Analyzing current trends for {state['campaign_data']['topic']}... This is fascinating! I'm seeing some incredible opportunities in this space. Let me share what I've discovered...",
                        "timestamp": datetime.now().isoformat()
                    }
                    state["conversation_history"].append(message)
                
                return (
                    self._render_conversation(state),
                    state,
                    self._render_agents_status(state.get("active_agents", [])),
                    self._render_progress(state),
                    self._render_strategy(state.get("current_strategy"))
                )
            
            # Connect events
            send_button.click(
                fn=handle_user_message,
                inputs=[user_input, conversation_state],
                outputs=[chat_display, conversation_state, user_input, active_agents_display, progress_display, strategy_display]
            )
            
            user_input.submit(
                fn=handle_user_message,
                inputs=[user_input, conversation_state],
                outputs=[chat_display, conversation_state, user_input, active_agents_display, progress_display, strategy_display]
            )
            
            start_campaign_btn.click(
                fn=start_new_campaign,
                inputs=[conversation_state],
                outputs=[chat_display, conversation_state, active_agents_display, progress_display, strategy_display]
            )
            
            analyze_trends_btn.click(
                fn=analyze_trends,
                inputs=[conversation_state],
                outputs=[chat_display, conversation_state, active_agents_display, progress_display, strategy_display]
            )
        
        return interface
    
    def _render_welcome_message(self) -> str:
        """Render the initial welcome message"""
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
                <p>Welcome to the most advanced AI Marketing system ever created! 🚀</p>
                <p>I'm here with a team of AI marketing experts ready to help you create incredible campaigns:</p>
                <ul>
                    <li>👩‍💼 <strong>Alexandra</strong> - AI Marketing CEO (Strategy & Vision)</li>
                    <li>🎯 <strong>Marcus</strong> - AI Marketing Director (Trends & Psychology)</li>
                    <li>🎨 <strong>Sofia</strong> - AI Creative Director (Design & Visuals)</li>
                    <li>📊 <strong>David</strong> - AI Performance Manager (Analytics & Optimization)</li>
                </ul>
                <p>Click <strong>"🚀 Start New Campaign"</strong> to begin our conversation, or just type what you'd like to create!</p>
            </div>
        </div>
        """
    
    def _render_conversation(self, state: Dict) -> str:
        """Render the conversation history"""
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
        """Render active agents status"""
        html = "<div style='padding: 15px;'>"
        html += "<h3>🤖 AI Team Status</h3>"
        
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
        phase = state.get("phase", "initial")
        
        phases = {
            "initial": ("🏁", "Getting Started", 0),
            "briefing": ("📝", "Gathering Requirements", 25),
            "strategy": ("🎯", "Creating Strategy", 50),
            "content": ("✍️", "Generating Content", 75),
            "execution": ("🚀", "Ready to Launch", 100)
        }
        
        current_phase = phases.get(phase, phases["initial"])
        icon, title, progress = current_phase
        
        return f"""
        <div style='padding: 15px;'>
            <h3>📊 Campaign Progress</h3>
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
    
    def _render_strategy(self, strategy: Optional[Dict] = None) -> str:
        """Render current strategy"""
        if not strategy:
            return """
            <div class="strategy-card">
                <h3>🎯 Campaign Strategy</h3>
                <p>Strategy will be created through our conversation. Start by telling us about your campaign goals!</p>
            </div>
            """
        
        strategy_data = strategy.get("strategy", {})
        
        return f"""
        <div class="strategy-card">
            <h3>🎯 {strategy_data.get('campaign_name', 'Campaign Strategy')}</h3>
            <p><strong>Summary:</strong> {strategy_data.get('executive_summary', 'No summary available')}</p>
            <p><strong>Target:</strong> {strategy_data.get('target_audience', {}).get('primary', 'Not defined')}</p>
            <p><strong>Channels:</strong> {', '.join(strategy_data.get('channel_strategy', {}).get('primary_channels', []))}</p>
        </div>
        """
    
    async def _process_user_message(self, message: str, state: Dict) -> Tuple[str, Dict]:
        """Process user message and generate appropriate AI response"""
        
        # Extract campaign information from message
        self._extract_campaign_data(message, state)
        
        # Determine conversation phase and active agents
        phase = state.get("phase", "initial")
        
        if phase == "initial" or phase == "briefing":
            # CEO handles initial briefing
            return await self._handle_briefing_phase(message, state)
        elif phase == "strategy":
            # Full team strategic meeting
            return await self._handle_strategy_phase(message, state)
        elif phase == "content":
            # Content creation phase
            return await self._handle_content_phase(message, state)
        else:
            # Default response
            return await self._handle_general_conversation(message, state)
    
    def _extract_campaign_data(self, message: str, state: Dict):
        """Extract campaign information from user message"""
        campaign_data = state.get("campaign_data", {})
        
        # Simple keyword extraction (could be enhanced with NLP)
        message_lower = message.lower()
        
        # Extract topic/product
        if not campaign_data.get("topic"):
            # Look for business/product indicators
            if any(word in message_lower for word in ["selling", "product", "service", "business", "company", "brand"]):
                # Extract the main subject
                words = message.split()
                for i, word in enumerate(words):
                    if word.lower() in ["selling", "for", "about", "promoting"]:
                        if i + 1 < len(words):
                            topic = " ".join(words[i+1:i+4])  # Take next 3 words
                            campaign_data["topic"] = topic
                            break
        
        # Extract target audience
        if any(word in message_lower for word in ["gen z", "millennials", "teens", "adults", "age", "target"]):
            if "gen z" in message_lower:
                campaign_data["target_audience"] = "Gen Z (18-25 years old)"
            elif "millennial" in message_lower:
                campaign_data["target_audience"] = "Millennials (26-40 years old)"
        
        # Extract budget hints
        if any(char in message for char in ["$", "€", "budget", "spend"]):
            # Extract budget (simplified)
            import re
            budget_match = re.search(r'[\$€]([0-9,]+)', message)
            if budget_match:
                campaign_data["budget"] = budget_match.group(0)
        
        state["campaign_data"] = campaign_data
    
    async def _handle_briefing_phase(self, message: str, state: Dict) -> Tuple[str, Dict]:
        """Handle the initial briefing conversation"""
        state["active_agents"] = ["ceo"]
        
        campaign_data = state.get("campaign_data", {})
        
        # Check if we have enough information for strategy
        if campaign_data.get("topic") and len(state["conversation_history"]) >= 3:
            # Ready to move to strategy phase
            state["phase"] = "strategy"
            
            # CEO introduces the team
            response = f"""
            Perfect! I have a clear picture of what you want to achieve. Let me bring in the rest of our AI marketing team for a strategic discussion.
            
            🎯 **Marcus** (Marketing Director) will analyze trends and consumer psychology
            🎨 **Sofia** (Creative Director) will develop the visual strategy  
            📊 **David** (Performance Manager) will focus on metrics and optimization
            
            Give us a moment to discuss your {campaign_data.get('topic', 'campaign')} and create a comprehensive strategy...
            """
            
            # Add typing indicator
            state["conversation_history"].append({
                "type": "agent",
                "agent": "ceo", 
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Simulate strategic meeting
            try:
                meeting_result = await self.orchestrator.simulate_strategic_meeting(campaign_data)
                state["current_strategy"] = meeting_result["final_strategy"]
                state["active_agents"] = ["ceo", "cmo", "creative_director", "performance_manager"]
                
                # CEO presents the strategy
                strategy_summary = self._format_strategy_summary(meeting_result)
                
                state["conversation_history"].append({
                    "type": "agent",
                    "agent": "ceo",
                    "content": f"🎉 **Strategy Complete!** Here's what our team has developed:\n\n{strategy_summary}\n\nWhat do you think? Should we proceed with content creation, or would you like to adjust anything?",
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                # Fallback response
                state["conversation_history"].append({
                    "type": "agent",
                    "agent": "ceo",
                    "content": f"I'm having a brief technical moment with the team meeting. Let me continue working on your {campaign_data.get('topic', 'campaign')} strategy and get back to you shortly!",
                    "timestamp": datetime.now().isoformat()
                })
        
        else:
            # Continue gathering information
            if not campaign_data.get("topic"):
                response = "I'd love to help you create something amazing! Could you tell me more about what you want to promote? Is it a product, service, event, or something else?"
            elif not campaign_data.get("target_audience"):
                response = f"Great! So you want to promote {campaign_data['topic']}. Who is your target audience? For example, are you targeting Gen Z, millennials, professionals, or a specific demographic?"
            else:
                response = f"Excellent! A {campaign_data['topic']} campaign for {campaign_data.get('target_audience', 'your audience')}. What's your main goal - brand awareness, sales, lead generation, or something else?"
            
            state["conversation_history"].append({
                "type": "agent",
                "agent": "ceo",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
        
        return "", state
    
    async def _handle_strategy_phase(self, message: str, state: Dict) -> Tuple[str, Dict]:
        """Handle strategy discussion and refinement"""
        # Move to content phase
        state["phase"] = "content"
        
        response = """
        🎨 **Sofia (Creative Director):** Perfect! I'm excited about this strategy. Let me start creating some content variations for you.
        
        📊 **David (Performance Manager):** I'll also run some performance predictions so we know what to expect.
        
        ✍️ Ready to see your content options!
        """
        
        state["conversation_history"].append({
            "type": "agent",
            "agent": "creative_director",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return "", state
    
    async def _handle_content_phase(self, message: str, state: Dict) -> Tuple[str, Dict]:
        """Handle content creation phase"""
        response = "🚀 Content creation is in progress! Our team is working on multiple variations for you to choose from."
        
        state["conversation_history"].append({
            "type": "agent",
            "agent": "creative_director",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return "", state
    
    async def _handle_general_conversation(self, message: str, state: Dict) -> Tuple[str, Dict]:
        """Handle general conversation"""
        response = "I'm here to help with your marketing campaigns! What would you like to work on today?"
        
        state["conversation_history"].append({
            "type": "agent",
            "agent": "ceo",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return "", state
    
    def _format_strategy_summary(self, meeting_result: Dict) -> str:
        """Format the strategy meeting results for display"""
        strategy = meeting_result.get("final_strategy", {}).get("strategy", {})
        
        if not strategy or isinstance(strategy, str):
            return "📋 **Comprehensive Strategy Created!** Our team has analyzed your requirements and developed a complete marketing approach. The strategy includes audience targeting, creative direction, channel optimization, and performance metrics."
        
        summary = f"""
        📋 **{strategy.get('campaign_name', 'Your Campaign')}**
        
        🎯 **Target Audience:** {strategy.get('target_audience', {}).get('primary', 'Defined')}
        
        💭 **Key Messages:**
        {self._format_list(strategy.get('key_messages', []))}
        
        📺 **Primary Channels:** {', '.join(strategy.get('channel_strategy', {}).get('primary_channels', []))}
        
        🎨 **Creative Style:** {strategy.get('creative_direction', {}).get('visual_style', 'Defined')}
        """
        
        return summary
    
    def _format_list(self, items: List[str], max_items: int = 3) -> str:
        """Format a list for display"""
        if not items:
            return "• Strategically defined"
        
        formatted = []
        for i, item in enumerate(items[:max_items]):
            formatted.append(f"• {item}")
        
        if len(items) > max_items:
            formatted.append(f"• And {len(items) - max_items} more...")
        
        return "\n".join(formatted)

# Create the interface
def create_conversational_interface() -> gr.Blocks:
    """Create and return the conversational interface"""
    interface = ConversationalInterface()
    return interface.create_interface()

if __name__ == "__main__":
    # Test the interface
    interface = create_conversational_interface()
    interface.launch(server_name="127.0.0.1", server_port=7861, share=False)
