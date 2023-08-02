import pickle
import os
import string
import random


#User Class
class User():
    #initialized the instance of the class
    def __init__(self,username = "",password = ""):
        self.__username = username
        self.__password = password
    # getter functions for password and username
    def get_pass(self):
        return self.__password
    
    def get_name(self):
        return self.__username



#User Library functions

    

#get string of printable ascii characters
list_of_encryption = string.printable

#contains the string:
'''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ 
'''




#validates the user's password, returns true if they get it right, otherwise it returns false
def password_validation(user_name,user_dict):

    #i will keep track of the attempts the user has taken
    i = 3
    local_user = user_dict[user_name]

    real_pass = de_cipher(local_user.get_pass())

    #user will be kicked back if they get the password wrong 3 times
    while i != 0:
        print(f'Tries Remaining: {i}')
        input_pass = str(input("Please Enter your password: "))

        if input_pass != real_pass:
              print("Incorrect, please try again\n")
              i -= 1
              continue
        else:
            return True
        
    return False



          
#function that will tell us if the user's password contains the required amount of numbers, returns true if it does, otherwise it retunrs false
def num_counter(password):
    #start off assuming there are no numbers
    num_counter = 0
    #for each integer in the password, increment the counter
    for x in password:
        if x.isnumeric() == True:
            num_counter +=1
        else:
            continue
    #if we incremented the counter at least twice, return true, if we didn't, return false
    if num_counter < 2:
        return False
    else:
        return True

#return an encrypted version of whatever is passed 
def cipher(password):
    #create an empty string
    encrypted = ""
    
    #seed will determine the pattern of encryption for the string, which will be stored in the string for later decryption, add one to the string value so its harder to decrypt
    string_seed = str(random.randint(1,8)+1) 
    int_seed = int(string_seed) - 1
  
    for x in password:
        if list_of_encryption.index(x)+ int_seed > 99:
            wrap_around = 100 - int_seed
            index = list_of_encryption.index(x) - wrap_around
            encrypted += list_of_encryption[index]
        else:
            index = list_of_encryption.index(x) + int_seed
            encrypted += list_of_encryption[index]
            
    #store the seef at the end of the encrypted string       
    encrypted += string_seed
    return encrypted


       
        
#return a decrypted version of whatever is passed            
def de_cipher(password):
    decrypted = ""

    
    #seed will determine the pattern of encryption for the string, which will be stored in the string for later decryption
    seed = int(password[len(password)-1]) -1
    password = password[:-1]
    
    #alter the value of the string to be a index of the ascii table, wrap around if it goes over the index
    for x in password:
        if list_of_encryption.index(x) - seed < 0:
            wrap_around = 100 + seed
            index = list_of_encryption.index(x) + wrap_around
            decrypted += list_of_encryption[index]
        else:
            index = list_of_encryption.index(x) - seed
            decrypted += list_of_encryption[index]
            
    #return the decrypted string     
    return decrypted



#returns a list of all users, or the dict type if the fule does not exist
def load_users():
    if os.path.exists("users.pickle"):
            
        with open("users.pickle", "rb+") as infile:
            password_list = pickle.load(infile)
            infile.close()
            return password_list
    else:
        return dict()


#save users in the user file
def save_users(user):
    with open("users.pickle", "wb") as outfile:
        pickle.dump(user,outfile)
        outfile.close()
    
#creates a new user and save the user, Also creates a file named after their encrypted username
def new_user():

    #list of characters required in the password
    required_chars = ['!','@','#','?','*','&','%']


    #load in the dictionary of users, create a list of the dict keys
    user_list = list()
    dict_users = load_users()
    key_list = dict_users.keys()

    #decipher the usernames
    for key in key_list:
        user_list.append(de_cipher(key))

    #request user to create a username
    while True:
        user_name = str(input("Please Enter Your Username: "))
        #username must be unique
        if len(dict_users)!= 0 and user_name in user_list:
            print("Username already exists, it must be unique to you!")
            continue
        #username must be 3-10 characters long
        elif len(user_name) not in range (3,11):
            print("Username must be 3 to 10 characters long\n")
            continue
        #username cant contain spaces
        elif " " in user_name:
            print("Username May Not Contain White Space\n")
            continue
        else:
            break

    #get the password from the user
    while True:
        password = input("Please choose a password: ")

        #password must be 8-16 characters long
        if len(password) not in range(8,17):
            print("Passwords must be between 8 and 16 characters long\n")
            continue
        #password must contain one of the characters from required_list
        elif any(x in password for x in required_chars) == False:
            print("For security reasons, your password must contian at least one of the following characters: '!,' '#,','?','*','&','%' or '@'\n")
            continue
        #password must contain two numbers
        elif num_counter(password) == False:
            print("Your Password Should Contain at least 2 numbers!\n")
            continue
        #password can not contain spaces
        elif " " in password:
            print("Password May Not Contain White Space\n")
            continue
        else:
            break


    #cipher the username and password, store them in a user object, store the username as the key in a dictionary, and the object as the value
    store_name = cipher(user_name)
    store_password = cipher(password)

    #store the name and password in an instance of a user object
    new_user = User()
    new_user.__init__(store_name,store_password)

    #update the user dict we got earlier
    dict_users.update({store_name:new_user})

    #save the updated dict
    save_users(dict_users)


    #CREATE A SEPERATE FILE FOR THE USER:
    user_file = open(store_name + ".pickle",'x')
    user_file.close()

    print("User Added! Returning to main menu!")

    

    return
    
        
    
#login prompts the user for their username and password, it returns their encrypted name if sucsessful
def login():

    #load dictionary of users
    key_list = list()
    user_dict = load_users()
    #get list of user keys
    user_list = list(user_dict.keys())

    #decipher the user names
    for key in user_list:
        key_list.append(de_cipher(key))

    #ask the user for their name
    while True:
        user_name = input("Please enter your Username: ")
        
        #if we cant find it ask the user what they want to do
        if user_name not in key_list:
            print("User name not found\n")
            while True:
                #the user may enter 1 or 2 depending on if they want to try again or not
                not_found = str(input("1.Try again\n2.Return to main menu\n"))
                if not_found == '1':
                    break
                elif not_found == '2':
                    return "NULL"
                else:
                    print("Please enter 1 or 2\n")
                    continue
            continue
        #the user was found
        else:
            #get the index of the non encrypted user
            index = key_list.index(user_name)
            #use that index to find the encrypted version
            encrypted_name = user_list[index]

            #run the password validation function, if sucsess, return the encrypted name
            if password_validation(encrypted_name,user_dict) == True:
                print("Welcome!")
                return encrypted_name
            #if failure, return the string: "NULL"
            else:
                print("Sorry, you've run out of attempts\n")
                return "NULL"
