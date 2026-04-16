from openai import AsyncOpenAI
import os

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
