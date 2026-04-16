import ollama
import random
import asyncio
from typing import Optional

class OllamaEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek AI girlfriend jo short, sweet, Hinglish replies deti hai. "
        "Thoda flirty, emotional, fun. Har reply 1-2 sentences me."
    )

    def __init__(self):
        self.model = "llama3.2"  # Local model name
        
    async def ask_question(self, message: str) -> str:
        try:
            clean_msg = message.strip()[:500]
            if not clean_msg:
                return "Kya bolna hai babu? 😘"
            
            # Ollama chat (FREE - No API key!)
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": clean_msg}
                ],
                options={
                    "temperature": 0.8,
                    "num_predict": 100
                }
            )
            
            reply = response['message']['content'].strip()
            
            # Clean & limit
            if len(reply) > 2000:
                reply = reply[:2000] + " 💕"
            
            return f"❖ {reply}" if reply else "Hmmm soch rahi hu! 💭"
            
        except Exception as e:
            print(f"Ollama Error: {e}")
            fallbacks = [
                "Uff network slow hai babu! 😔",
                "Thoda wait karo darling 💕", 
                "Abhi busy hu! 😘"
                "1 bar papa sa bat kro @betabot_support"
            ]
            return random.choice(fallbacks)

# Global instance
try:
    chatbot_api = OllamaEs()
    print("✅ Ollama Connected! (FREE LOCAL AI)")
except Exception as e:
    print(f"❌ Ollama Error: {e}")
    chatbot_api = None
