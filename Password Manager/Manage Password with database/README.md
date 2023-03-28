This project is a simple password manager that allows users to store passwords for different applications. It includes a database integration for secure storage of user data. The project is written in Python and includes two files: AuthenticationModule.py and Manage-Password-With-database.py.

### Features
Secure storage of passwords in a PostgreSQL database
User authentication for added security
Ability to add, retrieve, and delete passwords
Simple command-line interface


###  Getting Started
Clone the repository to your local machine
Install the required libraries by running pip install ...
Open AuthenticationModule.py and set the master_password variable to your desired master password.
Run Manage-Password-With-database.py to start the password manager.
### Usage
Upon running the Manage-Password-With-database.py file, you will be prompted to enter your master password. If the password is correct, you will be logged into the password manager and presented with a menu of options:

Add password
Retrieve password
Delete password
Quit
To add a new password, select option 1 and follow the prompts to enter the username, application, and password. The password will be encrypted and stored in the database.

To retrieve a password, select option 2 and enter the username and application for the password you want to retrieve. The password will be decrypted and displayed on the screen.

To delete a password, select option 3 and enter the username and application for the password you want to delete.

### Security
The password manager includes several security features to protect user data. Passwords are encrypted using the Fernet encryption algorithm from the cryptography library. User authentication is implemented using the UserAuthenticator class in AuthenticationModule.py. The user's master password is never stored in plain text and is used to decrypt the user's password data from the database.

#### License
This project is licensed under the MIT License. See LICENSE for more information 