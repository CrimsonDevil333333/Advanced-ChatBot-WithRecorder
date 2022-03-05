import webbrowser

from logs.Logers import logs

from modules.AimlModule import Aiml
from modules.WikipediaModule import Wikipedia
from modules.WikiHowModule import WikiHow

from exceptions.NetworkException import NetworkException
from exceptions.WikiHowDataNotFoundException import WikiHowDataNotFoundException


class InputOutputConnector:
    def __init__(self) -> None:
        self.response = None

        self.aimlResponse = Aiml()
        self.wikipediaResponse = Wikipedia()
        self.wikiHowResponse = WikiHow()

    # Main input output function for application 
    def responseManager(self, responseInput): 
        print(responseInput)
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
                return self.aimlResponse.standAloneInput(response)
        
        except NetworkException:
            logs().error("Internet Connection Error in InputOutputConnector")

        except WikiHowDataNotFoundException:
            logs().error("WikiHowDataNotFound Error in InputOutputConnector")
            logs().debug("Sending Data to internet for google search ")
            self.responseFromInternet()

    # Last resort if application is incapable to answer any query it will redirect to internet 
    def responseFromInternet(self):
        webbrowser.open_new('www.google.com/search?q=' + self.response)
        return "Searching in Browser"