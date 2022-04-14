import webbrowser
from sqlalchemy import null

from logs.Logers import logs

from modules.AimlModule import Aiml
from modules.WikipediaModule import Wikipedia
from modules.WikiHowModule import WikiHow
from modules.NlpModule import NLP

from modules.recorder.InternalVoiceRecoder import InternalVoiceRecorder
from modules.converter.VoiceToTextConverter import VoiceToTextConverter

from exceptions.NetworkException import NetworkException
from exceptions.WikiHowDataNotFoundException import WikiHowDataNotFoundException
from exceptions.NlpQueryNotFoundException import NlpQueryNotFoundException


class InputOutputConnector:
    def __init__(self, nlpFilePath = None) -> None:
        self.response = None

        self.aimlResponse = Aiml()
        self.wikipediaResponse = Wikipedia()
        self.wikiHowResponse = WikiHow()
        if nlpFilePath != null:
            self.nlpResponse = NLP(nlpFilePath)
        else:
            self.nlpResponse = NLP()

    # Main input output function for application 
    def responseManager(self, responseInput): 
        return self.responseLogic(responseInput)

    # It takes question in form of response and gives out output according to the given query 
    def responseLogic(self, response):
        self.response = response
        try:
            if "tell me about" in response:
                return self.wikipediaResponse.standAloneInput(response.replace("tell me about ", ""))
            elif "how to" in response:
                return self.wikiHowResponse.standAloneInput(response.replace("how to ",""))
            else:
                return self.nlpResponse.standAloneInput(response)
                
        
        except NetworkException:
            logs().error("Internet Connection Error in InputOutputConnector")

        except WikiHowDataNotFoundException:
            logs().error("WikiHowDataNotFound Error in InputOutputConnector")
            logs().debug("Sending Data to internet for google search ")
            return webbrowser.open_new('www.google.com/search?q=' + response)

        except NlpQueryNotFoundException:
            logs().error("NlpQueryNotFoundException Error in InputOutputConnector")
            logs().debug("Sending query to AIML response section")
            return self.aimlResponse.standAloneInput(response)
        
        except IndexError:
            return webbrowser.open_new('www.google.com/search?q=' + response)

    # NLP with multiple files inclusions
    def nlpWithCustomFilePaths(self, nlpFilePath):
        self.nlpResponse = NLP(nlpFilePath)

    # record meeting and save audio in proper wav format and convert at sametime 
    def recorderAndConverter(self, outputFileName = None, outputFilePath = None, txtFileOutputPath = None):
        if outputFileName == None:
            outputFileName = "test"
        if outputFilePath == None:
            outputFilePath = rf"database\audiofiles\{outputFileName}"  
        if txtFileOutputPath == None:
            txtFileOutputPath = rf"database\{outputFileName}.txt"

        voiceToTextConverter = VoiceToTextConverter()

        InternalVoiceRecorder().recorder(outputFilePath + ".mp3")
        voiceToTextConverter.audioFormatConverter(inputPath= outputFilePath+".mp3", outputPath= outputFilePath+".wav")
        voiceToTextConverter.voiceToTextConverter(inputPath= outputFilePath+".wav", outputPath= txtFileOutputPath)


