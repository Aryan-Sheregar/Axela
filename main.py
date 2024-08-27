from speech_to_text import record_and_transcribe
from bot import generate_response, add_context, clear_context
from text_to_speech import text_to_speech

if __name__ == "__main__":
    while True:
        # Call the function to record and transcribe audio

        transcript = record_and_transcribe()
        print("Transcription:\n", transcript)

        add_context(" ")

        # Example usage
        prompt = f"{transcript}"
        response = generate_response(prompt)
        response = response.replace("*", "")

        print(response)
        text_to_speech(response)

        # Add more context and generate a new response
        add_context(f"{prompt}")
        add_context(f"{response}")

        if "Bye." in prompt:
            text_to_speech("Goodbye")
            clear_context()
            break