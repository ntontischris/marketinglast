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
    print(f"ERROR in PerformanceOptimizerAgent: {e}")
    client = None

class PerformanceOptimizerAgent(BaseAgent):
    """
    Performance optimizer agent that analyzes and refines content to optimize
    for engagement, reach, and conversions.
    """

    def __init__(self):
        super().__init__(name="Performance Optimizer Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    def invoke(self, state: dict) -> dict:
        """
        Analyzes the created content and provides recommendations for improving
        its performance based on metrics like engagement, reach, and conversions.

        Args:
            state: A dictionary containing the current state.
                   Expected to have 'final_content' and possibly other metrics.

        Returns:
            The updated state dictionary with performance recommendations.
        """
        final_content = state.get("final_content")

        if not client or not final_content:
            error_message = f"Performance optimization skipped. Client configured: {bool(client)}, Final content provided: {bool(final_content)}"
            print(f"ERROR: {error_message}")
            return {**state, "performance_recommendations": "Performance optimization could not be conducted."}

        print(f"-- '{self.name}' optimizing content performance --")

        prompt = (
            f"You are a top conversion rate and engagement specialist. Analyze the following content and provide actionable recommendations to improve its effectiveness.\n\n"
            f"Content: {final_content}\n\n"
            f"Provide recommendations in Greek that cover:\n\n"
            f"## 📊 Performance Metrics\n"
            f"- Engagement Rate\n"
            f"- Conversion Rate\n\n"
            f"## 💡 Optimization Suggestions\n"
            f"- Changes to Increase Engagement\n"
            f"- Best Practices for Calls to Action\n"
            f"- Visual Enhancements\n\n"
            f"## 🛠 Μετατροπές (Landing Page Optimization)\n"
            f"- Headline Revisions\n"
            f"- Image/Video Suggestions\n"
            f"- Audit tracking improvements\n\n"
            f"Ensure all responses are in Greek and include specific, measurable examples."
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
            raw_recommendations = chat_completion.choices[0].message.content

            # Clean the response
            if "\u003c/think\u003e" in raw_recommendations:
                performance_recommendations = raw_recommendations.split("\u003c/think\u003e", 1)[1].strip()
            else:
                performance_recommendations = raw_recommendations.strip()

            print("Successfully generated performance optimization recommendations.")
        except Exception as e:
            print(f"An error occurred while calling the Groq API: {e}")
            performance_recommendations = "Error: Could not generate performance recommendations."

        # Update the state with performance recommendations
        updated_state = {**state, "performance_recommendations": performance_recommendations}
        return updated_state
