from gtts import gTTS
import os


def text_to_speech(text, lang='en'):

    tts = gTTS(text=text, lang=lang)
    tts.save("output.wav")
    os.system("afplay output.wav")
