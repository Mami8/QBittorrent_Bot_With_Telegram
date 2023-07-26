import speech_recognition as sr
import subprocess
import os

KEYWORDS = ["cicikuş", "cici kuş"]
script_folder = "scripts/"

r = sr.Recognizer()
mic = sr.Microphone()
while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("dinleniyor")
            audio = r.listen(source)
            speech = r.recognize_google(audio, language="tr")
            print(speech)
            if speech in KEYWORDS:
                print("Şimdi script adını söyleyin (ingilizce): ")
                audio = r.listen(source)
                script = r.recognize_google(source, language="en-US")
                script = os.path.join(script_folder, script)
                subprocess.run(script)
    except Exception as e:
        print(e)
