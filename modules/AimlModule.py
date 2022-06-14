import aiml
import os

from logs.Logers import logs

# AIML module
class Aiml:
    def __init__(self) -> None:
        logs().info("Aiml is called")

        self.k = aiml.Kernel()
        BRAIN_FILE="dump/brain.dump"
        if os.path.exists(BRAIN_FILE):
            logs().debug("Loading from brain file: " + BRAIN_FILE)
            self.k.loadBrain(BRAIN_FILE)
        else:
            logs().debug("Parsing aiml files")
            self.k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
            logs().debug("Saving brain file: " + BRAIN_FILE)
            self.k.saveBrain(BRAIN_FILE)

    def standAloneInput(self, question):
        if question == None:
            return "Queries cannot be Left blank"
        return self.k.respond(question)