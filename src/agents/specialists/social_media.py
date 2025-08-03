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

class SocialMediaAgent(EnhancedBaseAgent):
    """A unified social media agent that coordinates platform-specific content optimization."""
    
    def __init__(self):
        super().__init__(name="Social Media Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        self.platform_agents = {
            'twitter': TwitterAgent(),
            'instagram': InstagramAgent(),
            'facebook': FacebookAgent(),
            'tiktok': TikTokAgent(),
            'blog': BlogWriterAgent()
        }
        print(f"'{self.name}' initialized with {len(self.platform_agents)} platform agents.")
    
    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content for specified social media platforms."""
        content = state.get("content", [])
        platforms = state.get("platforms", ["instagram", "facebook"])
        
        if not content:
            raise ValueError("State must include 'content'")
        
        optimized_content = []
        
        for content_piece in content:
            platform_results = {}
            
            for platform in platforms:
                if platform.lower() in self.platform_agents:
                    agent = self.platform_agents[platform.lower()]
                    platform_state = {
                        "draft": content_piece.get("content", ""),
                        "platform": platform
                    }
                    
                    try:
                        result = agent.invoke(platform_state)
                        platform_results[platform] = result.get("specialized_draft", "")
                    except Exception as e:
                        platform_results[platform] = f"Error optimizing for {platform}: {str(e)}"
            
            optimized_content.append({
                "original_content": content_piece,
                "platform_optimizations": platform_results
            })
        
        return {"optimized_content": optimized_content}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)


class TwitterAgent(EnhancedBaseAgent):
    """An agent that specializes in adapting content for Twitter."""
    def __init__(self):
        super().__init__(name="Twitter Specialist Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized.")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
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

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        specialized_draft = chat_completion.choices[0].message.content
        return {"specialized_draft": specialized_draft}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)


class InstagramAgent(EnhancedBaseAgent):
    """An agent that specializes in adapting content for Instagram."""
    def __init__(self):
        super().__init__(name="Instagram Specialist Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized.")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
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

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        specialized_draft = chat_completion.choices[0].message.content
        return {"specialized_draft": specialized_draft}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)


class FacebookAgent(EnhancedBaseAgent):
    """An agent that adapts a draft for Facebook, aiming for slightly longer, more engaging posts."""
    def __init__(self):
        super().__init__(name="Facebook Specialist Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized.")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
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

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        specialized_draft = chat_completion.choices[0].message.content
        return {"specialized_draft": specialized_draft}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)


class TikTokAgent(EnhancedBaseAgent):
    """An agent that specializes in adapting content for TikTok."""
    def __init__(self):
        super().__init__(name="TikTok Specialist Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized.")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a TikTok marketing expert. Your task is to adapt the following content for a TikTok video. "
            f"Create an engaging hook for the first 3 seconds, describe the video concept, and include trending hashtags. "
            f"Focus on creating viral, entertaining content that encourages engagement.\n\n"
            f"Original Content:\n\"{original_draft}\"\n\n"
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized TikTok Video Script (in Greek):"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        specialized_draft = chat_completion.choices[0].message.content
        return {"specialized_draft": specialized_draft}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)


class BlogWriterAgent(EnhancedBaseAgent):
    """An agent that specializes in creating blog content."""
    def __init__(self):
        super().__init__(name="Blog Writer Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        print(f"'{self.name}' initialized.")

    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        original_draft = state.get("draft")
        if not original_draft:
            raise ValueError("State must include 'draft'")

        prompt = (
            f"You are a professional blog writer. Your task is to expand the following content into a well-structured blog post. "
            f"Create an engaging introduction, develop the main points with clear sections, and provide a compelling conclusion. "
            f"Use a conversational yet informative tone, include subheadings, and aim for 300-500 words.\n\n"
            f"Original Content:\n\"{original_draft}\"\n\n"
            f"IMPORTANT: The entire output must be in Greek.\n"
            f"Optimized Blog Post (in Greek):"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        specialized_draft = chat_completion.choices[0].message.content
        return {"specialized_draft": specialized_draft}

    # For backward compatibility with synchronous calls
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
