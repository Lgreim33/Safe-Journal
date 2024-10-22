from datetime import date
import sqlite3
from db import create_connection

#journal class, just holds title,entry, and date of writting
class JournalEntry:
    def __init__(self, title="", entry=""):
        self.title = title
        self.entry = entry
        self.date = date.today().strftime("%d/%m/%Y")

#store the entry into the database
def save_entry(user_id, journal_entry):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO JournalEntries (user_id, title, entry, date) VALUES (?, ?, ?, ?)",
        (user_id, journal_entry.title, journal_entry.entry, journal_entry.date),
    )
    conn.commit()
    conn.close()
    print("Journal entry saved successfully!")

#returns all entries of the passed user id
def load_entries(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, entry, date FROM JournalEntries WHERE user_id = ?",
        (user_id,)
    )
    entries = cursor.fetchall()
    conn.close()
    return entries


# returns list of journal entries of the passed user id with a similar title 
def search_entries(user_id, search_title):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT title, entry, date 
        FROM JournalEntries 
        WHERE user_id = ? AND title LIKE ?
        """,
        (user_id, f"%{search_title}%")
    )
    results = cursor.fetchall()
    conn.close()
    return results
#print out the user entry
def print_entry(entry):
    print(f"\n{entry[2]}\n-------------\n{entry[0]}:\n{entry[1]}\n")

#print all user entries for the passed user 
def print_all(user_id):
    entries = load_entries(user_id)
    if not entries:
        print("No journal entries found.")
    else:
        for entry in entries:
            print_entry(entry)

#create a new entry
def create_entry():
    #title prompt, only first 100 characters
    title = input("Title your journal entry: ")[:100]
    #entry prompt, only store the first 2000 characters
    entry = input("Write your journal entry (max 2000 chars): ")[:2000]
    return JournalEntry(title, entry)

#journal menu for searching entries
def search_menu(user_id):
    search_title = input("Enter the title or part of the title to search: ")
    results = search_entries(user_id, search_title)
    if not results:
        print("No matching entries found.")
    else:
        for entry in results:
            print_entry(entry)
#main journal menu for the given user
def journal_menu(user_id):
    while True:
        choice = input(
            "1. Create Entry\n2. View All Entries\n3. Search by Title\n4. Back\n"
        )
        if choice == '1':
            new_entry = create_entry()
            save_entry(user_id, new_entry)
        elif choice == '2':
            print_all(user_id)
        elif choice == '3':
            search_menu(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")