import google.generativeai as genai
from openai import AsyncOpenAI
import os

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye."
    )

    def __init__(self, gemini_api_key: str, openai_api_key: str):
        # 1. Gemini Setup (Fastest and Safest Model)
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=self.SYSTEM_PROMPT
        )
        
        # 2. ChatGPT Setup (Fallback Mechanism)
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)

    async def ask_question(self, message: str) -> str:
        try:
            # First Try: Ask Gemini
            response = self.gemini_model.generate_content(message)
            return f"❖ {response.text.strip()}"
            
        except Exception as e:
            print(f"Gemini failed, switching to ChatGPT. Error: {e}")
            try:
                # Second Try (Fallback): Ask ChatGPT if Gemini fails
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": message}
                    ]
                )
                return f"❖ {response.choices[0].message.content.strip()}"
                
            except Exception:
                # If BOTH APIs fail
                return "Uff! Mera thoda network issue chal raha hai babu, thodi der baad baat karte hain! 😔"

# ==========================================
# UNIVERSAL AI OBJECT
# ==========================================
# Replace these strings with your actual API keys!
GEMINI_KEY = "AIzaSyBI3YVYcfn-fAYQRVWbpniBFyux_LZmut4"  # Starts with AIzaSy...
OPENAI_KEY = "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"  # Starts with sk-proj...

# Initialize the global AI brain
mahi_ai = ChatGptEs(gemini_api_key=GEMINI_KEY, openai_api_key=OPENAI_KEY)
