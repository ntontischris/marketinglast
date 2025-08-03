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
    print(f"ERROR in ClientBriefingAgent: {e}")
    client = None

class ClientBriefingAgent(EnhancedBaseAgent):
    """
    An agent that conducts a dialogue with the user to create a detailed creative brief.
    """

    def __init__(self):
        super().__init__(name="Client Briefing Agent")
        self.model_name = 'deepseek-r1-distill-llama-70b'
        if client:
            print(f"'-- '{self.name}' initialized with Groq model: {self.model_name}. --")
        else:
            print(f"'-- '{self.name}' failed to initialize due to API key error. --")

    async def _execute_core(self, state: dict) -> dict:
        """
        Conducts a Q&A with the user to define the campaign goals.
        """
        initial_topic = state.get("topic")
        if not client:
            return {**state, "creative_brief": f"Briefing failed. {self.name} is not configured."}

        print("\n--- 🤝 مرحباً! أنا مساعدك الاستراتيجي. لنتحدث عن حملتك. ---")
        print(f"الموضوع الأولي هو: '{initial_topic}'.")

        conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are an expert marketing strategist conducting a client interview. Your goal is to create a 'Creative Brief'. "
                    "Start by asking an opening question based on the user's initial topic. Then, continue asking clarifying questions one by one based on the user's answers. "
                    "Your questions should be natural and conversational. Aim to understand the Goal, Target Audience, Key Message, Call to Action, and Tone. "
                    "Once you are confident you have enough information, output the exact phrase 'BRIEF_READY' and nothing else. All your questions must be in Greek."
                )
            },
            {
                "role": "user",
                "content": f"Το αρχικό μου θέμα είναι: {initial_topic}"
            }
        ]

        # Conversational loop
        for _ in range(6): # Max 6 turns to prevent infinite loops
            chat_completion = client.chat.completions.create(
                messages=conversation_history,
                model=self.model_name,
            )
            ai_response = chat_completion.choices[0].message.content.strip()

            if ai_response == "BRIEF_READY":
                print("\n🤖 Ευχαριστώ! Έχω όλες τις πληροφορίες που χρειάζομαι.")
                break

            # Ask the question and get user's answer
            conversation_history.append({"role": "assistant", "content": ai_response})
            user_answer = input(f"\n🤖 {ai_response}\n> ")
            conversation_history.append({"role": "user", "content": user_answer})
        else:
             print("\n🤖 Έχουμε φτάσει στο όριο των ερωτήσεων. Θα προχωρήσω με τις πληροφορίες που έχω.")

        print("\n-----------------------------------------------------")
        print("Αναλύω τη συζήτησή μας για να δημιουργήσω την τελική σύνοψη...")

        # Create the final brief by sending a new, clean request
        synthesis_messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior marketing strategist. Based on the entire conversation history with a client that follows, create a concise 'Creative Brief'. "
                    "The brief must be in Greek and should summarize the campaign's main goal, target audience, key message, call to action, and desired tone. "
                    "Present it as a clean, well-structured summary, not a conversation. Do not include the user's answers verbatim. Synthesize them into a professional brief."
                )
            }
        ]
        # Add the full conversation history for context
        synthesis_messages.extend(conversation_history)

        try:
            chat_completion = client.chat.completions.create(
                messages=synthesis_messages,
                model=self.model_name,
            )
            creative_brief = chat_completion.choices[0].message.content

            print("\n--- 📝 Η Σύνοψη της Στρατηγικής μας ---")
            print(creative_brief)
            print("-----------------------------------------")

            confirmation = input("Είστε ικανοποιημένος με αυτή την κατεύθυνση; (ναι/οχι): ").strip().lower()

            if confirmation == 'ναι':
                print("Τέλεια! Προχωράμε με βάση αυτό το πλάνο.")
                return {**state, "creative_brief": creative_brief, "topic": initial_topic}
            else:
                print("Κατανοητό. Ας δοκιμάσουμε ξανά από την αρχή.")
                return await self._execute_core(state) # Recursive call to restart the process

        except Exception as e:
            print(f"An error occurred during brief synthesis: {e}")
            return {**state, "creative_brief": "Error: Could not create brief."}

    # For backward compatibility with synchronous calls
    def invoke(self, state: dict) -> dict:
        """Synchronous wrapper for backward compatibility"""
        return self(state)
