import os
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent

# Load environment variables
load_dotenv()

# Configure the Groq API
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file or is empty.")
    client = Groq(api_key=api_key)
except (ValueError, KeyError) as e:
    print(f"ERROR in BrandVoiceAgent: {e}")
    client = None

class BrandVoiceAgent(EnhancedBaseAgent):
    """
    Brand voice agent that ensures consistent personality, tone, and messaging
    across all content while adapting to different audiences and channels.
    """

    def __init__(self):
        super().__init__(name="Brand Voice Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    async def _execute_core(self, state: dict) -> dict:
        """
        Analyzes the campaign strategy and creates a comprehensive brand voice guide
        that will be used by all content creation agents.

        Args:
            state: A dictionary containing the current state.
                   Expected to have 'topic', 'campaign_strategy' and other context.

        Returns:
            The updated state dictionary with brand voice guidelines.
        """
        topic = state.get("topic")
        campaign_strategy = state.get("campaign_strategy", "")

        if not client or not topic:
            error_message = f"Brand voice analysis skipped. Client configured: {bool(client)}, Topic provided: {bool(topic)}"
            print(f"ERROR: {error_message}")
            return {**state, "brand_voice_guide": "Brand voice guide could not be created."}

        print(f"-- '{self.name}' developing brand voice guidelines for: '{topic}' --")

        prompt = (
            f"You are a senior brand strategist specializing in voice and personality development. "
            f"Create a comprehensive brand voice guide for a campaign about: '{topic}'.\n\n"
            f"Campaign Strategy Context:\n{campaign_strategy}\n\n"
            f"Create a detailed brand voice guide in Greek that includes:\n\n"
            f"## 🎭 Προσωπικότητα Μάρκας\n"
            f"- 5 βασικές ιδιότητες προσωπικότητας (π.χ. φιλικός, καινοτόμος, αξιόπιστος)\n"
            f"- Τι είμαστε vs τι ΔΕΝ είμαστε\n"
            f"- Brand archetype που εκπροσωπούμε\n\n"
            f"## 🗣️ Τόνος Επικοινωνίας\n"
            f"- Γενικός τόνος (formality level, energy, approach)\n"
            f"- Προσαρμογές ανά κανάλι (social media vs email vs blog)\n"
            f"- Συναισθηματική απόχρωση\n\n"
            f"## 📝 Γλωσσικές Κατευθύνσεις\n"
            f"- Λεξιλόγιο που χρησιμοποιούμε (buzzwords, technical terms)\n"
            f"- Λεξιλόγιο που αποφεύγουμε\n"
            f"- Δομή προτάσεων (μακριές vs σύντομες)\n\n"
            f"## 💭 Messaging Framework\n"
            f"- Core value proposition σε μία πρόταση\n"
            f"- 3 βασικά pillars του messaging\n"
            f"- Call-to-action στυλ και προτιμήσεις\n\n"
            f"## 🎨 Δημιουργικές Κατευθύνσεις\n"
            f"- Στυλ περιεχομένου (storytelling, data-driven, inspirational)\n"
            f"- Χρήση emoji και visual elements\n"
            f"- Formatting preferences\n\n"
            f"## ✅ Παραδείγματα Do's & Don'ts\n"
            f"- 3 παραδείγματα σωστής επικοινωνίας\n"
            f"- 3 παραδείγματα λανθασμένης επικοινωνίας\n\n"
            f"Make it actionable and specific. All responses in Greek."
        )

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
            )
            raw_guide = chat_completion.choices[0].message.content

            # Clean the response
            if "</think>" in raw_guide:
                brand_voice_guide = raw_guide.split("</think>", 1)[1].strip()
            else:
                brand_voice_guide = raw_guide.strip()

            print("Successfully generated comprehensive brand voice guide.")
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            brand_voice_guide = "Error: Could not generate brand voice guide."

        # Update the state with the brand voice guide
        updated_state = {**state, "brand_voice_guide": brand_voice_guide}
        return updated_state

    # For backward compatibility with synchronous calls
    def invoke(self, state: dict) -> dict:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
