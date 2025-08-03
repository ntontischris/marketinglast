import os
from dotenv import load_dotenv
from groq import Groq
import asyncio
from typing import Dict, Any

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent

# Load environment variables
load_dotenv()

# Configure the Groq API
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")
client = Groq(api_key=api_key)

class ContentWriterAgent(EnhancedBaseAgent):
    """
    An agent that takes a specific content idea and writes a short draft for it.
    """

    def __init__(self):
        super().__init__(name="Content Writer Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a short content draft for a given topic and a selected idea.

        Args:
            state: A dictionary containing the current state. 
                   Expected to have 'topic' and 'selected_idea' keys.

        Returns:
            The updated state with the generated 'final_content'.
        """
        topic = state.get("topic")
        idea = state.get("selected_idea")

        if not topic or not idea:
            print("ERROR in ContentWriterAgent: State must include 'topic' and 'selected_idea'.")
            return {**state, "final_content": "Error: Missing topic or selected idea for the writer."}

        print(f"-- '{self.name}' received idea: '{idea}' for topic: '{topic}' --")

        prompt = (
            f"You are a creative content writer. Your task is to write a short, engaging social media post in Greek. "
            f"The main topic is '{topic}'. "
            f"Focus on the following specific idea: '{idea}'."
            f"Keep the post concise, around 2-3 paragraphs, and add a relevant emoji at the end."
            f"IMPORTANT: The entire output must be in Greek."
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
            final_content = chat_completion.choices[0].message.content
            print(f"-- '{self.name}' generated final content successfully. --")
        except Exception as e:
            print(f"An error occurred while generating content: {e}")
            final_content = "Sorry, I couldn't generate a draft for this idea."

        # Add the final content to the state and return
        updated_state = {**state, "final_content": final_content}
        return updated_state

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
