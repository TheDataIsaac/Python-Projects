#Import necesary libraries
import pickle
from cryptography.fernet import Fernet, InvalidToken
import psycopg2


class DatabaseConnection:
    def __init__(self):
        pass

    def connect_database(self):
        #Connect to PostgreSQL database
        conn=psycopg2.connect(
            dbname="test",
            user="classicisaac",
            password="thimmy",
            host="localhost",
            port="5432"
            )
        try:
            #Open a cursor to perform dtabase operations
            return conn.cursor(),conn
        except(Exception) as error:
            raise Exception("Error while connecting to PostgreSQL") from error





class Database:
    def __init__(self):
        self.databaseconnection=DatabaseConnection()
        self.cur,self.conn=self.databaseconnection.connect_database()
        self.create_table()


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

        #Method to check if table exists
    def check_for_table(self):
        #Define the name of the table you want to check
        table_name="password_table"
        #Execute the query to check if the table exists
        self.cur.execute("SELECT EXISTS(SELECT * FROM pg_catalog.pg_tables WHERE tablename=%s)",(table_name,))
        #Fetch the name of the query
        result=self.cur.fetchone()
        return result[0]

    def retrieve_data(self,username,app):
        try:
            retrieve_query="SELECT password FROM password_manager.password_table WHERE (username,app)=(%s,%s);"
            self.cur.execute(retrieve_query,(username,app))
            #Check if the row exists
            #return (str(self.cur.fetchone()[0]))
        except(Exception) as error:
            raise Exception("Error while fetching data from PostgreSQL") from error
        else:
            result=self.cur.fetchone()
            #print(result)
            if result is not None:
                return result[0]
            else:
                print(f"{app} password does not exist")
                quit()

    def add_to_database(self,username,app,encrypted_data):
        insert_query="INSERT INTO password_manager.password_table(username,app,password) VALUES (%s,%s,%s) ON CONFLICT (username,app) DO UPDATE SET password=EXCLUDED.password;"
        self.cur.execute(insert_query,(username,app,encrypted_data)) 
        self.conn.commit()

    def delete_from_database(self,username,app):
        delete_query="DELETE FROM password_manager.password_table WHERE username=(%s) AND app=(%s)"
        self.cur.execute(delete_query,(username,app)) 
        self.conn.commit()

class UserAuthenticator:
    def __init__(self):
        #Initialize the master password for the password manager 
        self.master_password="CLASSICISAAC"
        self.login()

    def login(self):
        #Prompt the user to enter master password
        password = input("Enter master password: ")
        #If the entered password does not match the master password
        if password != self.master_password:
            print("Incorrect password. Access denied.")
            quit()

#Define PasswordManager class
class PasswordManager:
    def __init__(self, username):
        self.username=username
        self.login=UserAuthenticator()
        #Call login method
        self.login
        #Generate the fernet encryption key to encrypt/decrypt the passwords
        self.fernet = self.generate_fernet_key()
        self.database=Database()
    
    #Generate a fernet key
    def generate_fernet_key(self):
        #Hardcided Fernet encryption key
        my_key = b'l3QlnmJRYceg84ze42mgZVewqfeBk_tkbZpXKSyUY1w='
        #Return the Fernet object initialized with the given key
        return Fernet(my_key)
   
    #Authenticate user

    
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
        app_name = input("Enter App name or Web URL: ").strip().capitalize()
        #Get the password for the app
        password = input("Password: ").strip()
        #Serioalize the data to be stored as a password object
        pickled_data = pickle.dumps(password)
        #Encrypt the pasword using the Fernet encryption key
        encrypted_data = self.fernet.encrypt(pickled_data)
        self.database.add_to_database(self.username,app_name,encrypted_data)
        #Print a message confirming that the password was added successfully
        print(f"Added password for {app_name}")

    def get_password(self,app_name):
        encrypted_data=self.database.retrieve_data(self.username,app_name)
        try:
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
        password=self.get_password(app_name)
        print(f"{app_name} Password: {password}")


    
    #Method to change password for a given app name
    def change_password(self):
        #Ask user for which app password to change
        app_name = input("Which password do you want to change? ").strip().capitalize()
        self.database.retrieve_data(self.username,app_name)
        new_password = input("Enter new password: ").strip()
        #Seriaize the data
        pickled_data = pickle.dumps(new_password)
        #Encrypt the serialized data
        encrypted_data = self.fernet.encrypt(pickled_data)
        self.database.add_to_database(self.username,app_name,encrypted_data)
        print(f"{app_name} password changed successfully")



    #Method to delete password for a given app name
    def delete_password(self):
        #Ask user for which app password to delete
        app_name = input("Which password do you want to delete? ").strip().capitalize()
        self.database.retrieve_data(self.username,app_name)
        self.database.delete_from_database(self.username,app_name)
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
        print("Your information is secure. Have a great day")



passwordmanager=PasswordManager("Classic Isaac")
passwordmanager.managepassword()