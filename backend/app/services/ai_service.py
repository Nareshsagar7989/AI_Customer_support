import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(user_message: str) -> str:
    """
    Sends the user message to Groq (Llama 3) and returns the response.
    """
    if not os.getenv("GROQ_API_KEY"):
        return "System: GROQ_API_KEY is missing in .env file."

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful restaurant assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            # Using Qwen 3.8 27B model which is currently available on your Groq account
            model="qwen/qwen3.8-27b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"
