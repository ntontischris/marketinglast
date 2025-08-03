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
    print(f"ERROR in VisualSuggestionAgent: {e}")
    client = None

class VisualSuggestionAgent(EnhancedBaseAgent):
    """
    An agent that analyzes final text content and suggests visual ideas.
    """

    def __init__(self):
        super().__init__(name="Visual Suggestion Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    async def _execute_core(self, state: dict) -> dict:
        """
        Generates visual ideas based on the final content.

        Args:
            state: A dictionary containing the current state.
                   Expected to have a 'final_content' key.

        Returns:
            The updated state with a new 'visual_suggestions' key.
        """
        final_content = state.get("final_content")

        if not final_content:
            print("ERROR in VisualSuggestionAgent: 'final_content' not found in state.")
            return {**state, "visual_suggestions": "Error: Final content is required to suggest visuals."}

        print(f"-- '{self.name}' received content to analyze for visuals. --")

        prompt = (
            f"You are an expert creative director for social media. Your task is to suggest visual ideas for a post. "
            f"Analyze the following text and provide exactly 3 distinct, creative, and actionable visual concepts. "
            f"For each concept, provide a 'description' and a 'prompt' for an AI image generator like DALL-E. "
            f"Format EACH idea STRICTLY as follows, using '||' as a separator: "
            f"description: [Your detailed description in Greek]||prompt: [Your ready-to-use prompt in English]"
            f"Separate each of the 3 complete ideas with a newline."
            f"\n--- POST TEXT ---\n{final_content}\n\n--- VISUAL IDEAS ---"
        )

        if not client:
            return {**state, "visual_suggestions": "VisualSuggestionAgent is not configured due to API key error."}

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
            raw_suggestions = chat_completion.choices[0].message.content
            suggestions = []
            for line in raw_suggestions.strip().split('\n'):
                if '||' in line:
                    try:
                        desc_part, prompt_part = line.split('||', 1)
                        description = desc_part.replace('description:', '').strip()
                        prompt_text = prompt_part.replace('prompt:', '').strip()
                        if description and prompt_text:
                            suggestions.append({"description": description, "prompt": prompt_text})
                    except ValueError:
                        print(f"-- Warning: Could not parse line: {line} --")
                        continue
            print(f"-- '{self.name}' generated and parsed {len(suggestions)} visual suggestions successfully. --")
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            suggestions = [] # Return empty list on error

        updated_state = {**state, "visual_suggestions": suggestions}
        return updated_state

    # For backward compatibility with synchronous calls
    def invoke(self, state: dict) -> dict:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
