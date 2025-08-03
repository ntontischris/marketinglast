import gradio as gr
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Προσθήκη του root φακέλου στο path για σωστές εισαγωγές
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.core.orchestrator import OrchestratorAgent

class MarketingAIInterface:
    """Προηγμένο interface του Gradio για το Σύστημα Μάρκετινγκ AI."""
    
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.session_state: Dict[str, Any] = {}

    def get_available_agents(self) -> str:
        """Επιστρέφει μια λίστα με τους διαθέσιμους agents του συστήματος."""
        agent_list = ""
        for agent_name, agent_instance in self.orchestrator.__dict__.items():
            if agent_name.endswith('_agent'):
                # Λήψη του docstring ή μιας προεπιλεγμένης περιγραφής
                doc = agent_instance.__doc__ or ""
                description = doc.strip().split('\n')[0]
                agent_list += f"- **{agent_instance.name}:** {description}\n"
        return agent_list

    def analyze_trends(self, topic: str) -> Tuple[str, str]:
        """Αναλύει τις τάσεις για ένα δεδομένο θέμα."""
        if not topic.strip():
            return "❌ Παρακαλώ δώστε ένα θέμα.", ""
        
        self.session_state = {"topic": topic}
        state_with_trends = self.orchestrator.trend_analysis_agent.invoke(self.session_state)
        self.session_state.update(state_with_trends)
        
        report = self.session_state.get("trend_analysis_report", "Δεν ήταν δυνατή η δημιουργία αναφοράς.")
        return "✅ Η ανάλυση τάσεων ολοκληρώθηκε!", report

    def generate_content_ideas(self) -> Tuple[str, gr.update]:
        """Δημιουργεί ιδέες περιεχομένου βάσει του θέματος και των τάσεων."""
        if "topic" not in self.session_state:
            return "❌ Ξεκινήστε με την ανάλυση τάσεων.", gr.update(choices=[], value=None)
        
        state_with_ideas = self.orchestrator.content_strategy_agent.invoke(self.session_state)
        self.session_state.update(state_with_ideas)
        ideas = self.session_state.get("ideas", [])
        
        if not ideas:
            return "😕 Δεν βρέθηκαν ιδέες. Δοκιμάστε διαφορετικό θέμα.", gr.update(choices=[], value=None)
            
        return f"✅ Βρέθηκαν {len(ideas)} ιδέες!", gr.update(choices=ideas, value=ideas[0] if ideas else None)

    def create_final_content(self, selected_idea: str) -> Tuple[str, str]:
        """Δημιουργεί το τελικό περιεχόμενο βάσει της επιλεγμένης ιδέας."""
        if not selected_idea:
            return "❌ Παρακαλώ επιλέξτε μια ιδέα.", ""
        
        self.session_state["selected_idea"] = selected_idea
        final_state = self.orchestrator.content_writer_agent.invoke(self.session_state)
        self.session_state.update(final_state)
        final_content = self.session_state.get("final_content", "")
        
        return "✅ Το περιεχόμενο δημιουργήθηκε!", final_content

    def generate_visuals(self) -> Tuple[str, str, gr.update]:
        """Δημιουργεί προτάσεις για οπτικά."""
        if "final_content" not in self.session_state:
            return "❌ Δημιουργήστε πρώτα το περιεχόμενο.", "", gr.update(choices=[], value=None)
        
        state_with_visuals = self.orchestrator.visual_suggestion_agent.invoke(self.session_state)
        self.session_state.update(state_with_visuals)
        suggestions = self.session_state.get("visual_suggestions", [])
        
        if not suggestions:
            return "😕 Δεν βρέθηκαν ιδέες για οπτικά.", "", gr.update(choices=[], value=None)
        
        formatted_suggestions = ""
        prompts = []
        for i, sug in enumerate(suggestions):
            formatted_suggestions += f"### 🎨 Ιδέα {i+1}\n**Περιγραφή:** {sug['description']}\n**Prompt:** `{sug['prompt']}`\n\n"
            prompts.append(sug['prompt'])
        
        return "✅ Οι ιδέες για οπτικά δημιουργήθηκαν!", formatted_suggestions, gr.update(choices=prompts, value=prompts[0] if prompts else None)

    def generate_image(self, prompt: str) -> Tuple[str, str]:
        """Δημιουργεί μια εικόνα βάσει του επιλεγμένου prompt."""
        if not prompt:
            return "❌ Επιλέξτε ένα prompt.", None
        
        image_state = self.orchestrator.image_generation_agent.invoke({"image_prompt": prompt})
        image_path = image_state.get("image_path", "Η δημιουργία απέτυχε.")
        
        if os.path.exists(image_path):
            return "✅ Η εικόνα δημιουργήθηκε!", image_path
        return "❌ Αποτυχία δημιουργίας εικόνας.", None

def create_gradio_interface():
    """Δημιουργεί και ρυθμίζει το interface του Gradio."""
    app = MarketingAIInterface()
    
    # Φόρτωση του CSS
    css_path = os.path.join(os.path.dirname(__file__), "static", "theme.css")
    css = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

    with gr.Blocks(theme=gr.themes.Soft(), css=css, title="AI Marketing Generator") as interface:
        # Header
        gr.HTML("""
        <div class='section-header'>
            <h1>🤖 AI Marketing Content Generator</h1>
            <p>Ο έξυπνος συνεργάτης σας για τη δημιουργία εκπληκτικών καμπανιών μάρκετινγκ.</p>
        </div>
        """)

        with gr.Tabs():
            # Καρτέλα Κύριας Ροής
            with gr.TabItem("🚀 Δημιουργία Καμπάνιας"):
                with gr.Row():
                    # Αριστερή Στήλη: Είσοδοι & Ενέργειες
                    with gr.Column(scale=1):
                        # Βήμα 1: Ανάλυση Τάσεων
                        gr.HTML('<div class="step-header"><h3>Βήμα 1: Θέμα & Ανάλυση Τάσεων</h3></div>')
                        topic_input = gr.Textbox(label="💡 Κεντρικό Θέμα Καμπάνιας", placeholder="π.χ. 'Βιώσιμη μόδα', 'Vegan συνταγές'...")
                        trends_btn = gr.Button("📈 Ανάλυση Τάσεων", variant="primary")
                        
                        # Βήμα 2: Δημιουργία Ιδεών
                        gr.HTML('<div class="step-header"><h3>Βήμα 2: Δημιουργία Ιδεών</h3></div>')
                        ideas_btn = gr.Button("💡 Δημιουργία Ιδεών", variant="primary")
                        ideas_dropdown = gr.Dropdown(label="🧠 Επιλογή Ιδέας", choices=[], interactive=True)
                        
                        # Βήμα 3: Δημιουργία Περιεχομένου
                        gr.HTML('<div class="step-header"><h3>Βήμα 3: Δημιουργία Περιεχομένου</h3></div>')
                        content_btn = gr.Button("✍️ Δημιουργία Περιεχομένου", variant="primary")
                        
                        # Βήμα 4: Δημιουργία Οπτικών
                        gr.HTML('<div class="step-header"><h3>Βήμα 4: Δημιουργία Οπτικών</h3></div>')
                        visuals_btn = gr.Button("🎨 Δημιουργία Ιδεών για Οπτικά", variant="primary")
                        visual_prompt_dropdown = gr.Dropdown(label="🖼️ Επιλογή Prompt για Εικόνα", choices=[], interactive=True)
                        image_btn = gr.Button("🏞️ Δημιουργία Εικόνας", variant="primary")

                    # Δεξιά Στήλη: Έξοδοι & Αποτελέσματα
                    with gr.Column(scale=2):
                        status_textbox = gr.Textbox(label="ℹ️ Κατάσταση", interactive=False)
                        
                        # Περιοχή Εξόδου με Καρτέλες
                        with gr.Tabs():
                            with gr.TabItem("📊 Αναφορά Τάσεων"):
                                trends_output = gr.Markdown()
                            with gr.TabItem("📝 Τελικό Περιεχόμενο"):
                                final_content_output = gr.Markdown()
                            with gr.TabItem("🎨 Προτάσεις Οπτικών"):
                                visual_suggestions_output = gr.Markdown()
                            with gr.TabItem("🖼️ Τελική Εικόνα"):
                                final_image_output = gr.Image(type="filepath", label="Η εικόνα σας")

                # Συνδέσεις των κουμπιών με τις συναρτήσεις
                trends_btn.click(
                    app.analyze_trends,
                    inputs=[topic_input],
                    outputs=[status_textbox, trends_output]
                )

                ideas_btn.click(
                    app.generate_content_ideas,
                    outputs=[status_textbox, ideas_dropdown]
                )

                content_btn.click(
                    app.create_final_content,
                    inputs=[ideas_dropdown],
                    outputs=[status_textbox, final_content_output]
                )

                def update_visual_prompts(status, _, prompts_update):
                    return status, prompts_update

                visuals_btn.click(
                    app.generate_visuals,
                    outputs=[status_textbox, visual_suggestions_output, visual_prompt_dropdown]
                ).then(
                    update_visual_prompts,
                    inputs=[status_textbox, visual_suggestions_output, visual_prompt_dropdown],
                    outputs=[status_textbox, visual_prompt_dropdown]
                )

                image_btn.click(
                    app.generate_image,
                    inputs=[visual_prompt_dropdown],
                    outputs=[status_textbox, final_image_output]
                )

            # Καρτέλα "About"
            with gr.TabItem("ℹ️ About"):
                gr.HTML('<div class="step-header"><h3>Οι Agents του Συστήματος</h3></div>')
                available_agents_md = gr.Markdown()
                interface.load(app.get_available_agents, None, available_agents_md)

        # Footer
        gr.HTML("""
        <div class='footer'>
            <p><strong>🤖 AI Marketing Content Generator</strong></p>
            <p>Powered by Groq • Gradio • Windsurf</p>
        </div>
        """)
    
    return interface

if __name__ == "__main__":
    demo = create_gradio_interface()
    # Try different ports if 7860 is occupied
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
        print("❌ Δεν βρέθηκε διαθέσιμη θύρα. Δοκιμάστε να κλείσετε άλλες εφαρμογές.")
        exit(1)
    
    print(f"🚀 Εκκίνηση του AI Marketing System στη θύρα {port}...")
    print(f"🔗 Ανοίξτε τον browser σας και πηγαίνετε στο: http://127.0.0.1:{port}")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        debug=False,
        show_error=True,
        quiet=False
    )
