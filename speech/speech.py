import speech_recognition as sr
import  webbrowser, time, playsound, os, random
from gtts import gTTS
from time import ctime

r = sr.Recognizer()

def record_audio(ask = False):
    #setting microphone as source
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice_data = ''         #voice store
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            screxii_speak('Sorry didn\'t get that')
        except sr.RequestError:
            screxii_speak('Speech service down')
        return voice_data

def respond(voice_data):
    if 'what is your name' in voice_data:
        return screxii_speak('My name is Screxy')
    if 'what time is it' in voice_data:
        screxii_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        return screxii_speak('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('What location?')
        if location != '':
            url = 'https://google.com/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            return screxii_speak('Opening up the map for ' + location)
        else :
            return screxii_speak('I don\'t know where that is')
    if 'leave' in voice_data:
        exit()
    else :
        return screxii_speak('Ask me something')

def screxii_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file) 

#time.sleep(1)
print('How can I help you?')
while 1:
    voice_data = record_audio()
    #print("Given input: ", voice_data)
    respond(voice_data)