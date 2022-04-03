
def checkUserFromDB(userName, userPassword):
    return userName == "" or userPassword == ""

def saveUserInDB(userName, userEmail, userPassword):
    return userName == "" or userEmail == "" or userPassword == ""
    