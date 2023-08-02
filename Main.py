import Journal
import User




    
#main prgram
def main():
    print("Welcome to Secure Journaler! Your innermost thoughts have never been so safe!\n\n")

    #run the main menu until the user wants to quit
    while True:
        print("Menu\n---------")
        #prompt user with a choice
        choice = str(input("1.Create New User\n2.Login\n3.Quit\n"))
        #creates and stores a new user object as well as creating a new file for that user
        if choice == '1':
            User.new_user()
        #if the user already exists they can attempt to login
        elif choice == '2':
            print("Welcome Back!\n")
            #if the login function returns the username and to the NULL string, then they can access their journal
            user = User.login()
            if user != "NULL":
                Journal.journal_menu(user)
            else:
                continue
        #user quit, thank them and exit
        elif choice == '3':
            print("Thank you for trusting us with your thoughts!")
            break
        #invalid input
        else:
            print("Please pick 1, 2, or 3")
            continue

main()
