# Learnt Tkinter from https://www.tutorialspoint.com/ and https://realpython.com/python-gui-tkinter/
# Learnt about clearing the tree in tkinter from this https://stackoverflow.com/questions/22812134/how-to-clear-an-entire-treeview-with-tkinter
# Learnt about creating the modal window from https://stackoverflow.com/questions/16803686/how-to-create-a-modal-dialog-in-tkinter
# Learnt about passing focus and rasing window in Tkinter from https://stackoverflow.com/questions/48352645/how-do-i-correctly-pass-focus-to-and-from-a-message-box-in-python-3-in-windows
# Learnt about changing background colour for Tkinter windows from https://pythonexamples.org/python-tkinter-window-background-color/

# This script expects data folder to be in the same path as the Python script
# and execute from the file's directory to be set in VS code.

# Imports sqlite3 for database
import sqlite3

# Imports Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Imports regular expression for entry validation
import re


#==========================================================
# Creates the Book class according to the requirement
#==========================================================
class Book():
    '''
    This is Book class with id, title, author and quantity instance variables.
    It has to_list method to convert the object into a list.
    '''
    # Constructor method to create a Book object
    def __init__(self, id, title, author, quantity):
        self.id = id
        self.title = title
        self.author = author
        self.quantity = quantity

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author
    
    def get_quantity(self):
        return self.quantity

    # __str__ for displaying the object in string format
    def __str__(self):
        return f'{self.id} {self.title} {self.author} {self.quantity}'

    # Method to convert the book object into a list
    def to_list(self):
        return [self.id, self.title, self.author, self.quantity]


#==========================================================
# Database functions
#==========================================================
#==========================================================
# Function to create the table and populate the database
#==========================================================
def create_populate_db():
    '''
    This function creates the table and populates the database
    and returns any error message from the database.
    '''
    message = ""
    db = None

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Gets the table name to check if the table exists
        cursor.execute('''SELECT name FROM SQLITE_MASTER WHERE TYPE = "table" and NAME = "books"''')
        if len(cursor.fetchall()) == 0:
        
            # Creates the table as required
            cursor.execute('''
                CREATE TABLE books
                (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
            ''')

            # Populates the table
            book_list = [Book(3001,"A Tale of Two Cities", "Charles Dickens", 30).to_list(),
                        Book(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40).to_list(),
                        Book(3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25).to_list(),
                        Book(3004, "The Lord of the Rings", "J.R.R Tolkien", 37).to_list(),
                        Book(3005, "Alice in Wonderland", "Lewis Carroll", 12).to_list()]
            
            cursor.executemany('''INSERT INTO books VALUES(?,?,?,?)''', book_list)
            db.commit()

    # Handles errors regarding database creation and path
    except sqlite3.OperationalError as oe:
       message = f"\nCheck if the data folder exists in the same folder as the script.\
        \nAlso execute the script from its directory.\n\nAdditional info: {oe}"

    # Handles any other exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'Something unforseen has happened with the database. Please try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()

    return message


#==========================================================
# Function to retrieve books from the table
#==========================================================
def retrieve_books():
    '''
    This function retrieves the books from the table and
    returns the list containing those book objects and 
    any database error message.
    '''
    book_list = []
    db = None
    message = ""

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Gets the content of the table and creates a list of book objects
        cursor.execute('''SELECT id, Title, Author, Qty FROM books''')
        for row in cursor:
            id = row[0]
            title = row[1]
            author = row[2]
            quantity = row[3]
            book = Book(id, title, author, quantity) 
            book_list.append(book)

    # Handles any other exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f"Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}"

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()
    
    return message, book_list
    

#==========================================================
# Function to get the next book id from the table
#==========================================================
def next_book_id():
    '''
    This function gets the next book id from the table and any 
    error message from the database.
    '''
    db = None
    message = ""
    book_id = 0

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()
        
        # Gets the highest id of the table
        cursor.execute('''SELECT MAX(id) FROM books''')
        for row in cursor:
            last_book_id = row[0]

        book_id = last_book_id + 1
    
    # Handles any other exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
       message = f'Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()
    
    return message, book_id


#==========================================================
# Function to insert a book record into the table
#==========================================================
def create_book(book_entry):
    '''
    This function inserts a book record into the table and returns 
    any error message from the database.
    '''
    db = None
    message = ""

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Inserts the record into the database
        book_entry = book_entry.to_list()
        cursor.execute('''INSERT INTO books VALUES(?,?,?,?)''', book_entry)
        db.commit()

    # Handles any exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()
    
    return message


#==========================================================
# Function to delete a record from the table
#==========================================================
def delete_book(book_entry):
    '''
    This functions deletes a record from the table and returns 
    any error message from the database.
    '''
    db = None
    message = ""

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Deletes a book from the database
        cursor.execute('''DELETE FROM books WHERE id = ?''', (book_entry.get_id(),))
        db.commit()
    
    # Handles any exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()

    return message


#==========================================================
# Function to search books from the table
#==========================================================
def search_books(id, title, author):
    '''
    This function searches books based on id, title and author and returns 
    the list containing those book objects and any database error message.
    '''
    is_execute = True
    book_list = []
    message = ""    
    db = None
    
    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # constructs and executes the sql query according to the input
        if len(title) > 0 and len(author) > 0 and len(id) > 0 :
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ? OR Title LIKE ? OR Author LIKE ?''', (id, "%"+title+"%", "%"+author+"%"))
            
        elif len(title) > 0 and len(author) > 0 and len(id) == 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Title LIKE ? OR Author LIKE ?''', ("%"+title+"%", "%"+author+"%"))
            
        elif len(title) > 0 and len(author) == 0  and len(id) > 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ? OR Title LIKE ?''', (id, "%"+title+"%"))

        elif len(title) == 0 and len(author) > 0  and len(id) > 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ? OR Author LIKE ?''', (id, "%"+author+"%"))

        elif len(title) == 0 and len(author) == 0  and len(id) > 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ?''', (id,))
        
        elif len(title) > 0 and len(author) == 0  and len(id) == 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Title LIKE ?''', ("%"+title+"%",))
        
        elif len(title) == 0 and len(author) > 0  and len(id) == 0:
            cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Author LIKE ?''', ("%"+author+"%",))

        elif len(title) == 0 and len(author) == 0 and len(id) == 0 :
            is_execute = False
            message = "Please enter atleast one criteria and try again!"

        # Gets the records if an entry is given
        if is_execute == True:
            records = cursor.fetchall()
            
            if len(records) == 0:
                message = "No matches found!"
            else:
                # Creates a list of book objects from the search
                for row in records:
                    id = row[0]
                    title = row[1]
                    author = row[2]
                    quantity = row[3]
                    book = Book(id, title, author, quantity) 
                    book_list.append(book)
            
    # Handles any exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()

    return message, book_list  
    

#==========================================================
# Function to update a book entry in the table
#==========================================================
def update_book(book_entry):
    '''
    This function updates a book entry in the table and returns
    any database error message.
    '''
    db = None
    message = ""

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Updates a book entry
        cursor.execute('''UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ?''',
            (book_entry.get_title(), book_entry.get_author(), book_entry.get_quantity(), book_entry.get_id()))
        db.commit()

    # Handles any exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'Something unforseen has happened with the database.\nPlease try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()

    return message


#==========================================================
# Function to get books with the lowest stock from 
# the table
#==========================================================
def get_lowest_stock_books():
    '''
    This function gets book with the lowest stock from the table
    and returns the list containing those book objects and any
    database error message.
    '''
    message = ""
    db = None
    book_list = []

    try:
        db = sqlite3.connect("data/ebookstore")
        cursor = db.cursor()

        # Gets the quantities with minimum stock
        cursor.execute('''SELECT MIN(Qty) FROM books''')
        for row in cursor:
            lowest_qty = row[0]
        
        # Gets the records with the minimum quantity
        cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE Qty = ?''', (lowest_qty,))
        
        # Creates the list of book objects with the minimum quantity
        for row in cursor:
            id = row[0]
            title = row[1]
            author = row[2]
            quantity = row[3]
            book = Book(id, title, author, quantity) 
            book_list.append(book)
    
    # Handles any exception related to database due to unforseen circumstances
    except sqlite3.DatabaseError as de:
        message = f'\nSomething unforseen has happened with the database. Please try again!\n\nAdditional info: {de}'

    finally:
        # Checks for the database connection and closes it
        if db:
            db.close()

    return message, book_list
    

#==========================================================
# Front-end functions
#==========================================================
#==========================================================
# Function to display all books' records
#==========================================================
def display_books(book_list):
    '''
    This function displays the list of books in the Treeview tree
    '''
    # Clears the tree of previous entries
    tree.delete(*tree.get_children())
    count = 0

    # Inserts the entries for odd and even rows in two different colours
    for book in book_list:
        book_entry = book.to_list()
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text="", values=(book_entry), tag="evenrow")
        else:
            tree.insert(parent='', index='end', iid=count, text="", values=(book_entry), tag="oddrow")
        count += 1


#==========================================================
# Function to display the lowest stock
#==========================================================
def show_lowest_stock():
    '''
    This function displays the books with the lowest stock 
    or displays any error message from the database
    '''
    message, book_list = get_lowest_stock_books()
    # Uses display_book to display the book entries
    if len(message) == 0:
        display_books(book_list)
    else:
        messagebox.showerror(parent=window, title="Error", message=message)
        exit()


#==========================================================
# Function to show all records
#==========================================================
def show_all(cmd):
    '''
    This function displays all book records
    '''
    # Retrieves the latest entries from the table and displays them
    message, book_list = retrieve_books()
    if len(message) == 0:
        if len(cmd) > 0:
            messagebox.showinfo(parent=pop, title="Info", message=f"Book {cmd}d successfully.")
        display_books(book_list)
    else:
        messagebox.showerror(parent=window, title="Error", message=message)
        exit()


#==========================================================
# Function to display the modal window on Enter, Update
# and Delete button click
#==========================================================
def pop_window(cmd):
    '''
    This function displays the modal window on Enter, Update
    and Delete button click. Further, it gets the option for Confirm 
    or Cancel for each options.
    '''
    # Creates a modal window with the following attributes
    global pop
    pop = tk.Toplevel(window)
    pop.title("Book")
    pop.geometry("750x300")
    pop.configure(bg="#FFFFB9")
    # Deletes this window on clicking cancel or confirm
    pop.protocol("WM_DELETE_WINDOW", close_pop)

    # Disables the parent window
    window.wm_attributes("-disabled", True)

    # Creates the frame inside the window
    data_frame = tk.LabelFrame(pop, text="Book")
    data_frame.pack(expand="yes", padx=20)
    data_frame.configure(bg="#FFFFB9")
    
    # Gets the parent window's dimensions and places the pop window accordingly
    window_x = window.winfo_rootx()
    window_y = window.winfo_rooty()
    pop_x = window_x + 50
    pop_y = window_y + 50
    pop.geometry(f'+{pop_x}+{pop_y}')

    # Places the label inside the frame
    label_id = tk.Label(data_frame, text="Id", font=('Verdana', 10), bg="#FFFFB9")
    label_title = tk.Label(data_frame, text="Title", font=('Verdana', 10), bg="#FFFFB9")
    label_author = tk.Label(data_frame, text="Author", font=('Verdana', 10), bg="#FFFFB9")
    label_quantity = tk.Label(data_frame, text="Quantity", font=('Verdana', 10), bg="#FFFFB9")

    # Gives position for those labels
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    label_title.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    label_author.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    label_quantity.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    # Places the entry boxes inside the frame
    entry_id = tk.Entry(data_frame, width=20, bd=2, font=('Verdana', 10))
    entry_title = tk.Entry(data_frame, width=65, bd=2, font=('Verdana', 10))
    entry_author = tk.Entry(data_frame, width=50, bd=2, font=('Verdana', 10))
    entry_quantity = tk.Entry(data_frame, width=20, bd=2, font=('Verdana', 10))

    # Gives position for those entry boxes
    entry_id.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    entry_title.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w") 
    entry_author.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    entry_quantity.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")
    
    if cmd == "create":
        
        # Calls the next_book_id() for id to be populated automatically for create
        message, book_id = next_book_id()
        # Checks for error message from the database
        if len(message) == 0:
            entry_id.insert(0,book_id)
        else:
            # Pops any error message from the database and exits
            messagebox.showerror(parent=pop, title="Error", message=message)
            exit()
        
        # Disables the entry box for id
        entry_id.config(state="disabled")

    # Gets the focused book entry from TreeView tree in the parent window for update and delete
    # and displays it in the entry boxes of the pop window
    elif cmd == "update" or cmd == "delete":
        focused_book = tree.focus()
        book = tree.item(focused_book, "values")
        entry_id.insert(0, book[0])
        entry_id.config(state="disabled")
        entry_title.insert(0, book[1])
        entry_author.insert(0, book[2])
        entry_quantity.insert(0, book[3])

        # Disables the entry boxes for delete
        if cmd == "delete":
            entry_title.config(state="disabled")
            entry_author.config(state="disabled")
            entry_quantity.config(state="disabled")
            
    # Creates the Confirm button and assigns save() function to the command
    button_confirm = tk.Button(data_frame, text="Confirm", font=('Verdana', 10), bg="#d6ca27", 
        command= lambda: save(cmd, entry_id.get(), entry_title.get().strip(), entry_author.get().strip(), entry_quantity.get().strip()))
    button_confirm.grid(row=4, column=1, columnspan=1, padx=10, pady=10, sticky="e")

    # Creates the Cancel button and assigns the close_pop function
    button_delete = tk.Button(data_frame, text="Cancel", font=('Verdana', 10), bg="#d6ca27", command=close_pop)
    button_delete.grid(row=4, column=2, columnspan=1, padx=10, pady=10, sticky="w")


#==========================================================
# Function to validate the entries in title, author
# and quantity entry boxes
#==========================================================
def validate(id, title, author, quantity):
    '''
    This function validates the input in title, author and
    quantity entry boxes and returns a book object and any 
    error message
    '''
    message = ""
    book = None    

    # Accepts any characters for book, but should be in the length of 3 to 50
    title = title.strip()
    if len(title) > 50 or len(title) < 3:
        message = "Title should be between 3 and 50 characters in length!\n\n"
            
    author = author.strip()
    # Accepts a string starting with upper case alphabet followed by
    # atleast three or more of alphabets or spaces or '.' or '-' or "'"
    regex = r"^[A-Z]+[A-Za-z-\s.']{3,}"
    if re.fullmatch(regex, author) == None :
        message += "Author name should start with a capital letter and should \
        have a minimum of 4 characters including space(in between), hypen, dot and single quote!\n\n"
    
    quantity = quantity.strip()
    # Checks if the quantity is a positive integer
    if quantity.isdigit():
            quantity = int(quantity)
    else:
        message += "Enter a positive integer for quantity!\n"

    # Creates the book object from the entries after validation
    if len(message) == 0:
        book = Book(id, title, author, quantity)
    
    return message, book


#==========================================================
# Function that calls the validate function and then calls 
# the corresponding back-end functions based on the command
#==========================================================
def save(cmd, id, title, author, quantity):
    '''
    This function calls the corresponding back-end fucntion based on 
    the command to update, delete or create book record in the table
    '''
    # Handles delete command
    if cmd == "delete":
        book = Book(id, title, author, quantity)
        message_from_delete = delete_book(book)
        if len(message_from_delete) > 0:
            messagebox.showerror(parent=pop, title="Error", message=message_from_delete)
            exit()
        
        show_all(cmd)
        close_pop()

    else:
        # Validates the entry boxes' entries
        validate_message, book = validate(id, title, author, quantity)

        if len(validate_message) == 0:
            # Handles the create command
            if cmd == "create" :
                message_from_create = create_book(book)
                if len(message_from_create) > 0:
                    messagebox.showerror(parent=pop, title="Error", message=message_from_create)
                    exit()

            # Handles the update command
            elif cmd == "update" :
                message_from_update = update_book(book)
                if len(message_from_update) > 0:
                    messagebox.showerror(parent=pop, title="Error", message=message_from_update)
                    exit()

            show_all(cmd)
            close_pop()

        else:
            # Displays the validation error messages
            click_ok = messagebox.showerror(parent=pop, title="Error", message=validate_message)


#==========================================================
# Function to close the pop up modal window
#==========================================================
def close_pop():
    '''
    This function closes the pop up modal window 
    and enables the parent window.
    '''
    pop.destroy()
    window.wm_attributes("-disabled", False)
    window.tkraise()


#==========================================================
# Function to validate if one record is selected for update
# and delete operations
#==========================================================
def update_delete_validation(operation):
    '''
    This function validates if one record is selected in the
    parent window when update or delete button is clicked
    '''
    selected_records = tree.selection()
    # Calls the modal pop up window only when one entry is selected
    if len(selected_records) == 1:
        pop_window(operation)
    elif len(selected_records) > 1:
        messagebox.showwarning("Warning", "Please select only one record!")
    else:
         messagebox.showwarning("Warning", "Please select one record!")


#==========================================================
# Function that calls the search_books() and displays the 
# returned book
#==========================================================
def get_books():
    '''
    This function displays the searched book and also 
    displays any error message from the database.
    '''
    # Gets the entries from search frame
    id = search_entry_id.get().strip()
    title = search_entry_title.get().strip()
    author = search_entry_author.get().strip()

    # Calls the search_books()
    message, book_list = search_books(id, title, author)

    # Either display the error message from the database or displays the book
    if message.find("database") > 0:
        messagebox.showerror(parent=window, title="Error", message=message)
        exit()
    elif len(book_list) == 0:
        messagebox.showinfo("Info", message)
    else:
        display_books(book_list)

    # clears the entry boxes in the search frame
    search_entry_id.delete(0, "end")
    search_entry_title.delete(0, "end")
    search_entry_author.delete(0, "end")


#==========================================================
# Main function
#==========================================================
# Creates the parent window
window = tk.Tk()
window.title("Book Store")
window.geometry("900x600+50+50")
window.configure(bg="#FFFFB9")

# Gives the styling for the window
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", foreground="black", rowheight=25, font=('Verdana', 10))

# Creates the frame to place the tree
tree_frame = tk.Frame(window)
tree_frame.pack(pady=10)

# Adds veritical scrollbar to the tree frame and places the scroll accordingly
tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

# Creates the Treeview tree
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
tree_scroll.config(command=tree.yview)

# Packs the tree with headings and columns accordingly
tree.pack()
tree['columns'] = ("id", "title", "author", "quantity")
tree.column("#0", width=0, stretch="no")
tree.column("id", anchor="w", width=50)
tree.heading("id", text="Id", anchor="w")
tree.column("title", anchor="w", width=300)
tree.heading("title", text="Title", anchor="w")
tree.column("author", anchor="w", width=200)
tree.heading("author", text="Author", anchor="w")
tree.column("quantity", anchor="w", width=50)
tree.heading("quantity", text="Quantity", anchor="w")

# Creates tag for the tree for odd and even rows to have different colour
tree.tag_configure('oddrow', background='#d6ca27', font=('Verdana', 8))
tree.tag_configure('evenrow', background='#e5ed6f', font=('Verdana', 8))

# Creates the search_frame
search_frame = tk.LabelFrame(window, text="Search")
search_frame.pack(expand="yes", padx=20)
search_frame.configure(bg="#FFFFB9")

# Creates the id, title and author labels in the search_frame
search_id = tk.Label(search_frame, text="Id", font=('Verdana', 10), bg="#FFFFB9")
search_title = tk.Label(search_frame, text="Title", font=('Verdana', 10), bg="#FFFFB9")
search_author = tk.Label(search_frame, text="Author", font=('Verdana', 10), bg="#FFFFB9")

# Places them in the search frame
search_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
search_title.grid(row=1, column=0, padx=10, pady=10, sticky="e")
search_author.grid(row=2, column=0, padx=10, pady=10, sticky="e")

# Creates the entry boxes for id, title and author in the search frame 
search_entry_id = tk.Entry(search_frame, width=10, bd=2, font=('Verdana', 10))
search_entry_title = tk.Entry(search_frame, width=65, bd=2, font=('Verdana', 10))
search_entry_author = tk.Entry(search_frame, width=50, bd=2, font=('Verdana', 10))

# Places them in the search frame
search_entry_id.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky="w")
search_entry_title.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
search_entry_author.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

# Creates the Search button in the search_frame and assigns the get_book function to the command
button_search = tk.Button(search_frame, text="Search Books", font=('Verdana', 10), bg="#d6ca27", command=get_books)
button_search.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="w")

# Creates the Show All button in the search frame and assings the show_all function to the command
button_show_all = tk.Button(search_frame, text="Show All", font=('Verdana', 10), bg="#d6ca27", command=lambda: show_all(""))
button_show_all.grid(row=3, column=2, columnspan=1, padx=10, pady=10, sticky="w")

# Creates the Show Lowest Stock button in the search frame and assigns the show_lowest_stock function to the command
button_show_lowest_stock = tk.Button(search_frame, text="Show Lowest Stock", font=('Verdana', 10),
bg="#d6ca27", command=show_lowest_stock)
button_show_lowest_stock.grid(row=3, column=3, columnspan=1, padx=10, pady=10, sticky="w")

# Creates the button frame for the Enter, Update and Delete buttons
button_frame = tk.LabelFrame(window)
button_frame.pack(expand="yes", padx=20)
button_frame.configure(bg="#FFFFB9")

# Creates Enter Book button in the button frame and assigns pop_window() to the command
button_add = tk.Button(button_frame, text="Enter Book", font=('Verdana', 10), bg="#d6ca27",
command= lambda: pop_window("create"))
button_add.grid(row=12, column=1, columnspan=1, padx=20, pady=20)

# Creates Update Book button in the button frame and assigns the update_delete_validation("update") to the command
button_update = tk.Button(button_frame, text="Update Book", font=('Verdana', 10), bg="#d6ca27",
command= lambda: update_delete_validation("update"))
button_update.grid(row=12, column=2, columnspan=1, padx=20, pady=20)

# Creates Delete Book button in the button frame and assigns update_delete_validation("delete") to the command
button_delete = tk.Button(button_frame, text="Delete Book", font=('Verdana', 10), bg="#d6ca27",
command= lambda: update_delete_validation("delete"))
button_delete.grid(row=12, column=3, columnspan=1, padx=20, pady=20)

# Creates Exit button in the button frame and assigns exit() to the command
button_exit = tk.Button(button_frame, text="Exit", font=('Verdana', 10), bg="#d6ca27", command= lambda:exit())
button_exit.grid(row=12, column=4, columnspan=1, padx=20, pady=20)

list_books = []

# Calls the function to create the database and book table and populate it for the first time
message = create_populate_db()
if len(message) > 0:
    messagebox.showerror(parent=window, title="Error", message=message)
    exit()

# Displays the books in the window when the application loads for the first time
message, list_books = retrieve_books()
if len(message) == 0:
    display_books(list_books)
else:
    messagebox.showerror(parent=window, title="Error", message=message)
    exit()

# Call the parent window to display   
window.mainloop()
