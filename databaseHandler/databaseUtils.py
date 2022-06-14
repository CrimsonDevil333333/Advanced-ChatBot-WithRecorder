import json

from exceptions.AliasNotFoundException import AliasNotFoundException

class DatabaseUtils:
    def __init__(self) -> None:
        self.jsonFilePath = r'database\fileStructure.json'
        self.jsonFile = open(self.jsonFilePath)
        self.data = json.load(self.jsonFile)
        self.jsonFile.close()

        # Default values of fields it will remain this unless user changes 
        self.alias = "output"
        self.mp3FileName = r"database\audiofiles\output.mp3"
        self.wavFileName = r"database\audiofiles\output.wav"
        self.txtFileName = r"database\output.txt"

    def updateDatabase(self):
        self.data[self.alias] = {
            "mp3FileName": self.mp3FileName,
            "wavFileName": self.wavFileName,
            "txtFileName": self.txtFileName
        }
        with open(self.jsonFilePath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        print("data is saved") 

    def updateFileNamesAndPaths(self, alias = None, mp3FileName = None, wavFileName = None, txtFileName = None):
        if alias != None:
            self.alias = alias
        if mp3FileName != None:
            self.mp3FileName = mp3FileName
        if wavFileName != None:
            self.wavFileName = wavFileName
        if txtFileName != None:
            self.txtFileName = txtFileName

    def getFilesPathOnBaseOfAlias(self, alias):
        try:
            return self.data[alias]
        except KeyError:
            raise AliasNotFoundException


    
