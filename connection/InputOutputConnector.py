from numpy import outer
from modules.AimlModule import Aiml

class InputOutputConnector:
    def __init__(self) -> None:
        self.aimlResponse = Aiml()
        
    def responseManager(self, responseInput):
        # We will call responce logic here to sync our program 
        
        print(responseInput)
        output = self.aimlResponse.standAloneInput(responseInput)
        return output

    def responseLogic():
        pass