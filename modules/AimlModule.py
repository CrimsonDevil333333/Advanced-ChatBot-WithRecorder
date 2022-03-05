from tkinter.messagebox import QUESTION
import aiml
import os

class Aiml:
    def __init__(self) -> None:
        self.k = aiml.Kernel()
        BRAIN_FILE="dump/brain.dump"
        if os.path.exists(BRAIN_FILE):
            print("Loading from brain file: " + BRAIN_FILE)
            self.k.loadBrain(BRAIN_FILE)
        else:
            print("Parsing aiml files")
            self.k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
            print("Saving brain file: " + BRAIN_FILE)
            self.k.saveBrain(BRAIN_FILE)

    def standAloneInput(self, question):
        if question == None:
            return "Queries cannot be Left blank"
        return self.k.respond(question)