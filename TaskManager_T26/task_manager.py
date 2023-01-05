#=====Importing libraries===========
# Imports the date module for date validation and getting the curent date
from datetime import datetime

# Got help from 
# https://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory
# To run the Python script from the directory where the Python file is, 
# so that the text files are accessible when placed in the same path as the Python script
import os
# Gets the path of current python script
abs_path = os.path.abspath(__file__)
# Gets the directory name where the script is located
dir_name = os.path.dirname(abs_path)
# Changes the current directory to the directory where the script is
os.chdir(dir_name)

#==========================================================
# Function for user validation
#==========================================================
def user_validation(task_username):

    username_check = False
    # Opens the file for username existence check and uses boolean value for it
    with open("user.txt", "r", encoding="utf-8") as user_file :
        for entry in [line.split(", ") for line in user_file] :

            if task_username == entry[0] :
                username_check = True
                break
            
    return username_check


#==========================================================
# Function for registering a new user
#==========================================================
def reg_user(admin):
    
    # Checks if the user is admin to let only admin user do the registration
    if admin :
        # Asks the user for username until it is unique
        while True:
            new_username = input("\nEnter the new username: ")

            if not user_validation(new_username):
                break
            else:
                print("\nUsername already taken!\n")

        # Asks the user for password and reconfirmation password until both matches
        while True :
            new_password = input("\nEnter your new password: ")
            confirm_new_password = input("Confirm your password: ")

            if new_password == confirm_new_password :
                # Registers a new user
                with open("user.txt", "a") as user_file :
                    user_file.write(f"\n{new_username}, {new_password}")
                    print("\nNew user credentials added!\n")
                    break

            else:
                print("\nThe passwords doesn't match! Please re-enter and confirm again.\n")

    else:
        print("\nYou have made a wrong choice, Please try again\n")


#==========================================================
# Function for date validation
#==========================================================
def date_validation(task_due_date):

    try:
        # Checks for past date and displays message accordingly
        if datetime.strptime(task_due_date,"%d %m %Y").date() >= datetime.today().date() :
            # Converts the user entry to desired format for files
            task_due_date = datetime.strptime(task_due_date,"%d %m %Y").strftime("%d %b %Y")
            return True, task_due_date

        else:
            print("\nDue date cannot be in the past!\n")
            return False, None

    except ValueError:
            print("\nInvalid Date\n")
            return False, None


#==========================================================
# Function for adding a task for a user
#==========================================================
def add_task():

    # Asks the user for a username for a task until the username exists
    while True:
        task_username = input("\nEnter the user you want to assign the task to: ")

        if user_validation(task_username):
            break
        else:
            print("\nInvalid username. Username does not exist!\n")

    # Asks the user for the title of the task until a valid entry is given
    while True:
        task_title = input("\nTitle of the task: ")
        # Replaces ^ for any commas given in the title entry since commas are used as entry delimiters 
        task_title = task_title.replace(",", "^")

        if len(task_title.strip()) == 0 :
            print("\nInvalid title of the task!\n")
        else:
            break
        
    # Asks the user for the title description of the task until a valid entry is given
    while True:
        task_desc = input("\nDescription of the task: ")
        # Replaces ^ for any commas given in the title entry since commas are used as entry delimiters
        task_desc = task_desc.replace(",", "^")

        if len(task_desc.strip()) == 0 :
            print("\nInvalid description of the task!\n")
        else:
            break
    
    # Asks the user for due date until a valid entry is given
    while True:
        task_due_date = input("\nEnter the due date in dd mm yyyy format: ")
        is_date_valid, task_due_date = date_validation(task_due_date)

        if is_date_valid :
            break

      
    # Updates current_date and task_completed varaibles
    current_date = datetime.today().strftime("%d %b %Y")
    task_completed = "No"

    # Adds a new task into tasks.txt
    with open("tasks.txt", "a") as task_file :
        task_file.write(f"{task_username}, {task_title}, {task_desc}, {current_date}, {task_due_date}, {task_completed}\n")
        print("\nTask has been added successfully!\n")


#==========================================================
# Function to view all tasks
#==========================================================
def view_all():

    # Open the tasks.txt file to read the contents and displays it in the required format
    with open("tasks.txt", "r", encoding="utf-8" ) as task_file :
        for entry in [line.split(", ") for line in task_file] :

            # Replacing the carrot entry with commas in title and title description
            entry[1] = entry[1].replace("^", ",")
            entry[2] = entry[2].replace("^", ",")
            print("____________________________________________________________\n")
            print(f'''{'Task:':<22} {entry[1]:<}\n{'Assigned to:':<22} {entry[0]:<}\
            \n{'Date assigned:':<22} {entry[3]:<}\n{'Due date:':<22} {entry[4]:<}\
            \n{'Task complete?':<22} {entry[5].rstrip():<}\n{'Task description:':<22}\n {entry[2]:<}''')
            print("____________________________________________________________\n")


#==========================================================
# Function to display my task
#==========================================================
def display_my_task(username):

    # Initilises the variables
    task_exist = False
    user_task_count = 1
    completed_tasks = 0
    # Varible for tracking the actual user's task entry position
    pos_file = 0
    # Dictionary to map the task id to actual task entry position
    task_id_map = {}

    # Open the tasks.txt file to read the contents 
    with open("tasks.txt", "r", encoding="utf-8" ) as task_file :
        for entry in [line.split(", ") for line in task_file] :
            
            # Checks for the logged in user and displays only their content in the required format
            if username == entry[0] :

                task_exist = True
                # Updates the task dictionary
                task_id_map[user_task_count] = pos_file

                # Replacing the carrot entry with commas in title and title description
                entry[1] = entry[1].replace("^", ",")
                entry[2] = entry[2].replace("^", ",")
                print("____________________________________________________________\n")
                print(f'''{'Task id:':<22} {user_task_count}\n{'Task:':<22} {entry[1]:<}\n{'Assigned to:':<22} {entry[0]:<}\
                \n{'Date assigned:':<22} {entry[3]:<}\n{'Due date:':<22} {entry[4]:<}\
                \n{'Task complete?':<22} {entry[5].rstrip():<}\n{'Task description:':<22}\n {entry[2]:<}''')
                print("____________________________________________________________\n")

                # Counts the number of completed tasks for the user
                if entry[5].rstrip() == "Yes":
                    completed_tasks += 1
                
                #  Increments the total task count for the user 
                user_task_count += 1
            
            # Increments the postion of the user task entry in the file
            pos_file += 1


    # Checks if there are no tasks for the logged in user
    if not task_exist :
        print("\nNo tasks assigned to you!\n") 
        return None

    # Checks if all the tasks by user has been completed
    elif completed_tasks + 1 == user_task_count:
        print("\nYou have completed all tasks!\n")
        return None

    else:
        return task_id_map

#==========================================================
# Function to view and edit my task
#==========================================================
def view_mine(username):

    show_my_task = True

    # Gets the user entry for task editing until he gives a valid input
    while True:
        
        # Displays tasks only when needed
        if show_my_task:
            task_id_map = display_my_task(username)

        # Returns to main menu when user does not have any task
        if task_id_map == None:
            return

        # Asks the user to choose the task for editing
        user_entry_task = input("Enter the task id of the task you would like to work with (enter -1 to return to main menu): ")
        
        # Returns to main menu
        if user_entry_task == "-1":
            return

        # checks for the invalid entry
        if not user_entry_task.isdigit():
            print("\nInvalid entry\n")
            show_my_task = False
        
        # Checks for task id in the task_id_map dictionary
        elif int(user_entry_task) in task_id_map.keys():

            show_my_task = True
            user_entry_task = int(user_entry_task)

            # Open the file to read and edit accordingly
            with open("tasks.txt", "r+", encoding="utf-8" ) as task_file :

                entire_file = task_file.readlines()
                entry = entire_file[task_id_map[user_entry_task]].split(", ")

                # Checks if the selected task is not completed
                if entry[5].rstrip() == "No":
                    while True:
                        vm_choice = input('''\nSelect one of the following Options below:\
                                    \nm - mark the task as complete\
                                    \ned - edit the task\
                                    \n-1 - main menu\n''').lower()
                        
                        # Checks for main menu return
                        if vm_choice == "-1":
                            return

                        # Changes the task completion entry for the user
                        elif vm_choice == 'm':
                            # Changes the task to completed
                            entry[5] = "Yes\n"

                            # Updates that particular task entry
                            entire_file[task_id_map[user_entry_task]] = ", ".join(entry)

                            # Erases the content of the file
                            task_file.truncate(0)

                            # Starts from the beginning of the file
                            task_file.seek(0)
                            task_file.writelines(entire_file)
                            print(f"\nThe task has been updated!\n")
                            break
                        
                        # Asks the user for further options if they have selected to edit the task   
                        elif vm_choice == 'ed':
                            while True:
                                edit_choice = input('''\nSelect what you want to edit:\
                                                    \nu - username of the person to whom the task is assigned\
                                                    \nd - due date of the task can be edited\
                                                    \n-1 - exit to previous menu\n''').lower()
                                
                                # Checks for previous menu return
                                if edit_choice == "-1":
                                    break
                                
                                elif edit_choice == "u":
                                    # Asks for a username until a registered username is given 
                                    while True:
                                        task_username = input("\nEnter the user you want to assign the task to: ")
                                        if user_validation(task_username):
                                            if entry[0] != task_username:
                                                break
                                            else:
                                                print("The new username is same as the old one!")
                                        else:
                                            print("Invalid username. Username does not exist!")

                                    # Changes the username for the task selected
                                    entry[0] = task_username

                                    # Updates that particular task entry
                                    entire_file[task_id_map[user_entry_task]] = ", ".join(entry)

                                    # Erases the content of the file
                                    task_file.truncate(0)

                                    # Starts from the beginning of the file
                                    task_file.seek(0)
                                    task_file.writelines(entire_file)
                                    print(f"\nThe task has been updated!\n")
                                    break

                                elif edit_choice == "d":
                                    # Asks for the date until a valid one is given
                                    while True:
                                        task_due_date = input("\nEnter the due date in dd mm yyyy format: ")
                                        is_date_valid, task_due_date = date_validation(task_due_date)
                                        if is_date_valid:
                                            break
                                    
                                    # Changes the due date for the entry
                                    entry[4] = task_due_date

                                    # Updates that particular task entry
                                    entire_file[task_id_map[user_entry_task]] = ", ".join(entry)

                                    # Erases the content of the file
                                    task_file.truncate(0)

                                    # Starts from the beginning of the file
                                    task_file.seek(0)
                                    task_file.writelines(entire_file)
                                    print(f"\nThe task has been updated!\n")
                                    break

                                else:
                                    print("\nInvalid entry\n")
                                                                
                            # Checks to break after editing the task
                            if edit_choice != "-1" :
                                break
                        else:
                            print("\nInvalid entry\n")

                else:
                    print("The task has already been completed!\n")
                    show_my_task = False

        else:
            print("\nWrong Task id!\n")
            show_my_task = False


#==========================================================
# Function for login validation
#==========================================================     
def login_validation(username, password):

    # Initialises the variables
    username_check = False
    password_check = False

    # Opens the file to check for username and password validation
    with open("user.txt", "r", encoding="utf-8") as user_file :
        for entry in [line.split(", ") for line in user_file] :

            # Checks the username entry in user.txt
            if username == entry[0] :
                username_check = True
                # Checks if the password matches for the user
                if password == entry[1].strip() :
                    password_check = True
                break    

    # Returns True or False based on the match              
    if username_check and password_check:
        return True
    elif not username_check :
        print("Username not Found")
        return False
    else:
        print("Invalid password")
        return False


#==========================================================
# Function to produce report for the tasks
#==========================================================
def tasks_report(admin):
    # Does the operation only for admin user
    if admin:

        # Initialises the variables
        total_tasks = 0
        completed_tasks = 0
        incomplete_tasks = 0
        overdue_tasks = 0
        task_report = {}

        # Opens the tasks.txt file for reading
        with open("tasks.txt", "r", encoding= "utf-8" ) as task_file :
            # Increments the total_tasks for each entry
            for entry in [line.split(", ") for line in task_file] :
                total_tasks += 1
                
                # Increments the completed_tasks or incomplete tasks based on the entry
                if entry[5].strip() == "Yes" :
                    completed_tasks += 1
                elif entry[5].strip() == "No" :
                    incomplete_tasks += 1

                    # Checks the due date for the incomplete task and increments the overdue_tasks
                    if datetime.strptime(entry[4].strip(),"%d %b %Y").date() < datetime.today().date() :
                        overdue_tasks += 1
        
        # Handles divide by zero
        if total_tasks == 0:
            percentage_incomplete_tasks = 0
            percentage_overdue_tasks = 0
        else:
            percentage_incomplete_tasks = incomplete_tasks / total_tasks * 100
            percentage_overdue_tasks = overdue_tasks / total_tasks * 100

        # Updates the task_report dictionary with the value calculated
        task_report["Total tasks"] = total_tasks
        task_report["Completed tasks"]= completed_tasks
        task_report["Incomplete tasks"] = incomplete_tasks
        task_report["Overdue tasks"] = overdue_tasks
        task_report["Percentage of incomplete tasks"] = round(percentage_incomplete_tasks, 2)
        task_report["Percentage of overdue tasks"] = round(percentage_overdue_tasks, 2)

        # Calculates the length of the longest label and adds 5 spaces for formatting
        format_length = len(max(task_report.keys(), key=len)) + 5

        # Writes the task_report dictionary values into the file
        with open("task_overview.txt", "w") as task_overview_file :
            for description, value in task_report.items() :
                
                # Checks the description for adding % symbol
                if "Percentage" in description :
                    task_overview_file.write(f"{description} {f':':>{format_length-len(description)}}{value}%\n")
                else:
                    task_overview_file.write(f"{description} {f':':>{format_length-len(description)}}{value}\n")


#==========================================================
# Function to count total users
#==========================================================
def total_users():
    
    user_count = 0
    # Opens the user.txt and increments the user_count accordingly
    with open("user.txt", "r", encoding= "utf-8") as user_file :
        user_count = len([line for line in user_file]) 
            
    return user_count
    

#==========================================================
# Function to produce user reports
#==========================================================
def users_report(admin):

    # Checks for admin user
    if admin:

        # Calls total_users for user_count and sets the summary value for initial summary lines
        user_count = total_users()
        summary = False

        # Reads each entry in user.txt
        with open("user.txt", "r", encoding= "utf-8") as user_file :
            for user_entry in [line.split(", ") for line in user_file] :

                # Initialises the variables for each user
                user_report = {}
                user_total_tasks = 0
                total_tasks = 0
                user_completed_tasks = 0
                user_incomplete_tasks = 0
                user_overdue_tasks = 0
                
                # Reads each entry in tasks.txt
                with open("tasks.txt", "r", encoding= "utf-8" ) as task_file :
                    for task_entry in [line.split(", ") for line in task_file] :

                        # Increments the total_tasks for each entry
                        total_tasks += 1

                        # Increments the user_total_tasks for any match with username
                        if user_entry[0] == task_entry[0]:
                            user_total_tasks += 1

                            # Increments the completed_tasks or incomplete tasks based on the entry
                            if task_entry[5].strip() == "Yes" :
                                user_completed_tasks += 1
                            elif task_entry[5].strip() == "No" :
                                user_incomplete_tasks += 1

                                # Checks the due date for the incomplete task and increments the overdue_tasks
                                if datetime.strptime(task_entry[4].strip(),"%d %b %Y").date() < datetime.today().date() :
                                    user_overdue_tasks += 1
                

                # Handles divide by zero for percentage_user_total_tasks
                if total_tasks == 0:
                    percentage_user_total_tasks = 0
                else:
                    percentage_user_total_tasks = user_total_tasks / total_tasks * 100
                
                # Handles divide by zero for other percentages
                if user_total_tasks == 0:
                    percentage_user_completed_tasks = 0
                    percentage_user_incomplete_tasks = 0
                    percentage_user_overdue_tasks = 0
                else:
                    percentage_user_completed_tasks = user_completed_tasks / user_total_tasks * 100
                    percentage_user_incomplete_tasks = user_incomplete_tasks / user_total_tasks * 100
                    percentage_user_overdue_tasks = user_overdue_tasks / user_total_tasks * 100

                # Updates the user_report for other entries
                user_report["Total tasks"] = user_total_tasks
                user_report[f"Percentage of {user_entry[0]}'s total tasks"] = round(percentage_user_total_tasks, 2)
                user_report[f"Percentage of {user_entry[0]}'s completed tasks"] = round(percentage_user_completed_tasks, 2)
                user_report[f"Percentage of {user_entry[0]}'s incomplete tasks"] = round(percentage_user_incomplete_tasks, 2)
                user_report[f"Percentage of {user_entry[0]}'s overdue tasks"] = round(percentage_user_overdue_tasks, 2)

                # Calculates the length of the longest label and adds 5 spaces for formatting
                format_length = len(max(user_report.keys(), key=len)) + 5

                # Opens user_overview in append mode for each user 
                with open("user_overview.txt", "a") as task_overview_file :
                    
                    # Checks for summary and writes the initial summary accordingly
                    if not summary :
                        task_overview_file.truncate(0)
                        task_overview_file.write("==========================================================\n")
                        task_overview_file.write(f"Total number of users     :{user_count}\n")
                        task_overview_file.write(f"Total number of tasks     :{total_tasks}\n")
                        task_overview_file.write("==========================================================\n")
                        summary = True

                    # Writes the label for each report
                    task_overview_file.write(f"\n{user_entry[0]}'s report\n")
                    task_overview_file.write("----------------------------------------------------------\n")

                    # Writes the user_report dictionary values into the file    
                    for description, value in user_report.items() :
                        
                        # Checks the description for adding % symbol 
                        if "Percentage" in description :
                            task_overview_file.write(f"{description} {f':':>{format_length-len(description)}}{value}%\n")
                        else:
                            task_overview_file.write(f"{description} {f':':>{format_length-len(description)}}{value}\n")

                    task_overview_file.write("----------------------------------------------------------\n")


#==========================================================
# Function to generate the tasks' and users' reports
#==========================================================
def  generate_report(admin):

    tasks_report(admin)
    users_report(admin)


#==========================================================
# Function to display statistics
#==========================================================
def display_statistics(admin):

    # Checks for admin user
    if admin:

        # Calls the tasks_report to generate the latest report
        tasks_report(admin)
        
        print("==========================================================")
        print("                       Tasks' Report")
        print("==========================================================")
        
        # Diplays the content of the task_overview.txt
        with open("task_overview.txt", "r", encoding= "utf-8") as task_file :
            for line in task_file:
                print(line.rstrip())

        # Calls the users_report to generate the latest report
        users_report(admin)

        print("==========================================================")
        print("                       Users' Report")
        print("==========================================================")

        # Diplays the content of the user_overview.txt
        with open("user_overview.txt", "r", encoding= "utf-8") as user_file :
            for line in user_file:
                print(line.rstrip())


#==========================================================
# Main
#==========================================================
# Initialises admin to False
admin = False

# Asks the user for username and password until they enter the right credentials
while True:

    username = input("\nEnter your Username: ")
    password = input("Enter your Password: ")

    if login_validation(username, password):
        break

# Presents the menu to the user until e(exit) is entered
while True:          
    
    print("\nPlease select one of the following options")
    choices = ["r - register user", "a - add task","va - view all tasks",
                "vm - view my tasks","gr - generate reports",
                "ds - display statistics","e - exit"]

    # Updates the menu option according to the user and 
    # makes sure that the user input is converted to lower case.
    if username == "admin" :
        admin = True
        for i in range(6):
            print(choices[i])
        
    else:
        for i in range(1,4):
            print(choices[i])
    
    menu = input(f"{choices[6]}\n: ").lower()


    # For registering a new user
    if menu == 'r':

        # Checks if the user is admin to let only admin user register new users
        if admin :
            reg_user(admin)
        else:
            print("You have made a wrong choice, Please Try again\n")

    # For adding a task for a user
    elif menu == 'a':
        add_task()

    # For displaying all the tasks
    elif menu == 'va':
        view_all()

    # For displaying tasks for the logged in user
    elif menu == 'vm':
        view_mine(username)

    elif menu == 'gr':
        # Checks if the user is admin to let only admin user to generate the report
        if admin :
            generate_report(admin)
        else:
            print("You have made a wrong choice, Please Try again\n")

    # For displaying statistics - total user and total tasks for all user
    elif menu == 'ds' :

        # Checks if the user is admin to let only admin user to view the statistics
        if admin :
            display_statistics(admin)
        else:
            print("You have made a wrong choice, Please Try again\n")

    # For exiting the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # For invalid choices
    else:
        print("You have made a wrong choice, Please Try again\n")