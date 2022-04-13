import json

from regex import E
from exceptions.AliasAllreadyAvailableException import AliasAllreadyAvailableException
from exceptions.UserAlreadyAvailableException import UserAlreadyAvailableException
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException


class UserDataBase:
    def __init__(self) -> None:
        self.jsonFilePath = r'database\userDetails.json'
        self.jsonFile = open(self.jsonFilePath)
        self.data = json.load(self.jsonFile)
        self.jsonFile.close()

        # Default values of fields it will remain this unless user changes 
        self.userEmail = ""
        self.userPassword = ""
        self.userName = ""
        self.allAllias = ""

    def refreshDataBase(self):
        self.jsonFilePath = r'database\userDetails.json'
        self.jsonFile = open(self.jsonFilePath)
        self.data = json.load(self.jsonFile)
        self.jsonFile.close()

    def updateDatabase(self):
        self.data[self.userName] = {
            "userEmail": self.userEmail,
            "userPassword": self.userPassword,
            "allAllias": self.allAllias
        }
        with open(self.jsonFilePath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        print("data is saved") 

    def createNewUser(self, userEmail, userPassword, userName):
        try:
            DummyData = self.data[userName]
            print(DummyData)
            raise UserAlreadyAvailableException
        except KeyError:
            self.userEmail = userEmail
            self.userPassword = userPassword
            self.userName = userName
            self.allAllias = "default,"
            self.updateDatabase()
            print("new user data Added")

    def getUserDetails(self, userName, userPassword):
        try:
            data = self.data[userName]
            if data["userPassword"] == userPassword:
                self.updateSelfFields(userName=userName, userAllias=data["allAllias"], userEmail=data["userEmail"], userPass=data["userPassword"])
                return data
            else:
                raise WrongPasswordException
        except KeyError:
            raise UserNotFoundException


    def saveAliasForUser(self, userName, userAlias):
        pass

    def getUserAlias(self, userName):
        try:
            data = self.data[userName]
            self.updateSelfFields(userName=userName, userAllias=data["allAllias"], userEmail=data["userEmail"], userPass=data["userPassword"])
            return data["allAllias"]
        except:
            raise UserNotFoundException

    def updateAliasField(self, alias):
        try:
            dummyalias = self.allAllias.split(",")
            for r in dummyalias:
                if r == alias:
                    raise AliasAllreadyAvailableException
            self.allAllias = self.allAllias[:-1]
            self.allAllias = f"{self.allAllias},{alias},"
            self.updateDatabase()
        except:
            raise AliasAllreadyAvailableException
        

    def resetUserPassword(self, userName, oldPassword, newPassword):
        pass

    def resetUserName(self, oldUserName, newUserName):
        pass

    def resetEmailId(self, oldEmail, newEmail):
        pass
    
    def updateSelfFields(self, userName, userPass, userEmail, userAllias):
        self.userEmail = userEmail
        self.userPassword = userPass
        self.userName = userName
        self.allAllias = userAllias
