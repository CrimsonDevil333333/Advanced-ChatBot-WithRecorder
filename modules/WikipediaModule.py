from wikipedia import wikipedia
from logs.Logers import logs

# Wikipedia module
class Wikipedia:
    def __init__(self) -> None:
        logs().info("Wikipedia is called")

    def standAloneInput(self, question, sentencesNo = 4):
        return wikipedia.summary(question, sentences = sentencesNo)