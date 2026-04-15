import google.generativeai as genai

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum Mahi ho – ek Gemini AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye. "
        "Jab bhi user baat kare, Mahi apne andaaz mein pyar aur swag ke sath jawab de."
    )

    def __init__(self, api_key: str):
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Use a valid model name (gemini-1.5-pro or gemini-1.5-flash)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.SYSTEM_PROMPT # New way to set system prompts in Gemini 1.5
        )

    def ask_question(self, message: str) -> str:
        try:
            # Generate response
            response = self.model.generate_content(message)
            return response.text.strip()
        except Exception as e:
            return f"❖ I got an error: {str(e)}"

# 1. API Key Setup
# USE ONLY ONE API KEY. The one starting with "AIzaSy..." is for Google Gemini.
# The one starting with "sk-proj..." is for OpenAI (ChatGPT) and will NOT work here.
GEMINI_API_KEY = "AIzaSyAriHVdfaCWMQCzrdQtFv1VZmJUUQrBDVg" 

# 2. Initialize the Chatbot
chatbot_api = ChatGptEs(api_key=GEMINI_API_KEY)

# 3. Test the Bot
if __name__ == "__main__":
    user_input = "Hi Mahi, kaisi ho tum?"
    print(f"User: {user_input}")
    
    bot_reply = chatbot_api.ask_question(user_input)
    print(f"Mahi: {bot_reply}")
