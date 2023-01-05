'''
- This script populates the inbox intially with three emails hard coded in the script. 
- It doesn't send actual emails but appends it to a sent box. 
- The check email function adds an email randomly to the inbox from a list of hard coded emails. 
- For every user choice the program displays inbox when required. 
- The emails in the inbox are colour coded according to the email category - read, unread, spam
'''

# Imports regular expresion for email validation while sending
# Got help from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/ 
# to use regular expression to validate email address
import re
# Imports random number generator for simulating new emails in inbox
import random


#==========================================================
# Creates the Email class according to the requirement
#==========================================================
class Email:
    '''
    This is Email class with from_address, has_been_read, is_spam, 
    email_contents and email_subject instance variables. It has 
    mark_as_read and mark_as_spam methods.
    '''

    # Constructor method to create an Email object with from_address
    def __init__(self, from_address):
        
        self.from_address = from_address
        self.has_been_read = False
        self.is_spam = False
        self.email_contents = ""
        self.email_subject = ""

    # Method to mark the email as read
    def mark_as_read(self):

        self.has_been_read = True

    # Method to mark the email as spam
    def mark_as_spam(self):

        self.is_spam = True


#==========================================================
# Function to create an Email instance with the constructor,
# email_contents and email_subject
#==========================================================
def add_email(from_email, email_contents, email_subject):

    email = Email(from_email)
    email.email_contents = email_contents
    email.email_subject = email_subject

    return email


#==========================================================
# Function that returns the length of the list
#==========================================================
def get_count(inbox):

    return len(inbox)


#==========================================================
# Function that returns the email
#==========================================================
def get_email(index) :

    return inbox[index]

#==========================================================
# Function that returns all unread emails
#==========================================================
def get_unread_emails():

    unread_emails = [] 
    # Checks for unread email and adds it to uread_email list
    [unread_emails.append(email) for email in inbox if not email.has_been_read]

    return unread_emails

#==========================================================
# Function that returns all spam emails
# =========================================================
def get_spam_emails():

    spam_emails = []
    # Checks for spam email and adds it to spam_email list
    [spam_emails.append(email) for email in inbox if email.is_spam]
    
    return spam_emails


#==========================================================
# Function that deletes an email
#==========================================================
def delete(email):

    inbox.remove(email)


#==========================================================
# Function that displays the content any mail box
#==========================================================
def display_mailbox(inbox : list[Email], label):

   
    print(f"\n\n{BLUE}♦▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬♦")
    print(f"                                {label}")
    print(f"♦▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬♦")
    print(f"You have {WHITE}{get_count(inbox)} ✉ {WHITE:>50}(Unread {CYAN}Read {LIGHTRED}Spam{WHITE})")
    
    # Display the email in specific colours accordingly
    for index, email in enumerate(inbox, 1) :

        if email.is_spam :
            print(f"{LIGHTRED} {index}   ✉ {email.from_address:<40} {email.email_subject:>20}")

        elif email.has_been_read :
            print(f"{CYAN} {index}   ✉ {email.from_address:<40} {email.email_subject:>20}")

        else:
            print(f"{WHITE} {index}   ✉ {email.from_address:<40} {email.email_subject:>20}")


#==========================================================
# Function that does email ID validation
#==========================================================
def id_validation(inbox):

    # Asks for the ID until a valid one is given
    while True:
            index = input(f"{BLUE}\nEnter the email ID: ")

            if not index.isdigit():
                print("Enter a valid ID!")
            # Checks if the ID is inside the length of the list
            # Also checks for 0
            elif int(index) > len(inbox) or int(index) == 0:
                print("Please select an ID from above!")
            else:
                index = int(index) - 1
                return index


#==========================================================
# Function that marks an email to spam
#==========================================================
def mark_spam(inbox : list[Email]):

    index = id_validation(inbox)

    # Marks that email instance to spam
    inbox[index].mark_as_spam()


#==========================================================
# Function to display emails
#==========================================================
def read_email(inbox : list[Email]):

   
    index = id_validation(inbox)
    
    # Checks for spam mail reading
    if inbox[index].is_spam :
        read = input("This email is spam, Do you still want to read it? y/n ").lower()
        if read == 'n' :
           return

    # Gets the email contents       
    email = get_email(index)

    # Displays the email
    print(f"{WHITE}-------------------------------------------------------------------")
    print(f"\nFrom: {email.from_address}")
    print(f"Subject: {email.email_subject}")
    print(f"\n{email.email_contents}")
    print("-------------------------------------------------------------------")

    # Marks the email as read
    email.mark_as_read()


#==========================================================
#  Function to simulate new emails
#==========================================================
def check_new_emails(inbox):

    # Creates a list of fake emails
    list_emails_to_pick = []
    list_emails_to_pick.append(add_email("somebody@abc.com", "Any one there?", "Finding"))
    list_emails_to_pick.append(add_email("anyone@xyz.com", "Nice having you at our place!", "Hi"))
    list_emails_to_pick.append(add_email("lachoo@hotmail.com", "Looking forward to see you", "Miss you"))
    list_emails_to_pick.append(add_email("tom@bbc.co.uk", "Python Developer opportunities at BBC", "Career"))
    list_emails_to_pick.append(add_email("amazon@amazonshop.com", "List products on lightning sale", "sale"))

    # Picks an email from the above list and appends it to the inbox
    inbox.append(list_emails_to_pick[random.randrange(5)])

    # Displays the inbox
    display_mailbox(inbox,"Inbox")


#==========================================================
#  Function to simulate sending emails
#==========================================================
def send_email():

    # Asks for the email address until a valid one is entered
    while True:

        email_address = input("Enter sender's email address:")

        # Accepts any number of character from A-Z, a-z, 0-9, any of these
        # symbols - (._%+-) for the first part before @ Atleast one character from 
        # A-Z, a-z  and (.-) for the second part and a . after that
        # Minimum of 2 charcters from A-Z or a-z at the end
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex,email_address) == None :
            print("Enter a valid email address!")
        else:
            break
    
    # Gets the subject and content for the email
    email_subject = input("Enter the subject: ")
    email_contents = input("Enter the content: ")

    # Creates the email object for the composed email 
    # Appends it to the sent box
    email = add_email(email_address,email_subject, email_contents)
    sentbox.append(email)

    print("Message sent!")

    return sentbox


#==========================================================
# Main Program
#==========================================================

# Creates the list for inbox and fake sentbox
inbox = []
sentbox = []

# Intialises the variables for colours
LIGHTRED = '\033[91m'
WHITE = '\033[0m'
BLUE = '\033[94m'
CYAN = '\033[96m'

# Appends the inbox to load with few pre created emails
inbox.append(add_email("xyz@abc.com", "Hello World", "Helloooooo"))
inbox.append(add_email("lyra@darkmaterials.com", "Keep Learning", "Learn"))
inbox.append(add_email("will@hisdarkmaterials.com", "Be Brave", "Brave"))

# Displays the inbox
display_mailbox(inbox,"Inbox")


# Asks for user_choice until quit or 8 is entered
while True :
    
    user_choice = input(f"\n{BLUE}What would you like to do? choose options from below (e.g. 1 or 2 etc.)?\
        \n1.Read  2.Show Unread  3.Delete  4.Mark Spam  5.Show Spam  6.Send Email  7.Check Inbox  8.Quit\n").lower()

    
    if user_choice == "1" or user_choice == "read":

        display_mailbox(inbox,"Inbox")

        # Calls the read_email and displays inbox only when there are emails in it 
        if len(inbox) > 0 :
            read_email(inbox)
            display_mailbox(inbox,"Inbox")
        else:
            print(f"\n{BLUE}You have no emails!")
        
    elif user_choice == "2" or user_choice == "show unread":

        # Gets the unread emails
        unread_emails = get_unread_emails()

        # Displays the unread box only when there are emails
        if len(unread_emails) > 0 :
            display_mailbox(unread_emails, "Unread")
        else:
            print("You have no unread emails!")
       
    elif user_choice == "3" or user_choice == "delete":

        # Asks for email ID for deletion only when there are emails in the inbox
        if len(inbox) > 0 :

            display_mailbox(inbox,"Inbox")
            index = id_validation(inbox)

            # Checks with the user before deleting
            if input("Are you sure you want to delete? y/n ").lower() == "y" :
                delete(inbox[index])
                print(f"Message Deleted!")

                # Displays the inbox after deletion
                display_mailbox(inbox, "Inbox")
        else:
            print("You have no emails!")
        
    elif user_choice == "4" or user_choice == "mark spam":

        # Asks for email ID for marking spam only when there are emails in the inbox
        if len(inbox) > 0 :  

            display_mailbox(inbox,"Inbox")

            # Calls the mark_spam()
            mark_spam(inbox)
            print(f"Message has been marked as spam!")

            # Displays the inbox after marking spam
            display_mailbox(inbox, "Inbox")
        else:
            print("You have no emails!")

    elif user_choice == "5" or user_choice == "show spam":

        # Gets all the spam emails
        spam_emails = get_spam_emails()

        # Displays it if there is any
        if len(spam_emails) > 0:
            display_mailbox(spam_emails, "Spam")
        else:
            print("No spam emails!")

    elif user_choice == "6" or user_choice == "send email":

        # Calls the function to send email
        sentbox = send_email()
        display_mailbox(sentbox, "Sent Box")

    elif user_choice == '7' or user_choice == "check inbox":

        # Checks for new emails
        check_new_emails(inbox)

    elif user_choice == "8" or user_choice == "quit":

        print("Goodbye")
        exit()

    else:
        print("Oops - incorrect input!")
