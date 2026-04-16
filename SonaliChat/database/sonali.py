from openai import AsyncOpenAI
import os

# Test ChatGPT manually
python3
>>> from database.sonali import chatbot_api
>>> import asyncio
>>> asyncio.run(chatbot_api.ask_question("hi"))
'❖ Hii babu! 😘'  # Should return this
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
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.8
            )
            return f"❖ {response.choices[0].message.content.strip()}"
        except Exception:
            return "Uff! Network issue babu, thodi der baad try karo! 😔"

# Initialize
from config import OPENAI_API_KEY
chatbot_api = ChatGptEs(openai_api_key=OPENAI_API_KEY)

async def ask_question(self, message: str) -> str:
    try:
        response = await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": message[:1000]}  # Limit input
            ],
            max_tokens=100,  # Reduced tokens
            temperature=0.7
        )
        
        # ✅ CRITICAL FIXES
        reply = response.choices[0].message.content.strip()
        
        # Check empty response
        if not reply or len(reply.strip()) == 0:
            return "Aww babu, thoda soch rahi hu! 😘"
        
        # Remove invalid chars
        reply = reply.encode('utf-8', errors='ignore').decode('utf-8')
        reply = reply.replace('\n\n', '\n').strip()
        
        # Telegram safe length
        if len(reply) > 4000:
            reply = reply[:4000] + "... 💕"
            
        return f"❖ {reply}"
        
    except Exception as e:
        print(f"ChatGPT Error: {e}")
        return "Kya hua babu? Network slow hai! Thoda wait karo 😔"
