#Import necesary libraries
import pickle
from cryptography.fernet import Fernet, InvalidToken
import psycopg2
from AuthenticationModule import UserAuthenticator

#Define a class to handle database connections
class DatabaseConnection:
    def connect_database(self):
        #Connect to PostgreSQL database
        conn=psycopg2.connect(
            dbname="test",
            user=#Put your database username here,
            password=#Put your database password here,
            host="localhost",
            port="5432"
            )
        try:
            #Open a cursor to perform dtabase operations
            return conn.cursor(),conn
        except(Exception) as error:
            raise Exception("Error while connecting to PostgreSQL") from error




#Define a class to handle database operations
class Database:
    #Define an init method that creates a connection to the database, and creates a table in the database
    def __init__(self):
        #Instantiate a new instance of the DatabaseConnection class
        self.databaseconnection=DatabaseConnection()
        #Store the cursor and the connection object as instance variables
        self.cur,self.conn=self.databaseconnection.connect_database()
        #Create the password_table if it does not already exist
        self.create_table()

    #Define a method to create a new table in the database
    def create_table(self):
        #Define the SQL query for creating a new table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS password_manager.password_table(
            username VARCHAR(30) NOT NULL,
            app VARCHAR(30) NOT NULL,
            password VARCHAR(1000) NOT NULL,
            PRIMARY KEY(username,app)
        );"""
        #Execute the SQL query
        self.cur.execute(create_table_query)    
        #Commit the changes to the database and close the cursor and connection
        self.conn.commit()


    #Define a method to retrieve a password for a given username and app
    def retrieve_data(self,username,app):
        try:
            #SQL query for retrieving the password for  given username and app
            retrieve_query="SELECT password FROM password_manager.password_table WHERE (username,app)=(%s,%s);"
            #Execute the SQL query with given parameters
            self.cur.execute(retrieve_query,(username,app))
        except(Exception) as error:
            #Raise an exception idf there was an erroe while fetching data
            raise Exception("Error while fetching data from PostgreSQL") from error
        else:
            #Fetch the first result of the query
            result=self.cur.fetchone()
            #Check if there was a result
            if result is not None:
                #Return the password
                return result[0]
            else:
                #Print a message indicating that there was no result for the given username and app
                print(f"{app} password does not exist")
                quit()


    #Method to check if a password exists for a given username and app
    def check_for_password(self,username,app):
        try:
            #Define an SQL query for retrieving data
            retrieve_query="SELECT password FROM password_manager.password_table WHERE (username,app)=(%s,%s);"
            #Execute the SQL with the given parameters
            self.cur.execute(retrieve_query,(username,app))
        except(Exception) as error:
            #Raise an error if there was an error while fectching data
            raise Exception("Error while fetching data from PostgreSQL") from error
        else:
            #Fetch the first result of the query
            result=self.cur.fetchone()
            #Return a bookean indicating whether there was a result or not
            return (result is not None)

    #Method to add a new password to the database for a given username and app 
    def add_to_database(self,username,app,encrypted_data):
        #Define thee SQ for inserting data into the database
        insert_query="INSERT INTO password_manager.password_table(username,app,password) VALUES (%s,%s,%s) ON CONFLICT (username,app) DO UPDATE SET password=EXCLUDED.password;"
        #Execute the SQL query with given parameters
        self.cur.execute(insert_query,(username,app,encrypted_data)) 
        #Commit the changes to the database
        self.conn.commit()

    #Method to delete a password from the database for a given username and app
    def delete_from_database(self,username,app):
        #Definre the SQL query for deleting data from the database
        delete_query="DELETE FROM password_manager.password_table WHERE username=(%s) AND app=(%s)"
        #Execute the SQL with the given parameters
        self.cur.execute(delete_query,(username,app)) 
        #Commit the changes to the database
        self.conn.commit()



#Define PasswordManager class
class PasswordManager:
    def __init__(self, username):
        #Store the username passed to the object
        self.username=username
        #Instantiate UserAuthenticaotr object object to authenticate user
        self.login=UserAuthenticator()
        #Generate the fernet encryption key to encrypt/decrypt the passwords
        self.fernet = self.generate_fernet_key()
        #Create a database objecct to handle the database operations
        self.database=Database()
    
    #Generate a fernet key
    def generate_fernet_key(self):
        #Hardcided Fernet encryption key
        my_key = b'l3QlnmJRYceg84ze42mgZVewqfeBk_tkbZpXKSyUY1w='
        #Return the Fernet object initialized with the given key
        return Fernet(my_key)

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
   
    #Method to add password to database
    def add_password(self):
        #Get the name of the app for which the user wants to add a password
        app_name = input("Enter App name or Web URL: ").strip().capitalize()
        #Check if the password already exists
        if self.database.check_for_password(self.username,app_name):
            #If password exists, prompt the user if they want toc change the password
            change_prompt=input(f"NOTICE: {app_name} password exists. Do you want to change password?[yes/no]: ").strip().lower()
            #If the user enters an invalid input, quit the program
            if change_prompt not in ("yes","no"):
                print("Invalid input")
                quit()
            #If the user does not want to change the password, quit the program
            elif change_prompt=="no":
                print("\nYour information is secure. Have a great day")
                quit()
        #Get the password for the app
        password = input("Enter Password: ").strip()         
        #Serialize the data to be stored as a password object
        pickled_data = pickle.dumps(password)
        #Encrypt the pasword using the Fernet encryption key
        encrypted_data = self.fernet.encrypt(pickled_data)
        #Add the encrypted password to the database
        self.database.add_to_database(self.username,app_name,encrypted_data)
        #Print a message confirming that the password was added successfully
        print(f"Added password for {app_name}")

    #Method for decrypting encrypted password retrieved from database
    def get_password(self,app_name):
        #Retrieve the encrypted password from the database for the given app name
        encrypted_data=self.database.retrieve_data(self.username,app_name)
        try:
            #Convert the encrypted data to bytes
            encrypted_data=bytes.fromhex(encrypted_data[2:])
            #Decrypt the password using the Fernet encryption key
            pickled_data = self.fernet.decrypt(encrypted_data)
        #If the decryption fails, raise an InvalidToken exception     
        except InvalidToken:
            raise InvalidToken("InvalidToken: Could not decrypt data with given key")
        else:
            #Unpickle the decrypted data to get the password
            password=pickle.loads(pickled_data)
            return password


    #Method to view password for a given app name
    def view_password(self):
        #Get the app name and capitalize it
        app_name = input("Which password do you want to view? ").strip().capitalize()
        #Get the decrypted password for the app name using get_password method
        password=self.get_password(app_name)
        #Print the decrypted password
        print(f"{app_name} Password: {password}")


    
    #Method to change password for a given app name
    def change_password(self):
        #Ask user for which app password to change
        app_name = input("Which password do you want to change? ").strip().capitalize()
        #Check if the password exists before attempting to change it
        _=self.database.retrieve_data(self.username,app_name)
        #Get the new password from the user
        new_password = input("Enter new password: ").strip()
        #Seriaize the data
        pickled_data = pickle.dumps(new_password)
        #Encrypt the serialized data using the Ferne encryption key
        encrypted_data = self.fernet.encrypt(pickled_data)
        #Update the password in the database with the ew encrypted password
        self.database.add_to_database(self.username,app_name,encrypted_data)
        #Print a message confirming that the password was updated successfully
        print(f"{app_name} password changed successfully")



    #Method to delete password for a given app name
    def delete_password(self):
        #Ask user for which app password to delete
        app_name = input("Which password do you want to delete? ").strip().capitalize()
        #Check if the password exists before attempting to delete it
        _=self.database.retrieve_data(self.username,app_name)
        #Delete the passwrd from the database
        self.database.delete_from_database(self.username,app_name)
        #Print a amessage confirming that the password was deleted successfully
        print(f"{app_name} password deleted successfully")
        
    #Method to manage passwords - allows user to add, view, change, or delete passwords
    def managepassword(self):
        #Print menu of available operations
        print("'add' to add new password\n'view' to view existing passwords")
        print("'change' to change existing passwords\n'delete' to delete existing passwords")
        print("'quit' to cancel\n")
        #Prompt the user for desired operation chosen by user
        ask_operation = input("Which operation would you like to carry out?: ").lower().strip()
        # Call backend function to perform operation chosen by user
        self.backend(ask_operation)
        print("\nYour information is secure. Have a great day")


#Create an instance of the PasswordManager class with username
passwordmanager=PasswordManager("Classic Isaac")
#Call the managepassword() to begin the password management program
passwordmanager.managepassword()