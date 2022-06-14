from logs.Logers import logs
from webScraping.wikiHow import *

from exceptions.WikiHowDataNotFoundException import WikiHowDataNotFoundException

# Wiki How module
class WikiHow:
    def __init__(self) -> None:
        self.maxResults = 1

    def standAloneInput(self, question, maxResults = None):
        try:
            if maxResults != None:
                self.maxResults = maxResults
            
            howTos = search_wikihow(question, self.maxResults)
            assert len(howTos) == 1
            d = howTos[0].print()
            return d

        except:
            logs().error("WikiHowDataNotFound Error in WikiHowModule")
            raise WikiHowDataNotFoundException