#Import necesary libraries
import pickle
from cryptography.fernet import Fernet, InvalidToken


#Define PasswordManager class
class PasswordManager:
    def __init__(self, master_password):
        #Initialize the master password for the password manager
        self.master_password = "CLASSICISAAC" 
        #Generate the fernet encryption key to encrypt/decrypt the passwords
        self.fernet = self.generate_fernet_key()
    
    #Generate a fernet key
    def generate_fernet_key(self):
        #Hardcided Fernet encryption key
        my_key = b'l3QlnmJRYceg84ze42mgZVewqfeBk_tkbZpXKSyUY1w='
        #Return the Fernet object initialized with the given key
        return Fernet(my_key)
   
    #Authenticate user
    def login(self):
        #Prompt the user to enter master password
        password = input("Enter master password: ")
        #If the entered password does not match the master password
        if password != self.master_password:
            print("Incorrect password. Access denied.")
            #Raise an exception to deny access to the password manager
            raise ValueError("Incorrect password. Access denied.")
    
    #Backend method to manage operations for add, view, change, delete and quit
    def backend(self, operation):
        #Map the user's input to a corresponding funtion
        if operation == "add":
            self.add_password()
        elif operation == "view":
            self.view_password()
        elif operation == "change":
            self.change_password()
        elif operation == "delete":
            self.delete_password()
        #If user's input is "quit", exit the password manager
        elif operation == "quit":
            print("Goodbye!")
        #If the user enters an invalid option, print a message saying so
        else:
            print("Invalid option.")
   
    #Method to add password to file
    def add_password(self):
        #Get the name of the app for which the user wants to add a password
        name = input("Enter App name or Web URL: ").strip().capitalize()
        #Get the password for the app
        password = input("Password: ").strip()
        #Serioalize the data to be stored as a password object
        pickled_data = pickle.dumps({"name": name, "password": password})
        #Encrypt the pasword using the Fernet encryption key
        encrypted_data = self.fernet.encrypt(pickled_data)
        with open("passwords.bin", "ab") as file:
            #Write the encrypted password to a binary file
            file.write(encrypted_data)
            file.write(b"\n")
        #Print a message confirming that the password was added successfully
        print(f"Added password for {name}")
    
    #
    def get_password(self, app_name):
        #Initialize an empty list to store password objects
        password_list = []
        #Initialize a flag to check if the app_name is found in the password list
        text_found = False
        #Open the binary file containing the passwords in read mode
        with open("passwords.bin", "rb") as file:
            #Read all the lines from the file
            lines = file.readlines()
            for line in lines:
                try:
                    #Strip the whitespace from the line and decrypt it using the Fernet key
                    encrypted_data = line.strip()
                    #Decrypt the password using the Fernet encryption key
                    pickled_data = self.fernet.decrypt(encrypted_data)
                    #Unpickle the decrypted data to get the app name and password
                    data = pickle.loads(pickled_data)
                #If the decryption fails, raise an InvalidToken exception     
                except InvalidToken:
                    raise InvalidToken("InvalidToken: Could not decrypt data with given key")
                #Append the app name and password to the password list    
                else:
                    password_list.append(data)
        #Iterate over each app in the password list
        for app in password_list:
            #If the app name matches the given app name, set the text found flag
            #and retrieve the app name and password
            if app_name == app["name"]:
                text_found = True
                name = app["name"]
                password = app["password"]
                break
        #If the password was not found, return the text_found flag,
        #None for the name and password, and the password list
        else:
            return text_found, None, None, password_list
        return text_found, name, password, password_list
   
    #Method to view password for a given app name
    def view_password(self):
        #Get the app name and capitalize it
        app_name = input("Which password do you want to view? ").strip().capitalize()
        #Call the get_password to retrieve the password data
        text_found, name, password, _ = self.get_password(app_name)
        #If the app name was found, print the app name and password
        if text_found:
            print(f"{app_name} Password: {password}")
        #If the app name was not found, print a message indicating that it does not exist
        if not text_found:
            print(f"{app_name} password does not exist")
    
    #Method to change password for a given app name
    def change_password(self):
        #Ask user for which app password to change
        app_name = input("Which password do you want to change? ").strip().capitalize()
        #Call get_password method to retrieve the list of passwords and the passwords of the specified app
        text_found, _, _, password_list = self.get_password(app_name)
        #If the specified app exists, ask user to input new password
        if text_found:
            new_password = input("Enter new password: ").strip()
            #Loop through the list of apps and passwords
            for app in password_list:
                #If the specified is found
                if app_name == app["name"]:
                    #Change the password
                    app["password"] = new_password
            #Write the updated list of passwords to the binary file
            with open("passwords.bin", "wb") as file:
                for i in password_list:
                    #Seriaize the data
                    pickled_data = pickle.dumps(i)
                    #Encrypt the serialized data
                    encrypted_data = self.fernet.encrypt(pickled_data)
                    #Write the encrypted data to the binary file
                    file.write(encrypted_data)
                    file.write(b"\n")
            print(f"{app_name} password changed successfully")
        #If the app password was not found, print a message indicating that it does not exist
        else:
            print(f"{app_name} password does not exist")


    #Method to delete password for a given app name
    def delete_password(self):
        #Ask user for which app password to delete
        app_name = input("Which password do you want to delete? ").strip().capitalize()
        #Call get_password meThod to retrieve the list of passwords and the passwords of the specified app
        text_found, _, _, password_list = get_password(app_name, key)
        #If the specified app exists, loop through the list of apps and passwords
        if text_found:
            for app in password_list:
                #If the specified app is found
                if app_name == app["name"]:
                    #Remove the app and its password
                    password_list.remove(app)
            #Write the updated list of passwords to the binary file
            with open("passwords.bin", "wb") as file:
                for i in passwrord_list:
                    #Seriaize the data
                    pickled_data = pickle.dumps(i)
                    #Encrypt the serialized data
                    encrypted_data = self.fernet.encrypt(pickled_data)
                    #Write the encrypted data to the binary file
                    file.write(encrypted_data)
                    file.write(b"\n")
            print(f"{app_name} password deleted successfully")
        #If the app password was not found, print a message indicating that it does not exist
        else:
            print(f"{app_name} password does not exist")

    #Method to manage passwords - allows user to add, view, change, or delete passwords
    def managepassword(self):
        #Call login method
        self.login()
        #Print menu of available operations
        print("'add' to add new password\n'view' to view existing passwords")
        print("'change' to change existing passwords\n'delete' to delete existing passwords")
        print("'quit' to cancel\n")
        #Prompt the user for desired operation chosen by user
        ask_operation = input("Which operation would you like to carry out?: ").lower().strip()
        # Call backend function to perform operation chosen by user
        self.backend(ask_operation)
        print("Your information is secure. Have a great day")



passwordmanager=PasswordManager("CLASSICISAAC")
passwordmanager.managepassword()