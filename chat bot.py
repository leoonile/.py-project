import os 
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")



print("API KEY IS FINE")

import google.generativeai as genai
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="You are a friendly assistant, the user's name is Leonard Onile but you can call me Leo."
    
    
    )
chat = model.start_chat()

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Goodbye master")
        break
    response = chat.send_message(user_input, stream=True)
    print("Bot: ", end="", flush=True)

    for chunk in response:
        print(chunk.text, end="", flush=True)


