from datetime import date
import pickle
import os

#journal class
class Journal():
    def __init__(self,title = "",entry = ""):
        #initialize the object, date is auotomatically whatever todays date is
        today = date.today()
        self.__title = title
        self.__entry = entry
        self.__date = today.strftime("%d/%m/%Y")

    #geter methods for date, title, and entry
    def get_date(self):
        return self.__date
    def get_title(self):
        return self.__title
    def get_entry(self):
        return self.__entry
    

#start of journal functions

#gets a list of every user entry, if its empty it retuns the list data type, takes a string as it's arg  
def load_entries(user_name):

    #only open if the file is greater than 0 bits
    if os.path.getsize(user_name + ".pickle") > 0:
        with open(user_name + ".pickle", "rb") as infile:
            entry_list = pickle.load(infile)
            infile.close()
        return list(entry_list)
    else:
        return list()
        



    
#takes a string representing name and an entry object as args, saves entry to user's file
def save_entry(user_name,entry):

    #load all entries    
    previous_entries = load_entries(user_name)

    #add this entry to old entries
    previous_entries.append(entry)
    
    #open the user's file and save the list of entries back into the file
    with open(user_name + ".pickle", "wb") as outfile:
        pickle.dump(previous_entries,outfile)
    outfile.close()
    print("\nYour Entry has been saved!\n")

#prints contents of single entry
def print_entry(entry):
    print(f'\n{entry.get_date()}\n-------------\n{entry.get_title()}:\n{entry.get_entry()}\n\n')
        
#takes the user name as an argument, prints the user's entries
def print_all(user_name):
    #load all entries
    entries = load_entries(user_name)

    #there were no entries to show
    if len(entries) == 0:
        print("\nNo Entries To Display\n")
        return
        

    #call print entry for all entries
    for x in entries:
        print_entry(x)
    return
    
def create_entry():
    # create new instance of journal object
    new_entry = Journal()
    #ask user for title, this is what we will use to search for the entries
    while True:
        #title cant be more than 30 characters
        title = str(input("Title your journal entry: "))
        if len(title) > 30:
            print("Please make sure title is less than 30 characters")
            continue
        else:
            break
    #get journal entry, any string is a valid journal entry, but the program will only save the first 2000 characters for storage purposes
    entry = str(input("\nNOTE: Only the first 2000 characters of your entry will be saved\n---------------------------------\nJournal Here:\n"))

    if len(entry) > 2000:
        entry = entry[0:2001]

    #initialize the entry object
    new_entry.__init__(title,entry)

    #return the intanceso it can be saved
    return new_entry

def search_entries(user_name):
    print("Search for Journal entries by title\n------------------------\n")
    #get search criteria
    while True:
        search_title = str(input("What would you like to search for?: "))
        #search cant be longer than any title                         
        if len(search_title) > 30:
            print("Titles Are all 30 or fewer characters, this will return nothing\n")
            continue
        else:
            break
    #get every entry written by the user
    entry_list = load_entries(user_name)
    valid_entries = list()

    #store matching entries into a list of valid entries
    for entry in entry_list:
        if search_title in entry.get_title():
            valid_entries.append(entry)

    #if the length of that list is 0, nothing was found
    if len(valid_entries) == 0:
        print("\nEntry Not Found\n")
        return
    #otherwise, print all the entries out
    else:
        for x in valid_entries:
            print_entry(x)
                             
                        
#takes username as an argument       
def journal_menu(user_name):
    #run until user wants to return to the main menu
        while True:
            print("\nJournal Menu\n---------")
            choice = str(input("1.Create New Entry\n2.Search Entries\n3.View All\n4.Back\n"))
            if choice == '1':
                #get an entry from the user
                new_entry = create_entry()
                #save the entry
                save_entry(user_name,new_entry)
                #run the search entries function
            elif choice == '2':
                search_entries(user_name)
                #print every entry owned by the user
            elif choice == '3':
                print_all(user_name)
                #return to the main menu
            elif choice == '4':
                print("Retunring to main menu\n")
                return         
            else:
                print("Please pick 1, 2, 3, or 4")
                continue
