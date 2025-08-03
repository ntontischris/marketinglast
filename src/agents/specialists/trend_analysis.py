import os
from dotenv import load_dotenv
from groq import Groq
import asyncio
from typing import Dict, Any

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
    print(f"ERROR in TrendAnalysisAgent: {e}")
    client = None

class TrendAnalysisAgent(EnhancedBaseAgent):
    """
    An agent that analyzes current and emerging trends for a given topic.
    """

    def __init__(self):
        super().__init__(name="Trend Analysis Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes trends for a given topic and adds a report to the state.

        Args:
            state: A dictionary containing the current state. 
                   Expected to have a 'topic' key.

        Returns:
            The updated state dictionary with a new 'trend_analysis_report' key.
        """
        topic = state.get("topic")

        if not client or not topic:
            error_message = f"Trend analysis skipped. Client configured: {bool(client)}, Topic provided: {bool(topic)}"
            print(f"ERROR: {error_message}")
            return {**state, "trend_analysis_report": "Trend analysis could not be performed."}

        print(f"-- '{self.name}' received topic: '{topic}'. Analyzing trends... --")

        prompt = (
            f"You are a world-class marketing and social media analyst. Your task is to analyze the topic: '{topic}'."
            f"Provide a detailed trend analysis in Greek. The analysis must include the following sections:"
            f"\n1. **Current & Emerging Trends:** Identify key trends related to the topic."
            f"\n2. **Seasonal Patterns:** Describe any seasonal variations or opportunities."
            f"\n3. **Content Opportunities:** Suggest specific content formats or ideas based on the trends (e.g., video series, blog posts, interactive polls)."
            f"\nPresent the output as a structured report in Greek."
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
            raw_report = chat_completion.choices[0].message.content

            # Parse the report to remove the <think> block and other noise.
            if "</think>" in raw_report:
                trend_report = raw_report.split("</think>", 1)[1].strip()
            else:
                trend_report = raw_report.strip()

            # Ensure the report starts with a markdown header
            if "###" in trend_report:
                trend_report = trend_report[trend_report.find("###"):]

            print("Successfully generated and parsed trend analysis report.")
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            trend_report = "Error: Could not generate trend report."

        # Update the state with the trend analysis report
        updated_state = {**state, "trend_analysis_report": trend_report}
        return updated_state

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
