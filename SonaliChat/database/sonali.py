from openai import AsyncOpenAI
import os
import random

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye."
    )

    def __init__(self, openai_api_key: str):
        self.openai_client = AsyncOpenAI(
            api_key=openai_api_key,
            timeout=30.0,
            max_retries=2
        )

    async def ask_question(self, message: str) -> str:
        try:
            clean_msg = (message or "").strip()[:1000]
            if not clean_msg:
                return "Kya bolna hai babu? 😘"
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": clean_msg}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            reply = response.choices[0].message.content.strip()
            if not reply or len(reply) < 2:
                return "Hmmm soch rahi hu babu! 💭"
            
            reply = reply.encode('utf-8', errors='ignore').decode('utf-8')
            reply = reply.replace('\n\n\n', '\n').strip()
            
            if len(reply) > 3800:
                reply = reply[:3800] + "... 💕"
            
            return f"❖ {reply}"
            
        except Exception as e:
            print(f"ChatGPT Error: {e}")
            fallbacks = [
                "Uff network slow hai babu! 😔",
                "Thoda wait karo darling 💕", 
                "Abhi busy hu, baad me baat! 😘"
            ]
            return random.choice(fallbacks)

# Initialize
try:
    from config import OPENAI_API_KEY
    chatbot_api = ChatGptEs(openai_api_key=OPENAI_API_KEY)
    print("✅ ChatGPT Connected Successfully!")
except Exception as e:
    print(f"❌ ChatGPT Init Error: {e}")
    chatbot_api = None
