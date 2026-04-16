import google.generativeai as genai
import os
import random
import asyncio

class GeminiEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye."
    )

    def __init__(self, google_api_key: str):
        self.api_key = google_api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            'gemini-pro',
            generation_config={
                "max_output_tokens": 100,
                "temperature": 0.8
            },
            system_instruction=self.SYSTEM_PROMPT
        )
        print("✅ Gemini Connected Successfully!")

    async def ask_question(self, message: str) -> str:
        try:
            clean_msg = (message or "").strip()[:1000]
            if not clean_msg:
                return "Kya bolna hai babu? 😘"
            
            # Gemini chat session maintain karne ke liye
            response = await asyncio.to_thread(
                self.model.generate_content,
                clean_msg
            )
            
            reply = response.text.strip()
            
            # Same validation logic
            if not reply or len(reply) < 2:
                return "Hmmm soch rahi hu babu! 💭"
            
            reply = reply.encode('utf-8', errors='ignore').decode('utf-8')
            reply = reply.replace('\n\n\n', '\n').strip()
            
            if len(reply) > 3800:
                reply = reply[:3800] + "... 💕"
            
            return f"❖ {reply}"
            
        except Exception as e:
            print(f"Gemini Error: {e}")
            fallbacks = [
                "Uff network slow hai babu! 😔",
                "Thoda wait karo darling 💕", 
                "Abhi busy hu, baad me baat! 😘"
            ]
            return random.choice(fallbacks)

# Initialize
try:
    from config import GOOGLE_API_KEY  # Config file me name change karo
    chatbot_api = GeminiEs(google_api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"❌ Gemini Init Error: {e}")
    chatbot_api = None
