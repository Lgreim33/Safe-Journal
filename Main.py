import User
import Journal

def main():
    print("Welcome to Secure Journaler!")

    #simple menu for the journal
    while True:
        choice = input("1. Create New User\n2. Login\n3. Quit\n")
        if choice == '1':
            User.new_user()
        elif choice == '2':
            user_id = User.login()
            if user_id:
                Journal.journal_menu(user_id)
        elif choice == '3':
            print("Thank you for using Secure Journaler!")
            break
        else:
            print("Invalid choice. Try again.")

main()
