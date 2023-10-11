# Capstone Project II- Lists, Functions and String handling

# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
import textwrap
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# Define a function to register a user
def reg_user():
    # Request a user to input a username
    new_username = input("Please enter a username: ")
    while new_username in username_password:
        new_username = show_menu("\nUsername already exists. Try again with different username to proceed ahead.")

    # if user input is empty, return to main menu
    if new_username.strip() in [""]:
        return

    # Request a user to input a password
    new_password = input("Please enter a password: ")

    # Request a user for password confirmation.
    confirm_password = input("Please re-enter a password: ")

    # Validate a password and confirmed password
    if new_password == confirm_password:
        # If the password matched, add a user to the user.txt file
        print("New user added successfully!")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            # Write the users and their passwords in the output file
            out_file.write("\n".join([f"{u};{username_password[u]}" for u in username_password]))

    # Display the relevant message for invalidation of password
    else:
        print("Password did not match. The user could not be registered.")


# define a function to show relevant message ask for another input
def show_menu(message):
    print(message)
    return input("Please enter a different username: ")


# Define a function to add task/s
def add_task():
    """Allow a user to add a new task to task.txt file
    Prompt a user for the following:
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and
     - the due date of the task."""
    task_username = edit_username()
    if task_username == "b":
        return

    task_title = input("Title of Task: ")
    while task_title.strip() == "":
        task_title = show_menu("Task title can't be empty. Please enter a valid task title")

    if task_title == "b":
        return

    task_description = input("Description of Task: ")
    while task_description.strip() == "":
        task_description = show_menu("Task title can't be empty. Please enter a valid task title")

    if task_description == "b":
        return

    due_date_time = edit_due_date()

    # Get the current date
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    write_task_file(task_list)
    print("Task successfully added.")


# Define a function to view all tasks
def view_all():
    """
    Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    for index, t in enumerate(task_list):
        disp_str = f"Task {idx}: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# Define the function to view specific user's task and add few option/s
def view_mine():
    """
    Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """
    for idx, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task {idx}: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    while True:
        # Asking a user to select a task
        try:
            task_select = int(input("""Type the number of the task to select it.
            Or type '-1' to go back to the main menu : \n"""))

        except ValueError:
            task_select = -1
            print("Invalid option selected. Please use the format specified")

        if task_select == -1:
            return

        elif task_select > len(task_list) - 1:
            print("There is no task with this identifier.\n")

        else:
            # Asking a user to choose an option, edit is displayed only if the selected task is not completed
            task_option = input(f"""Select one of the following Options below:
            c - Mark the task as completed
            {(not task_list[task_select]["completed"]) * "e - Edit the task"}\n""").lower()
            if task_option == "c":
                # Change the task status to True
                task_list[task_select]["completed"] = True
                print(f"Task number {task_select} has been marked as completed\n")
            elif task_option == "e":
                # Asking the user to change the username and/or due date
                task_username = edit_username()
                if task_username == "b":
                    break
                else:
                    task_list[task_select]["username"] = task_username
                task_list[task_select]["due_date"] = edit_due_date()
                print("Task successfully edited.")
                break
            else:
                print("You have made a wrong choice, Please Try again!\n")

            # Adding the changes to the task file
            write_task_file(task_list)
            return


# Define a function to calculate and return the percentage
def percentage(parts, whole):
    return f'{round((parts / whole * 100), 2)}%'


# Define a function to return edited due date if the user chooses to modify
def edit_due_date():
    while True:
        try:
            task_due_date = input("Due date of task(YYYY-MM-DD): ")
            due_date = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please enter a date with specified format.")
    return due_date


# Define a function to edit the username which will be accessed within vm and return modified username
def edit_username():
    username = input("Enter the username of the person assigned to task: ")
    if username in ["b", ""]:
        return "b"
    elif username not in username_password:
        print("The username does not exist. Select one of the options below:\nb - Go back to Main Menu")
        # Loop through the function until we get valid input
        return edit_username()
    else:
        return username


# Define a function to write the task file
def write_task_file(tasks):
    with open("tasks.txt", "w") as file:
        task_list_to_write = []
        for t in tasks:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        file.write("\n".join(task_list_to_write))


# Define a function to generate reports
def generate_report(tasks, users):
    # Get the current date
    curr_date = datetime.today()
    # Create a dictionary to present report
    report = {"total_tasks": len(tasks),
              "total_users": len(users),
              "total_completed": 0,
              "overdue": 0,
              "users": {}
              }

    for task in tasks:
        # Checking if username is in the users dictionary
        if task["username"] not in report["users"]:
            # Create a dictionary for that user inside
            report["users"][task["username"]] = {"nr_of_tasks": 0, "completed": 0, "overdue": 0}

        # Increase the number of task assigned to a specific user
        report["users"][task["username"]]["nr_of_tasks"] += 1

        # Check if task is completed and add it to the report dictionary
        if task["completed"]:
            report["total_completed"] += 1
            report["users"][task["username"]]["completed"] += 1

        # Check if task is not completed and overdue and add it to the report dictionary
        if task["due_date"] < curr_date and task["completed"] is not True:
            report["overdue"] += 1
            report["users"][task["username"]]["overdue"] += 1

    # Go through all the users to add the ones that don't have tasks assigned
    for user in user_data:
        user = user.split(";")[0]
        if user not in report["users"]:
            report["users"][user] = {"nr_of_tasks": 0, "completed": 0, "overdue": 0}

    # Write the final report the output file
    with open("task_overview.txt", "w") as task_overview_file, open("user_overview.txt", "w") as user_overview_file:
        task_overview_file.write(f"""
    --------------------------------------------------
    Task Overview Report
    Date : {curr_date.strftime('%Y-%m-%d')}
    --------------------------------------------------
    Total number of tasks:                   {report["total_tasks"]}

    Total number of completed tasks:         {report["total_completed"]}

    Total number of uncompleted tasks:       {report["total_tasks"] - report["total_completed"]}

    Total number of tasks overdue:           {report["overdue"]}

    Percentage of tasks that are incomplete: {round((report["total_tasks"] - report["total_completed"]) /
                                                    report["total_tasks"] * 100, 2)}% 

    Percentage of tasks that are overdue:    {round(report["overdue"] / report["total_tasks"] * 100, 2)}%
    --------------------------------------------------""")

        user_overview_file.write(f"""
    -----------------------------------------------------------------------------------------------------
    User Overview Report
    Date : {curr_date.strftime('%Y-%m-%d')}
    -----------------------------------------------------------------------------------------------------
    Total number of user :                   {report["total_users"]}

    Total number of tasks :                  {report["total_tasks"]}
    -----------------------------------------------------------------------------------------------------""")
        for user in report["users"]:
            try:
                user_overview_file.write(f"""
    USERNAME : {user}
    Total number of tasks assigned to the user :                                                   {report["users"][user]["nr_of_tasks"]}

    Percentage of the total number of tasks that have been assigned to the user :                  {percentage(report["users"][user]["nr_of_tasks"], report["total_tasks"])}

    Percentage of the tasks assigned to the user that have completed :                             {percentage(report["users"][user]["completed"], report["users"][user]["nr_of_tasks"])}

    Percentage of the tasks assigned to the user that must still be completed :                    {percentage((report["users"][user]["nr_of_tasks"] - report["users"][user]["completed"]), report["users"][user]["nr_of_tasks"])}

    Percentage of the tasks assigned to the user that have not yet been completed and are overdue: {percentage(report["users"][user]["overdue"], report["users"][user]["nr_of_tasks"])}
    ------------------------------------------------------------------------------------------------------""")
            except ZeroDivisionError:
                user_overview_file.write(f"""
    USERNAME : {user}
    Total number of tasks assigned to the user :                                                   0
    Percentage of the total number of tasks that have been assigned to the user :                  0%
    Percentage of the tasks assigned to the user that have completed :                             0%
    Percentage of the tasks assigned to the user that must still be completed :                    0%
    Percentage of the tasks assigned to the user that have not yet been completed and are overdue: 0%
    ------------------------------------------------------------------------------------------------------""")


# Define a function to display user overview/task overview reports on the console
def display_statistics():
    with open("task_overview.txt", "r") as task_overview_file, open("user_overview.txt", "r") as user_overview_file:
        print("\t--------------------------------------------------")
        for line, content in enumerate(task_overview_file):
            if line not in [0, 1, 3]:
                print(content[:-1])
        for line, content in enumerate(user_overview_file):
            if line not in [0, 1, 2, 3, 5]:
                print(content[:-1])


# Create text file for tasks if it does not exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split each component by semicolon and manually add them together
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input(f'''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
{"""gr - Generate reports
ds - Display statistics
e - Exit""" if (curr_user == "admin") else "e - Exit"}
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        generate_report(task_list, user_data)
        print("The reports have been generated successfully")

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''

        # Check if the reports have been generated, if not generate them
        if not (os.path.exists("task_overview.txt") or os.path.exists("user_overview.txt")):
            generate_report(task_list, user_data)

        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again!")
