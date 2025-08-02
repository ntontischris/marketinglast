import google.generativeai as genai
from ..core.base_agent import BaseAgent

class TwitterAgent(BaseAgent):
    """An agent that specializes in adapting content for Twitter."""
    def __init__(self):
        super().__init__(name="Twitter Specialist Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized.")

    def invoke(self, state: dict) -> dict:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a Twitter marketing expert. Your task is to adapt the following content for a Twitter post. "
            f"Keep it concise, under 280 characters, and add 2-3 relevant and popular hashtags. "
            f"Maintain a professional but engaging tone.\n\n" 
            f"Original Content:\n\"{original_draft}\"\n\n" 
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized Twitter Post (in Greek):"
        )

        response = self.model.generate_content(prompt)
        specialized_draft = response.text
        return {"specialized_draft": specialized_draft}


class InstagramAgent(BaseAgent):
    """An agent that specializes in adapting content for Instagram."""
    def __init__(self):
        super().__init__(name="Instagram Specialist Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized.")

    def invoke(self, state: dict) -> dict:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are an Instagram marketing expert. Your task is to adapt the following content for an Instagram post. "
            f"Focus on creating a visually appealing and engaging caption. "
            f"Start with a strong hook, use emojis to break up the text, and include 5-7 relevant and trending hashtags. "
            f"Also, suggest a type of visual (e.g., 'Image: A vibrant photo of...', 'Video: A short clip showing...') that would accompany this post.\n\n" 
            f"Original Content:\n\"{original_draft}\"\n\n" 
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized Instagram Post (Caption and Visual Suggestion in Greek):"
        )

        response = self.model.generate_content(prompt)
        specialized_draft = response.text
        return {"specialized_draft": specialized_draft}


class FacebookAgent(BaseAgent):
    """An agent that adapts a draft for Facebook, aiming for slightly longer, more engaging posts."""
    def __init__(self):
        super().__init__(name="Facebook Specialist Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized.")

    def invoke(self, state: dict) -> dict:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a Facebook marketing expert. Your task is to adapt the following draft for a Facebook post. "
            f"The tone should be engaging and conversational. Feel free to expand on the idea, ask a question to encourage comments, and include relevant emojis. Keep it under 150 words.\n\n"
            f"Original Draft:\n\"{original_draft}\"\n\n"
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized Facebook Post (in Greek):"
        )

        response = self.model.generate_content(prompt)
        specialized_draft = response.text
        return {"specialized_draft": specialized_draft}


class TikTokAgent(BaseAgent):
    """An agent that creates a TikTok video script from a draft."""
    def __init__(self):
        super().__init__(name="TikTok Specialist Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized.")

    def invoke(self, state: dict) -> dict:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a TikTok content strategist. Your task is to create a short, punchy TikTok video script based on the following draft. "
            f"The script should be for a 15-20 second video. Provide a scene-by-scene description, suggest on-screen text, and recommend a trending audio style (e.g., 'upbeat pop,' 'inspirational voiceover').\n\n"
            f"Original Draft:\n\"{original_draft}\"\n\n"
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized TikTok Script (Scene-by-scene in Greek):"
        )

        response = self.model.generate_content(prompt)
        specialized_draft = response.text
        return {"specialized_draft": specialized_draft}


class BlogWriterAgent(BaseAgent):
    """An agent that writes a full, SEO-optimized blog post from a draft."""
    def __init__(self):
        super().__init__(name="Blog Writer Agent")
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print(f"'{self.name}' initialized.")

    def invoke(self, state: dict) -> dict:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a professional blog writer and SEO expert. Your task is to expand the following draft into a complete, well-structured, and SEO-optimized blog post of at least 400 words. "
            f"The blog post must include: \n"
            f"1. An engaging, keyword-rich Title.\n"
            f"2. An introduction that hooks the reader.\n"
            f"3. A body with at least two H2 subheadings.\n"
            f"4. A concluding paragraph that summarizes the key points and includes a call-to-action.\n"
            f"5. A suggestion for a meta description (under 160 characters).\n\n"
            f"Draft to Expand:\n\"{original_draft}\"\n\n"
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Full SEO-Optimized Blog Post (in Greek):"
        )

        response = self.model.generate_content(prompt)
        specialized_draft = response.text
        return {"specialized_draft": specialized_draft}
