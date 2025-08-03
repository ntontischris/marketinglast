import os
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

# Load environment variables
load_dotenv()

# Configure the Groq API
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file or is empty.")
    client = Groq(api_key=api_key)
except (ValueError, KeyError) as e:
    print(f"ERROR in CampaignStrategistAgent: {e}")
    client = None

class CampaignStrategistAgent(BaseAgent):
    """
    Strategic agent that creates comprehensive campaign plans with target audience analysis,
    messaging strategy, and multi-channel approach.
    """

    def __init__(self):
        super().__init__(name="Campaign Strategist Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    def invoke(self, state: dict) -> dict:
        """
        Creates a comprehensive campaign strategy including target audience,
        messaging framework, and channel recommendations.

        Args:
            state: A dictionary containing the current state.
                   Expected to have 'topic' and optionally 'trend_analysis_report'.

        Returns:
            The updated state dictionary with campaign strategy components.
        """
        topic = state.get("topic")
        trend_report = state.get("trend_analysis_report", "")

        if not client or not topic:
            error_message = f"Campaign strategy skipped. Client configured: {bool(client)}, Topic provided: {bool(topic)}"
            print(f"ERROR: {error_message}")
            return {**state, "campaign_strategy": "Campaign strategy could not be created."}

        print(f"-- '{self.name}' developing comprehensive strategy for: '{topic}' --")

        prompt = (
            f"You are a world-class marketing strategist with 15+ years of experience. Create a comprehensive campaign strategy for the topic: '{topic}'.\n\n"
            f"Context from trend analysis:\n{trend_report}\n\n"
            f"Provide a detailed strategy in Greek that includes:\n\n"
            f"## 🎯 Στόχος Καμπάνιας\n"
            f"- Κύριος στόχος και επιθυμητά αποτελέσματα\n"
            f"- Μετρήσιμοι δείκτες επιτυχίας (KPIs)\n\n"
            f"## 👥 Ανάλυση Κοινού\n"
            f"- Πρωτεύον κοινό (demographics, interests, behaviors)\n"
            f"- Δευτερεύον κοινό\n"
            f"- Pain points και motivations\n\n"
            f"## 💬 Στρατηγική Μηνυμάτων\n"
            f"- Κεντρικό μήνυμα της καμπάνιας\n"
            f"- Τόνος και στυλ επικοινωνίας\n"
            f"- Βασικά σημεία προς επικοινωνία\n\n"
            f"## 📺 Κανάλια Διανομής\n"
            f"- Προτεινόμενα κανάλια (social media, email, blog, κλπ)\n"
            f"- Προτεραιότητες και resource allocation\n\n"
            f"## ⏰ Χρονοδιάγραμμα\n"
            f"- Φάσεις εκτέλεσης\n"
            f"- Βασικά milestones\n\n"
            f"Respond only in Greek with clear structure and actionable insights."
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
            raw_strategy = chat_completion.choices[0].message.content

            # Clean the response
            if "</think>" in raw_strategy:
                campaign_strategy = raw_strategy.split("</think>", 1)[1].strip()
            else:
                campaign_strategy = raw_strategy.strip()

            print("Successfully generated comprehensive campaign strategy.")
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            campaign_strategy = "Error: Could not generate campaign strategy."

        # Update the state with the campaign strategy
        updated_state = {**state, "campaign_strategy": campaign_strategy}
        return updated_state
