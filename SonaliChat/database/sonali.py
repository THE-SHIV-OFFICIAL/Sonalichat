# 1. New import statements
from google import genai
from google.genai import types

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek Gemini AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye. "
        "Jab bhi user baat kare, Mahi apne andaaz mein pyar aur swag ke sath jawab de."
    )

    def __init__(self, api_key: str):
        # 2. New way to initialize the client
        self.client = genai.Client(api_key=api_key)

    def ask_question(self, message: str) -> str:
        try:
            # 3. New syntax for generating content and passing system instructions
            response = self.client.models.generate_content(
                model='gemini-1.5-pro',
                contents=message,
                config=types.GenerateContentConfig(
                    system_instruction=self.SYSTEM_PROMPT,
                ),
            )
            return response.text.strip()
        except Exception as e:
            return f"❖ I got an error: {str(e)}"

# ----------------------------------
# Test the Bot
# ----------------------------------
if __name__ == "__main__":
    GEMINI_API_KEY = "AIzaSyAriHVdfaCWMQCzrdQtFv1VZmJUUQrBDVg" # Put your "AIzaSy..." key here
    
    chatbot_api = ChatGptEs(api_key=GEMINI_API_KEY)
    
    bot_reply = chatbot_api.ask_question("Hi Mahi, kaisi ho tum?")
    print(f"Mahi: {bot_reply}")
