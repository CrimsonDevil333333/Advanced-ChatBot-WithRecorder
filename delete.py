from databaseHandler.userDataBase import UserDataBase
from exceptions.UserAlreadyAvailableException import UserAlreadyAvailableException
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException
if __name__ == "__main__":
    user = UserDataBase()
    user.refreshDataBase()
    
    # Signup
    # try:
    #     user.createNewUser(userEmail="admin@admin.admin", userName="admin", userPassword="admin")
    # except UserAlreadyAvailableException:
    #     print("User allready available")
   
    # Login
    # try:
    #     user.getUserDetails(userName="admin", userPassword="admin")
    # except UserNotFoundException:
    #     print("User Not found")
    # except WrongPasswordException:
    #     print("Password is not correct")