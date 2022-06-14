import speech_recognition as sr
import subprocess

class VoiceToTextConverter:
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def voiceToTextConverter(self, inputPath = None, outputPath = None):
        if inputPath == None:
            inputPath = r'database\audiofiles\output.wav'
        if outputPath == None:
            outputPath = r"database\output1.txt"

        with sr.AudioFile(inputPath) as source:
            audio = self.r.listen(source)
            
            text = self.r.recognize_google(audio)

            file=open(outputPath,"w")
            file.write(text)
            print(text)
            
    def audioFormatConverter(self, inputPath= None, outputPath= None):
        if inputPath == None:
            inputPath = r'database\audiofiles\output.mp3'
        if outputPath == None:
            outputPath = r'database\audiofiles\output.wav'
            
        subprocess.call(['ffmpeg', '-i',inputPath,
                   outputPath])
        
if __name__ == "__main__":
    # VoiceToTextConverter().audioFormatConverter()
    VoiceToTextConverter().voiceToTextConverter()