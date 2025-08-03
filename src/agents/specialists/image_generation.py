import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from src.agents.core.enhanced_base_agent import EnhancedBaseAgent

# Load environment variables
load_dotenv()

# Configure the OpenAI API
try:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or is empty.")
    client = OpenAI(api_key=api_key)
except (ValueError, KeyError) as e:
    print(f"ERROR in ImageGenerationAgent: {e}")
    client = None

class ImageGenerationAgent(EnhancedBaseAgent):
    """
    An agent that generates an image based on a prompt using DALL-E 3.
    """

    def __init__(self):
        super().__init__(name="Image Generation Agent")
        if client:
            print(f"'-- '{self.name}' initialized with OpenAI DALL-E 3. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    async def _execute_core(self, state: dict) -> dict:
        """
        Generates and saves an image.

        Args:
            state: A dictionary containing the current state.
                   Expected to have an 'image_prompt' key.

        Returns:
            The updated state with a new 'image_path' key.
        """
        image_prompt = state.get("image_prompt")

        if not client:
            return {**state, "image_path": "Error: ImageGenerationAgent is not configured."}

        if not image_prompt:
            print("ERROR in ImageGenerationAgent: 'image_prompt' not found in state.")
            return {**state, "image_path": "Error: Image prompt is required."}

        print(f"-- '{self.name}' received prompt. Generating image... --")

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            print(f"-- Image generated successfully. Downloading from URL... --")

            # Download and save the image
            image_data = requests.get(image_url).content
            output_dir = "output/images"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(output_dir, f"generated_image_{timestamp}.png")
            
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            print(f"-- Image saved successfully to: {file_path} --")
            return {**state, "image_path": file_path}

        except Exception as e:
            print(f"An error occurred during image generation or download: {e}")
            return {**state, "image_path": f"Error: {e}"}

    # For backward compatibility with synchronous calls
    def invoke(self, state: dict) -> dict:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
