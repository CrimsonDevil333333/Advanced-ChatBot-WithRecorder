from connection.InputOutputConnector import InputOutputConnector
from controller.MainController import MainController

from modules.recorder.InternalVoiceRecoder import InternalVoiceRecorder
from modules.converter.VoiceToTextConverter import VoiceToTextConverter

from exceptions.NetworkException import NetworkException
from logs.Logers import logs

class BackendMain:
    def __init__(self, Input = True, Output = True) -> None:
        self.voice_input = Input
        self.voice_output = Output
        self.ioc = InputOutputConnector()
        self.maincontrol = MainController()
        self.vttc = VoiceToTextConverter()

    def takeSingleInput(self):
        
        # saveMp3Output replace by voiceOutput to get audio in a file.
        try:
            if self.voice_input and self.voice_output:
                self.maincontrol.voiceOutput(output= self.ioc.responseManager(responseInput= self.maincontrol.convertVoiceToText()) )
            elif self.voice_input:
                self.maincontrol.textOutput(output= self.ioc.responseManager(responseInput= self.maincontrol.convertVoiceToText()))
            elif self.voice_output:
                n = input("Enter your Query : ")
                self.maincontrol.voiceOutput(output= self.ioc.responseManager(responseInput= n))
            else:
                n = input("Enter your query : ")
                self.maincontrol.textOutput(output= self.ioc.responseManager(responseInput= n))

        except NetworkException:
            # logs.error(msg="NetworkException error in main.py")
            print("network Exception")

    def getBotResponse(self, userInput):
        return self.maincontrol.textOutput(output= self.ioc.responseManager(responseInput= userInput))

    def recordMeetingFromApp(self, time = 10):
        # Audio is being saved as mp3 format if want to use it first convert it into wav format
        self.ivr = InternalVoiceRecorder(seconds= time)
        self.ivr.recorder(filePath=None)

    def convertRecordingsIntoData(self):
        #Converting mp3 as wav
        self.vttc.audioFormatConverter(inputPath=None, outputPath=None)
        self.vttc.voiceToTextConverter(inputPath=None, outputPath=None)

    def getVoiceInput(self):
        return  self.maincontrol.convertVoiceToText()

if __name__ == "__main__":
    mainClass = BackendMain(Input=True, Output=False)
    mainClass.takeSingleInput()
    print(mainClass.getVoiceInput())
    # mainClass.recordMeetingFromApp(time= 10)
    # mainClass.convertRecordingsIntoData()