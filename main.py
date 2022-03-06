from connection.InputOutputConnector import InputOutputConnector
from controller.MainController import MainController
from exceptions.NetworkException import NetworkException
from logs.Logers import logs

if __name__ == "__main__":
    outputFilePath = "output/test.txt"
    MainController = MainController()
    logs(1).debug("Application is used !!!")

    try:
        MainController.bothWayOutput(InputOutputConnector().responseManager(MainController.convertVoiceToText()))
        
    except NetworkException:
        logs().error("Internet Connection Error in Main")