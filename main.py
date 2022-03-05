from connection.InputOutputConnector import InputOutputConnector
from controller.MainController import MainController

if __name__ == "__main__":
    outputFilePath = "output/test.txt"
    MainController = MainController()
    ioc = InputOutputConnector()

    MainController.bothWayOutput(ioc.responseManager(MainController.convertVoiceToText()))
