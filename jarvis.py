import os 
from dotenv import load_dotenv
from RealtimeSTT import AudioToTextRecorder
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient
import io
from pydub import AudioSegment
from pydub.playback import play as play_audio


MAX_OUTPUT_TOKENS=200

def main():
    load_dotenv()

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    



    print("API KEY IS FINE")

    import google.generativeai as genai
    genai.configure(api_key=gemini_api_key)
    elevenlabs = ElevenLabs(api_key="sk_173f42dea5e0c7544a14cbdc435d94dbb8e31416b835292f")    

    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="You are a friendly assistant, the user's name is Leonard Onile but you can call me Leo."
      
    )
     
        
        
    

    chat = model.start_chat()
    recorder = AudioToTextRecorder(model='tiny.en', language="en", spinner=False)

    while True:
        print("You: ", end="", flush=True)
        user_input = recorder.text()
        print(user_input)
        if not user_input:
            print("I didn't catch that, can you repeat?")
            continue

        if user_input.lower() == "end.":
            print("Goodbye Leo")
            break
        response = chat.send_message(
            user_input, 
            stream=True,
            generation_config={"max_output_tokens": MAX_OUTPUT_TOKENS}
        )
        full_response = []
        print("Bot: ", end="", flush=True)

        for chunk in response:
            print(chunk.text, end="", flush=True)
            full_response.append(chunk)
        print()
        if full_response:
            full_text = "".join([chunk.text for chunk in full_response])
            audio = elevenlabs.text_to_speech.convert(
                 text=full_text,
                 voice_id='EXAVITQu4vr4xnSDxMaL',
                 model_id='eleven_flash_v2_5',
                 
            )
            audio_bytes = b''.join(audio)
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
            play_audio(audio_segment)


    recorder.shutdown()

        

if __name__ == "__main__":
    main()


