import os
from dotenv import load_dotenv
from groq import Groq

from src.agents.core.base_agent import BaseAgent

# Load environment variables from .env file
load_dotenv()

# Configure the Groq API
try:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file or is empty.")
    client = Groq(api_key=api_key)
    print("Groq API configured successfully.")
except (ValueError, KeyError) as e:
    print(f"ERROR: {e}")
    # In a real app, you might want to exit or handle this more gracefully
    exit()

class ContentStrategyAgent(BaseAgent):
    """
    An agent that generates content ideas based on a given topic using the Groq API.
    """

    def __init__(self):
        super().__init__(name="Content Strategy Agent")
        # Initialize the Groq model
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized with Groq model: {self.model_name}.")

    def invoke(self, state: dict) -> dict:
        """
        Generates content ideas for a given topic, taking into account current trends.

        Args:
            state: A dictionary containing the current state. 
                   Expected to have a 'topic' and optionally a 'trend_analysis_report' key.

        Returns:
            The updated state dictionary with a new 'ideas' key.
        """
        topic = state.get("topic")
        trend_report = state.get("trend_analysis_report")

        if not topic:
            print("ERROR: 'topic' not found in state for ContentStrategyAgent.")
            return {**state, "ideas": []}

        print(f"-- '{self.name}' received the topic. Generating ideas... --")

        # Build the prompt for the LLM, using the trend report if available
        prompt_context = f"Θέμα: {topic}\n"
        if trend_report:
            print("Trend analysis report found, using it for context.")
            prompt_context += f"\nΑναφορά Τάσεων:\n{trend_report}"

        prompt = (
            f"You are a world-class content strategist. Your task is to generate 5-7 distinct and creative content ideas based on the following topic and trend analysis. "
            f"Focus on ideas that are engaging, shareable, and aligned with the topic. Present the ideas as a numbered list. "
            f"The ideas should be specific and actionable. All output must be in Greek.\n\n"
            f"{prompt_context}"
            f"\n--- 5 CONTENT IDEAS (in Greek) ---"
        )

        ideas = []
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
            ideas_text = chat_completion.choices[0].message.content

            # Clean the response first
            if "</think>" in ideas_text:
                ideas_text = ideas_text.split("</think>", 1)[1].strip()
            
            # Use regex to find numbered or bulleted list items
            import re
            # This pattern looks for lines starting with a number and a dot, or a hyphen/asterisk.
            ideas = re.findall(r"^(?:\d+\.|- |\* )(.+)", ideas_text, re.MULTILINE)
            # Clean up any extra whitespace from the found ideas
            ideas = [idea.strip().replace('**', '') for idea in ideas]

            print(f"-- Successfully generated and parsed {len(ideas)} content ideas. --")

        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            ideas = []

        # Update the state with the parsed list of ideas
        updated_state = {**state, "ideas": ideas}
        return updated_state
    
    def _remove_thinking_tags(self, text: str) -> str:
        """Remove thinking tags and their content from the generated text."""
        import re
        # Remove content between <think> and </think> tags
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned.strip()
