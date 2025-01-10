import speech_recognition as s

sr= s.Recognizer()

print("i am you'r script and listning you ........")

with s.Microphone() as m:
    audio = sr.listen(m)
    query = sr.recognize_whisper(audio, language='eng-in')
    print(query)
    