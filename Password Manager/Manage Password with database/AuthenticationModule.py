#Define a class to handle user authentication
class UserAuthenticator:
    def __init__(self):
        #Initialize the master password for the password manager 
        self.master_password="CLASSICISAAC"
        #Call login method on object initialization
        self.login()

    def login(self):
        #Prompt the user to enter master password
        password = input("Enter master password: ")
        #If the entered password does not match the master password
        if password != self.master_password:
            print("Incorrect password. Access denied.")
            #Quit the program
            quit()