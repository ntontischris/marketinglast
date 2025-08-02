import os
from dotenv import load_dotenv
import google.generativeai as genai

from src.agents.core.base_agent import BaseAgent

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=api_key)

class ContentWriterAgent(BaseAgent):
    """
    An agent that takes a specific content idea and writes a short draft for it.
    """

    def __init__(self):
        super().__init__(name="Content Writer Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'-- '{self.name}' initialized with Gemini 1.5 Flash Latest model. --")

    def invoke(self, state: dict) -> dict:
        """
        Generates a short content draft for a given topic and idea.

        Args:
            state: A dictionary containing the current state. 
                   Expected to have 'topic' and 'selected_idea' keys.

        Returns:
            A dictionary with the generated 'draft'.
        """
        topic = state.get("topic")
        idea = state.get("selected_idea")

        if not topic or not idea:
            raise ValueError("State must include 'topic' and 'selected_idea'")

        print(f"-- '{self.name}' received idea: '{idea}' for topic: '{topic}' --")

        prompt = (
            f"You are a creative content writer. Your task is to write a short, engaging social media post in Greek. "
            f"The main topic is '{topic}'. "
            f"Focus on the following specific idea: '{idea}'."
            f"Keep the post concise, around 2-3 paragraphs, and add a relevant emoji at the end."
            f"IMPORTANT: The entire output must be in Greek."
        )

        try:
            response = self.model.generate_content(prompt)
            draft = response.text
            print(f"-- '{self.name}' generated draft successfully. --")
        except Exception as e:
            print(f"An error occurred while generating content: {e}")
            draft = "Sorry, I couldn't generate a draft for this idea."

        return {"draft": draft}
