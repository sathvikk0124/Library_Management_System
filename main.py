from datetime import datetime
import json
import os

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.entry_time = None
        self.exit_time = None
        self.history = []
        self.borrowed_books = []

    def check_in(self):
        self.entry_time = datetime.now()
        self.history.append(f"Checked in at {self.entry_time}")
        print(f"{self.name} checked in at {self.entry_time}")

    def check_out(self):
        self.exit_time = datetime.now()
        self.history.append(f"Checked out at {self.exit_time}")
        print(f"{self.name} checked out at {self.exit_time}")

    def show_history(self):
        if not self.history:
            print(f"No history available for {self.name}.")
            return
        print(f"History for {self.name}:")
        for record in self.history:
            print(record)

    def show_borrowed_books(self):
        if not self.borrowed_books:
            print(f"No books borrowed by {self.name}.")
            return
        print(f"Borrowed books for {self.name}:")
        for book in self.borrowed_books:
            print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author}")

    def __str__(self):
        entry = self.entry_time.strftime('%Y-%m-%d %H:%M:%S') if self.entry_time else 'Not checked in'
        exit = self.exit_time.strftime('%Y-%m-%d %H:%M:%S') if self.exit_time else 'Not checked out'
        return f"Member ID: {self.member_id}, Name: {self.name}, Entry Time: {entry}, Exit Time: {exit}"

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.borrowed_by = None

    def __str__(self):
        borrowed_by = self.borrowed_by.name if self.borrowed_by else 'Available'
        return f"Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Borrowed By: {borrowed_by}"

class Library:
    def __init__(self):
        self.members = {}
        self.books = {}

    def add_member(self, member_id, name):
        if member_id in self.members:
            print("Member ID already exists.")
        else:
            self.members[member_id] = Member(member_id, name)
            print(f"Member {name} added.")

    def check_in_member(self, member_id):
        if member_id in self.members:
            self.members[member_id].check_in()
        else:
            print("Member ID not found.")

    def check_out_member(self, member_id):
        if member_id in self.members:
            self.members[member_id].check_out()
        else:
            print("Member ID not found.")

    def show_member_info(self, member_id):
        if member_id in self.members:
            print(self.members[member_id])
        else:
            print("Member ID not found.")

    def show_member_history(self, member_id):
        if member_id in self.members:
            self.members[member_id].show_history()
        else:
            print("Member ID not found.")

    def delete_member(self, member_id):
        if member_id in self.members:
            del self.members[member_id]
            print(f"Member ID {member_id} deleted.")
        else:
            print("Member ID not found.")

    def show_all_members_history(self):
        if not self.members:
            print("No members found.")
            return
        for member_id, member in self.members.items():
            print(f"\nHistory for Member ID {member_id} ({member.name}):")
            member.show_history()

    def modify_member(self, member_id, new_name):
        if member_id in self.members:
            self.members[member_id].name = new_name
            print(f"Member ID {member_id} name changed to {new_name}.")
        else:
            print("Member ID not found.")

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("Book ID already exists.")
        else:
            self.books[book_id] = Book(book_id, title, author)
            print(f"Book '{title}' by {author} added.")

    def borrow_book(self, book_id, member_id):
        if book_id not in self.books:
            print("Book ID not found.")
        elif member_id not in self.members:
            print("Member ID not found.")
        elif self.books[book_id].borrowed_by is not None:
            print(f"Book '{self.books[book_id].title}' is already borrowed by {self.books[book_id].borrowed_by.name}.")
        else:
            self.books[book_id].borrowed_by = self.members[member_id]
            self.members[member_id].borrowed_books.append(self.books[book_id])
            print(f"Book '{self.books[book_id].title}' borrowed by {self.members[member_id].name}.")

    def show_book_info(self, book_id):
        if book_id in self.books:
            print(self.books[book_id])
        else:
            print("Book ID not found.")

    def show_member_borrowed_books(self, member_id):
        if member_id in self.members:
            self.members[member_id].show_borrowed_books()
        else:
            print("Member ID not found.")

    def return_book(self, book_id, member_id):
        if book_id not in self.books:
            print("Book ID not found.")
        elif member_id not in self.members:
            print("Member ID not found.")
        elif self.books[book_id].borrowed_by is None:
            print(f"Book '{self.books[book_id].title}' is not currently borrowed.")
        elif self.books[book_id].borrowed_by.member_id != member_id:
            print(f"Book '{self.books[book_id].title}' is borrowed by {self.books[book_id].borrowed_by.name}, not the specified member.")
        else:
            # Remove book from member's borrowed books list
            self.members[member_id].borrowed_books.remove(self.books[book_id])
            # Update book status
            self.books[book_id].borrowed_by = None
            print(f"Book '{self.books[book_id].title}' returned by {self.members[member_id].name}.")

    def save_data(self, filename="library_data.json"):
        """Save library data to JSON file"""
        try:
            data = {
                "members": {},
                "books": {}
            }
            
            # Serialize members
            for member_id, member in self.members.items():
                data["members"][str(member_id)] = {
                    "member_id": member.member_id,
                    "name": member.name,
                    "entry_time": member.entry_time.isoformat() if member.entry_time else None,
                    "exit_time": member.exit_time.isoformat() if member.exit_time else None,
                    "history": member.history,
                    "borrowed_books": [book.book_id for book in member.borrowed_books]
                }
            
            # Serialize books
            for book_id, book in self.books.items():
                data["books"][str(book_id)] = {
                    "book_id": book.book_id,
                    "title": book.title,
                    "author": book.author,
                    "borrowed_by": book.borrowed_by.member_id if book.borrowed_by else None
                }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Library data saved to {filename}")
            
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self, filename="library_data.json"):
        """Load library data from JSON file"""
        try:
            if not os.path.exists(filename):
                print("No existing data file found. Starting with empty library.")
                return
                
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Clear existing data
            self.members = {}
            self.books = {}
            
            # Load members
            for member_id_str, member_data in data.get("members", {}).items():
                member_id = int(member_id_str)
                member = Member(member_id, member_data["name"])
                member.entry_time = datetime.fromisoformat(member_data["entry_time"]) if member_data["entry_time"] else None
                member.exit_time = datetime.fromisoformat(member_data["exit_time"]) if member_data["exit_time"] else None
                member.history = member_data["history"]
                self.members[member_id] = member
            
            # Load books
            for book_id_str, book_data in data.get("books", {}).items():
                book_id = int(book_id_str)
                book = Book(book_id, book_data["title"], book_data["author"])
                self.books[book_id] = book
            
            # Restore borrowed book relationships
            for member_id_str, member_data in data.get("members", {}).items():
                member_id = int(member_id_str)
                member = self.members[member_id]
                for book_id in member_data["borrowed_books"]:
                    if book_id in self.books:
                        book = self.books[book_id]
                        member.borrowed_books.append(book)
                        book.borrowed_by = member
            
            print(f"Library data loaded from {filename}")
            print(f"Loaded {len(self.members)} members and {len(self.books)} books")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            print("Starting with empty library.")

    def search_books(self, query):
        """Search for books by title or author"""
        query = query.lower()
        found_books = []
        
        for book in self.books.values():
            if query in book.title.lower() or query in book.author.lower():
                found_books.append(book)
        
        if found_books:
            print(f"Found {len(found_books)} book(s) matching '{query}':")
            for book in found_books:
                print(book)
        else:
            print(f"No books found matching '{query}'")

    def search_members(self, query):
        """Search for members by name"""
        query = query.lower()
        found_members = []
        
        for member in self.members.values():
            if query in member.name.lower():
                found_members.append(member)
        
        if found_members:
            print(f"Found {len(found_members)} member(s) matching '{query}':")
            for member in found_members:
                print(member)
        else:
            print(f"No members found matching '{query}'")

def get_integer_input(prompt):
    """Helper function to get integer input with error handling"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a valid integer.")

def main():
    library = Library()
    
    # Load existing data on startup
    library.load_data()
    
    while True:
        print("\nLibrary Management System")
        print("1. Add Member")
        print("2. Check In Member")
        print("3. Check Out Member")
        print("4. Show Member Info")
        print("5. Show Member History")
        print("6. Show All Members History")
        print("7. Modify Member Details")
        print("8. Delete Member")
        print("9. Add Book")
        print("10. Borrow Book")
        print("11. Show Book Info")
        print("12. Show Member Borrowed Books")
        print("13. Return Book")
        print("14. Search Books")
        print("15. Search Members")
        print("16. Exit")
        choice = input("Enter your choice (1-16): ")
        if choice == '1':
            member_id = get_integer_input("Enter member ID: ")
            name = input("Enter member name: ")
            library.add_member(member_id, name)
        elif choice == '2':
            member_id = get_integer_input("Enter member ID to check in: ")
            library.check_in_member(member_id)
        elif choice == '3':
            member_id = get_integer_input("Enter member ID to check out: ")
            library.check_out_member(member_id)
        elif choice == '4':
            member_id = get_integer_input("Enter member ID to show info: ")
            library.show_member_info(member_id)
        elif choice == '5':
            member_id = get_integer_input("Enter member ID to show history: ")
            library.show_member_history(member_id)
        elif choice == '6':
            library.show_all_members_history()
        elif choice == '7':
            member_id = get_integer_input("Enter member ID to modify: ")
            new_name = input("Enter new member name: ")
            library.modify_member(member_id, new_name)
        elif choice == '8':
            member_id = get_integer_input("Enter member ID to delete: ")
            library.delete_member(member_id)
        elif choice == '9':
            book_id = get_integer_input("Enter book ID: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(book_id, title, author)
        elif choice == '10':
            book_id = get_integer_input("Enter book ID to borrow: ")
            member_id = get_integer_input("Enter member ID to borrow to: ")
            library.borrow_book(book_id, member_id)
        elif choice == '11':
            book_id = get_integer_input("Enter book ID to show info: ")
            library.show_book_info(book_id)
        elif choice == '12':
            member_id = get_integer_input("Enter member ID to show borrowed books: ")
            library.show_member_borrowed_books(member_id)
        elif choice == '13':
            book_id = get_integer_input("Enter book ID to return: ")
            member_id = get_integer_input("Enter member ID returning the book: ")
            library.return_book(book_id, member_id)
        elif choice == '14':
            query = input("Enter search query for books (title or author): ")
            library.search_books(query)
        elif choice == '15':
            query = input("Enter search query for members (name): ")
            library.search_members(query)
        elif choice == '16':
            print("Saving library data...")
            library.save_data()
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 16.")

if __name__ == "__main__":
    main()
