#=================Dependency: tabulate module======================
#======= Install tabulate module : pip install tabulate ========
# This script requires tabulate module to be installed
# Imports tabulate module to display data organised in table format
from tabulate import tabulate


# Got help from 
# https://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory
# To run the Python script from the directory where the Python file is, 
# so that inventory.txt is accessible when placed in the same path as the Python script
import os
# Gets the path of current python script
abs_path = os.path.abspath(__file__)
# Gets the directory name of the script
dir_name = os.path.dirname(abs_path)
# Changes the current directory to the directory where the script is
os.chdir(dir_name)

# Imports regular expression for entry validation for inventory
import re


#==========================================================
# Creates the Shoe class according to the requirement
#==========================================================
class Shoe:
    '''
    This is Shoe class with country, code, product, cost and quantity instance variables.
    It has get_cost, get_quantity methods
    '''

    # Constructor method to create a Shoe object
    def __init__(self, country, code, product, cost, quantity):
        
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    # Method to get the cost of a product
    def get_cost(self):
        return self.cost

    # Method to get the quantity of a product
    def get_quantity(self):
        return self.quantity

    # __str__ for displaying the class in string format
    def __str__(self):
        # Formats the cost to 2 decimal places
        return f"{self.country},{self.code},{self.product},{self.cost:.2f},{self.quantity}"

#========End of Shoe class=================================

#==========================================================
# Function to read shoes data from inventory.txt and 
# add them to a list
#==========================================================
def read_shoes_data():
    '''
    This function opens the file inventory.txt and reads the data from this file, 
    then creates a shoes object with this data and appends this object into the shoe
    list. One line in this file represents data to create one object of shoes. It 
    returns the shoe list. 
    '''
    shoe_list = []

    # Handles FileNotFoundError
    try:
        with open("inventory.txt", "r", encoding= "utf-8") as inventory_file :

            # Skips the first entry
            next(inventory_file)
            
            # splits each line with "," and gets the data
            for entry in [line.split(",") for line in inventory_file] :
                country = entry[0]
                code = entry[1]
                product = entry[2]

                # Converts the cost to float and rounds it to 2 decimal places
                cost = round(float(entry[3]),2)
                # Converts the quantity to int 
                quantity = int(entry[4].strip())
                # Appends the data to the shoe_list
                shoe_list.append(Shoe(country, code, product, cost, quantity))
                
    except FileNotFoundError:
            print("\nThe file does not exist! Please check the directory.")
            shoe_list = None

    return shoe_list


#==========================================================
# Function to search shoe object from a list based 
# on product code
#==========================================================
def search_shoe(shoe_list, code):
    '''
     This function searches for a shoe from the list
     using the shoe code and returns this object.
    '''

    shoe = None

    # Searches for shoe object in the list with the matching code
    for s in shoe_list:
        if s.code == code:
            shoe = s
            break
    
    return shoe
   

#==========================================================
# Function to get and validate code
#==========================================================
def get_validate_code():
    '''
    This function gets the input from the user until a valid code is given
    and returns the code.
    '''

    # Asks for a code until a valid one is given
    while True:

        code = input("\nEnter the five digit product code: SKU")
        
        # Accepts only 5 digits
        regex = r'[0-9]{5}'
        if re.fullmatch(regex, code) == None :
            print(f"Enter a valid code!")
        else:
            code = "SKU" + code
            break

    return code


#==========================================================
# Function to get entries from the user for new product
#==========================================================
def capture_shoes(shoe_list):
    '''
    This function get data from the user about a shoe 
    and uses this data to create a shoe object
    and appends this object inside the shoe list.
    It also appends the new data into inventory.txt
    and returns the shoe_list
    '''

    # Calls get_validate_code() to get the input from the user and validates it
    # until a valid one is given
    while True:
        code = get_validate_code()

        # Checks if a product already exists using the code using search_shoe()
        if search_shoe(shoe_list, code) != None:
            print("This product already exist!")
        else:
            break

    # Asks for country until a valid entry is given 
    while True:

        country = input("Enter the Country: ")
        # Accepts atleast two or more number of alphabets with spaces
        regex = r'[A-Za-z\s]{2,}\b'

        if re.fullmatch(regex, country) == None :
            print(f"Enter a valid country!")
        else:
            break

    # Asks for product name until a valid one is given         
    while True:

        product = input("Enter the product name: ").strip()
        # Accepts atleast three alphabets with spaces at the start which 
        # may or may not be followed by numbers 
        regex = r'\b[A-Za-z\s]{3,}[0-9]*\b'

        if re.fullmatch(regex, product) == None :
            print(f"Enter a valid product name!")
        else:
            break  

    # Asks for cost of the product untlil a valid one is given
    while True:

        cost = input("Enter the cost: ")
        
        # Handles the validation for float
        try:
            cost = round(float(cost),2)
            break

        except ValueError:
           print(f"Enter a valid cost!")

    # Asks for the quantity of the product until a valid one is given
    while True:

        quantity = input("Enter the quantity: ")
        
        if quantity.isdigit():
            quantity = int(quantity)
            break
        else:
           print(f"Enter a valid quantity!")

    # Creates a Shoe object with user input
    shoe = Shoe(country, code, product, cost, quantity)
    # Appends the object to the end of the list
    shoe_list.append(shoe)
    
    # Gets the string representation of the object for appending to inventory.txt
    shoe =  "\n" + f"{shoe}"

    # Handles the Permission Error when not able to access the file
    try:

        with open("inventory.txt", "a") as inventory_file :
            inventory_file.write(shoe)

        print("\nThe new product has been added successfully!")

    except PermissionError:
        print("You do not have permission to edit inventory.txt!")

    return shoe_list
    

#==========================================================
# Function to view all the stock in the shoe_list
#==========================================================
def view_all(shoe_list):
    '''
    This function iterates over the shoe_list and
    prints the details of the shoes in a table format 
    using tabulate module.
    '''
    # Creates the header for the table using colour green and initialises the table 
    headers = [G+"Country"+W, G+"Code"+W, G+"Product Name"+W, G+"Cost"+W, G+"Quantity"+W]
    table = []
    
    # Processes each string representation of the shoe object for tabulate
    for shoe in shoe_list :
        
        shoe = f"{shoe}".split(",")
        table.append(shoe)

    print("\n")
    # Uses tabulate to print with specified formatting
    print(tabulate(table, headers, tablefmt="grid", floatfmt=".2f"))
    

#==========================================================
# Function to search for shoes with the specified quantity
#==========================================================
def search_shoes_with_quantity(shoe_list, quantity):
    '''
    This function searches for a shoe object with the specified quantity 
    from the shoe list and returns a list of shoes.
    '''
    shoes = []

    # Appends the shoe object with the matching quantity into a list
    for s in shoe_list:
        if s.quantity == quantity:
            shoes.append(s)
            
    return shoes


#==========================================================
# Function to restock the products with the lowest stock
#==========================================================
def re_stock(shoe_list):
    '''
    This function finds the shoe objects with the lowest quantity,
    which is the shoes that needs to be re-stocked. It asks the user if they
    want to add more quantity of shoes and then updates the shoe_list.
    This quantity is also updated on the file for the shoes.
    '''

    # Uses lambda for key in min funtion to check minimum based on quantity
    low_stock_shoe = min(shoe_list, key=lambda shoe:shoe.quantity)
    min_quantity = low_stock_shoe.quantity

    # Calls the search_shoes_with_quantity() to get a list of shoes with the specified quantity
    low_stock_shoes = search_shoes_with_quantity(shoe_list, min_quantity)

    # Asks the user for the quantity to be added for each shoe in the low stock list
    for shoe in low_stock_shoes:
        print(f"\n{shoe.product}: {shoe.code} has only {shoe.quantity} in stock")

        # Validates the user entry for quantity
        while True:
            quantity = input(f"How many do you want to restock? ")
            if quantity.isdigit():
                shoe.quantity += int(quantity)
                break
            else:
                print("Enter a valid quantity!")
        
        # Updates the shoe_list with the newly calculated quantity
        shoe_list[shoe_list.index(shoe)] = shoe

    # Handles FileNotFoundError
    try:
        # Writes the updated entries to the file
        with open("inventory.txt", "r+", encoding="utf-8" ) as inventory_file :
            # Preserves the first line
            first_entry = inventory_file.readline().strip()

            # Rewrites the file from the beginning 
            inventory_file.seek(0)
            inventory_file.write(first_entry)

            # Writes each shoe object from the list
            for shoe in shoe_list:
                shoe = "\n" + f"{shoe}"
                inventory_file.write(shoe)

        print(f"\nThe product(s) with low stocks have been updated successfully!")    

    except FileNotFoundError:
        print("The file inventory.txt not found!")
    

#==========================================================
# Function to print the value for each shoe
#==========================================================
def value_per_item(shoe_list):
    '''
    This function calculates the total value for each item.
    It prints this information on the console for all the shoes
    in table format using tabulate.
    '''

    # Creates the header for the table using colour green and intialises the table
    headers = [G+"Product"+W, G+"Code"+W, G+"Quantity"+W, G+"Cost"+W, G+"Value"+W]
    table = []

    # Calculates the value for each shoe in the list
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        table.append([shoe.product, shoe.code, shoe.quantity, shoe.cost, value])
    
    print("\n")
    # Uses tabulate to print with specified formatting
    print(tabulate(table, headers, tablefmt="grid", floatfmt=".2f"))
    

#==========================================================
# Function to print the shoes with the highest quantity
#==========================================================
def highest_qty(shoe_list):
    
    '''
    This funtion prints the shoes with highest quantity for sale
    '''

    headers = [G+"Product"+W, G+"Code"+W]
    table = []
    
    # Uses lambda for key in max funtion to check maximum based on quantity
    high_stock_shoe = max(shoe_list, key=lambda shoe:shoe.quantity)
    max_quantity = high_stock_shoe.quantity

    # Calls the search_shoes_with_quantity() to get a list of shoes with the max quantity
    high_stock_shoes = search_shoes_with_quantity(shoe_list, max_quantity)

    print(f"\n\nThe following product(s) has the highest stock of {max_quantity}:")
    for shoe in high_stock_shoes:
        table.append([shoe.product, shoe.code])

    # Uses tabulate to print with the specified format with green header   
    print(tabulate(table, headers, tablefmt="grid"))
    print(f"So they are for sale!\n")

    
#==========================================================
# Main Program
#==========================================================

# Initialises shoe_list for storing a list of shoe objects
shoe_list = []

# Assigns the Green and White colour variables G and W for use in tabulate
G = '\033[92m'
W = '\033[0m'

# Asks the user to choose from the options specified
while True:
    
    # Gets the latest shoe list data from inventory.txt
    shoe_list = read_shoes_data()

    print("\n\n🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰\n")
    user_choice = input(f"What would you like to do? choose options from below (e.g. 1 or 2 etc.)?\
                        \n1. Search Stock With Code\
                        \n2. View All Stock\
                        \n3. Add Product\
                        \n4. Restock\
                        \n5. Show High Stock\
                        \n6. Stock Values \
                        \n7. Quit\
                        \n\n🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰\n").lower()

    if user_choice == "1":
        
        # Gets and validates the code from the user
        code = get_validate_code()

        # Searches the shoe for the code
        shoe = search_shoe(shoe_list, code)
        if shoe == None:
            print("Shoe not found")
        else:
            # Creates the header for the searched shoe
            headers = [G+"Country"+W, G+"Code"+W, G+"Product Name"+W, G+"Cost"+W, G+"Quantity"+W]
            table = []

            # Processes the shoe and displays the shoe info in table format 
            shoe = f"{shoe}".split(",")
            table.append(shoe)
            print("\n")
            print(tabulate(table, headers, tablefmt="grid", floatfmt=".2f"))

    elif user_choice == "2":
        # Calls the view_all()
        view_all(shoe_list)
    
    elif user_choice == "3":
        # Calls the funtion to add a product
        capture_shoes(shoe_list)
    
    elif user_choice == "4":
        # Calls the function to restock the shoes
        re_stock(shoe_list)

    elif user_choice == "5":
        # Calls the function to display the highest quantity shoes 
        highest_qty(shoe_list)
    
    elif user_choice == "6":
        # Calls the function to display the values for each shoe
        value_per_item(shoe_list)
    
    elif user_choice == "7":
        print("Goodbye")
        exit()
    
    # For invalid entry
    else:
        print("Invalid entry - Please try again!")
