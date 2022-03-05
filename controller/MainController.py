import speech_recognition as sr
import win32com.client as wincl

from gtts import gTTS
from logs.Logers import logs

from exceptions.NetworkException import NetworkException

class MainController:
    def __init__(self, outputFileName= None) -> None:
        self.outputFileName = outputFileName
        self.speak = wincl.Dispatch("SAPI.SpVoice")
        self.recorder = sr.Recognizer()
        self.language = 'en'

# If there is any file which user want to add to bot 
    def loadVoice(self, voiceLocation):
        pass

# If user wants to take input using voice 
    def convertVoiceToText(self):
        print("Start Talking")
        with sr.Microphone() as source:
            audio = self.recorder.listen(source)
            try:
                input = self.recorder.recognize_google(audio)
                return input
            except:
                logs().error("Internet Connection Error in MainController while using convertVoiceToText")
                raise NetworkException

# If we want to give output in form of voice instead of Text
    def voiceOutput(self, output):
        self.speak.Speak(output)

# If we want to give output in form of text 
    def textOutput(self, output):
        print(output)

# If we want to give output in both ways 
    def bothWayOutput(self, output):
        print(output)
        self.speak.Speak(output)

# If want to save output of voice as mp3 format
    def saveMp3Output(self, output):
        myobj = gTTS(text=output, lang=self.language, slow=False)
        myobj.save("output/response.mp3")