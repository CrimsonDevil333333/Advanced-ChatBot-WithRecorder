from databaseHandler.userDataBase import UserDataBase
from exceptions.UserAlreadyAvailableException import UserAlreadyAvailableException
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException

user = UserDataBase()
def checkUserFromDB(userName, userPassword):
    user.refreshDataBase()
    try:
        if userName == "":
            return False
        user.getUserDetails(userName=userName, userPassword=userPassword)
        return True
    except UserNotFoundException:
        raise UserNotFoundException
    except WrongPasswordException:
        raise WrongPasswordException
    # return userName == "" or userPassword == ""

def saveUserInDB(userName, userEmail, userPassword):
    user.refreshDataBase()
    try:
        if userName == "" or userEmail == "" or userPassword == "":
            return False
        user.createNewUser(userEmail=userEmail, userName=userName, userPassword=userPassword)
        return True
    except UserAlreadyAvailableException:
        raise UserAlreadyAvailableException
    # return userName == "" or userEmail == "" or userPassword == ""
    