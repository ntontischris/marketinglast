import os
from dotenv import load_dotenv
import google.generativeai as genai

from src.agents.core.base_agent import BaseAgent

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file or is empty.")
    genai.configure(api_key=api_key)
    print("Google Gemini API configured successfully.")
except (ValueError, KeyError) as e:
    print(f"ERROR: {e}")
    # In a real app, you might want to exit or handle this more gracefully
    exit()

class ContentStrategyAgent(BaseAgent):
    """
    An agent that generates content ideas based on a given topic using the Google Gemini API.
    """

    def __init__(self):
        super().__init__(name="Content Strategy Agent")
        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized with Gemini 1.5 Flash Latest model.")

    def invoke(self, state: dict) -> dict:
        """
        Generates content ideas for a given topic.

        Args:
            state: A dictionary containing the current state. Expected to have a 'topic' key.

        Returns:
            The updated state dictionary with a new 'ideas' key.
        """
        topic = state.get("topic")
        if not topic:
            print("ERROR: 'topic' not found in state for ContentStrategyAgent.")
            return {**state, "ideas": "Error: Topic is required."}

        print(f"Generating content ideas for topic: '{topic}'")

        prompt = f"""
        You are a senior content strategist. Your task is to generate 5 creative and distinct content ideas for the following topic.
        For each idea, provide a short, catchy title.
        The output should be a simple list of ideas, with each idea on a new line.
        IMPORTANT: All output must be in Greek.

        TOPIC: {topic}

        IDEAS (in Greek):
        """

        try:
            response = self.model.generate_content(prompt)
            generated_ideas = response.text
            print("Successfully generated ideas from Gemini.")
        except Exception as e:
            print(f"An error occurred while calling the Gemini API: {e}")
            generated_ideas = f"Error generating ideas: {e}"

        # Update the state with the generated ideas
        updated_state = {**state, "ideas": generated_ideas}
        return updated_state
