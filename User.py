# User.py
import sqlite3
from db import create_connection, initialize_db
import hashlib
import os

#user class
class User:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

def hash_password(password):
    #16 byte salt
    salt = os.urandom(16)
    
    # hash and salt the user's password
    hashed_password = hashlib.pbkdf2_hmac('sha256',password.encode(),salt,100000)
    
    #return salt and password
    return salt + hashed_password

#verify that the passed password is correct
def verify_password(stored_password, provided_password):
    
    # get the first 16 bytes (salt)
    salt = stored_password[:16]
    
    #get the hashed password
    stored_hash = stored_password[16:]
    
    #hash the password they providede to make sure it matches what we have stored
    provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    
    # check to make sure the values are equal
    return stored_hash == provided_hash

#saves new user in db, checks to make sure the new user is unique
def save_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (username, password) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different one.")
    finally:
        conn.close()
#take the username and password, return None if the user cant be found in the db, otherwise retruns user 
def get_user(username, provided_password):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id, stored_password = result
        if verify_password(stored_password, provided_password):

            return user_id
        else:
            print("Invalid password.")
    else:
        print("User not found.")
    return None



#create and store a new user
def new_user():
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    save_user(username, password)

#login option for user
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    user = get_user(username, password)
    #verify the entered user data
    if user:
        print("Login successful!")
        return user 
    else:
        print("Try again.")
        return None