
# from modules.NlpModule import NLP
# from modules.converter.VoiceToTextConverter import VoiceToTextConverter
# from exceptions.NlpQueryNotFoundException import NlpQueryNotFoundException
from connection.InputOutputConnector import InputOutputConnector

if __name__ == "__main__":
    # try:
    #     nlpResponse = NLP()
    #     print(nlpResponse.standAloneInput("What happen 17 years latter"))
    # except NlpQueryNotFoundException:
    #     print("Exsasasa")

    # VoiceToTextConverter().converter()

    # hello = "sasa"
    # print("hello"+rf"\{hello}"+" yo")

    InputOutputConnector().recorderAndConverter(outputFileName='test')
    