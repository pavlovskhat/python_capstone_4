
# ****** RESUBMISSION NOTES ******
# Registration issue was due to having the input copied into two statements.
# Reports function still had the dictionaries as 'print' command for error checking
# one of these dictionaries became obsolete thus the error.
# Finally the looping structure in the editing function was incorrect, just moved
# it around and it works fine.

# Thanks again for the resubmit, I chalk this up to frustration and having copied and pasted
# my code in and out of the project for isolated testing, learnt a lot in the process on
# how not to do things in future with something bigger like this program!

# ******************************************************************************************

# Capstone project IV

# This is a program that helps a small business assign tasks to its team members.

# ****** DEFINING PROGRAM FUNCTIONS: ******

# Function to generate reports from the program tasks and users file.
# Reports are written to tasks overview and users overview files.
def gen_report():

    # ****** Creating reporting data for task overview file. ******

    # Setting variable start conditions that are used within function.
    task_pend = 0
    task_done = 0
    task_late = 0
    all_task_list = []

    # Importing datetime module in order to compare dates.
    # Did more research on the datetime module and comparing dates from here:
    # https://docs.python.org/3/library/datetime.html
    from datetime import date
    today = date.today()  # Setting today to a variable.

    user_tasks = call_tasks()  # Calling tasks dictionary with pre-defined function.
    all_tasks = user_tasks.values()  # Extracting user tasks values dictionary values to list.

    task_total = len(user_tasks)  # Counting total tasks to use in calculations.

    # Each line of all tasks list is added as a separate item to all_task_list.
    for line in all_tasks:
        all_task_list.append(line)

    # Looping through the all_task_list and adding identifiers to each item.
    for line in all_task_list:
        task_user, task, task_desc, task_start, task_end, task_status = line.split(", ")

        # The due date identifier is formatted to date type.
        task_end = date.fromisoformat(task_end)

        # Adds a counter if task is identified as either incomplete or complete.
        if task_status == "No\n":
            task_pend += 1
        elif task_status == "Yes\n":
            task_done += 1

        # Adds a counter if task is incomplete and overdue based on date comparison with today's date.
        # If task is complete there is no overdue counter required.
        if today > task_end and task_status == "No\n":
            task_late += 1

    # The percentage of tasks that are incomplete and tasks that are overdue to calculated using counters.
    task_pend_pct = (task_pend / task_total) * 100
    task_late_pct = (task_late / task_total) * 100

    # Creating variable to store the report data into a readable format.
    task_report_data = (f"""Task report generated on {today}

Total tasks generated:\t\t{task_number}
Total tasks completed:\t\t{task_done}
Total tasks uncompleted:\t{task_pend}
Total tasks overdue:\t\t{task_late}
Percentage of tasks incomplete:\t{task_pend_pct}%
Percentage of tasks overdue:\t{task_late_pct}%""")

    # Writing the data to file.
    with open("task_overview.txt", "w") as file:
        file.write(task_report_data)

    # ****** Creating data for user overview file. ******

    # Creating variable for this part of the function.
    user_data = call_users()  # Calling list of users using pre-defined function.
    user_total = len(user_data)  # Calculating total number of users to be used in report.

    with open("tasks.txt", "r") as file:  # Reading data from tasks file.
        file_data = file.readlines()

    # Modifying the tasks data to individual items in a new list by joining and then splitting.
    string_data = ", ".join(file_data)
    string_data = string_data.split(", ")

    # Setting up all the required dictionaries as blanks.
    task_dict = {}  # Total task that each user has.
    task_prc_dict = {}  # Percentage of tasks assigned to each user.
    task_done_dict = {}  # Number of tasks done per user.
    task_done_prc_dict = {}  # Percentage of tasks completed per user.
    task_pend_dict = {}  # Number of tasks incomplete per user.
    task_pend_prc_dict = {}  # Percentage of tasks incomplete per user.
    task_late_dict = {}  # Number of tasks overdue per user.
    task_late_prc_dict = {}  # Percentage of tasks overdue and incomplete per user.

    # Creating the first part of the report data as variable user_data.
    user_data = (f"""User report generated on {today}

Total number of user:\t{user_total}
Total  tasks generated:\t{task_total}

Statistics per user:

""")

    # Writing the first part of the data to file, this entry will overwrite.
    with open("user_overview.txt", "w") as file:
        file.write(user_data)

    # Running a loop over file_data and adding identifiers to each item.
    for line in file_data:

        # Creating start point for all calculation counters.
        total_user_task = 0
        task_done_count = 0
        task_pend_count = 0
        task_late_count = 0

        # Setting up the item identifiers.
        task_user, task, task_desc, task_start, task_end, task_status = line.split(", ")

        # Setting special parameters to some of the identifiers.
        user_check = task_user  # Setting this identified iteration as alternate identifier for nested loop.
        status_check = task_status  # Setting this identified iteration as alternate identifier for nested loop.
        # Setting this identified iteration as alternate identifier for nested loop.
        # Also setting format to date type for date comparisons.
        date_check = date.fromisoformat(task_end)

        # Nested loop to check of many iterations of user_check is found and counted.
        for item in string_data:
            if item == user_check:
                total_user_task += 1

                # Calculations are made using counters and dictionaries are updated with user_check as key (username).
                task_dict.update({user_check: total_user_task})
                task_prc = (task_dict[user_check] / task_total) * 100
                task_prc_dict.update({user_check: task_prc})

        # Adding to dictionary based on if task is completed.
        if status_check == "Yes\n":
            task_done_count += 1
            task_done_dict.update({user_check: task_done_count})

        # Adding to dictionary based on if task is incomplete.
        if status_check == "No\n":
            task_pend_count += 1
            task_pend_dict.update({user_check: task_pend_count})

        # Adding to dictionary based on if task is overdue.
        if status_check == "No\n" and today > date_check:
            task_late_count += 1
            task_late_dict.update({user_check: task_late_count})

            # Calculating overdue task percentage and updating relevant dictionary.
            task_late_prc = (task_late_dict[user_check] / task_pend_dict[user_check]) * 100
            task_late_prc_dict.update({user_check: task_late_prc})

        # If not overdue dictionaries are updated to zero for instance.
        else:
            task_late_dict.update({user_check: 0})
            task_late_prc_dict.update({user_check: 0})

        # Had to find how to iterate through a dictionary from here:
        # https://realpython.com/iterate-through-dictionary-python/
        # Looping through task complete dictionary.
        for key in task_done_dict:

            # Calculating percentage completed from all complete if completed tasks is more than '0'.
            # Cannot divide by zero!
            if user_check in task_done_dict and task_done_dict[user_check] > 0:
                task_done_prc = (task_done_dict[user_check] / task_dict[user_check]) * 100
                task_done_prc_dict.update({user_check: task_done_prc})

            # Otherwise percentage is set to 0.
            else:
                task_done_prc_dict.update({user_check: 0})

            # Calculating percentage incomplete from all incomplete if incomplete tasks is more than '0'.
            # Cannot divide by zero!
            if user_check in task_pend_dict and task_pend_dict[user_check] > 0:
                task_pend_prc = (task_pend_dict[user_check] / task_dict[user_check]) * 100
                task_pend_prc_dict.update({user_check: task_pend_prc})

            # Otherwise percentage is set to 0.
            else:
                task_pend_prc_dict.update({user_check: 0})

            # Each instance of the above calculations will populate the below data string.
            # Data string is formatted for easy reading.
            user_specific_data = (f"""{user_check}
Total tasks assigned:\t\t\t{task_dict[user_check]}
Percentage of tasks assigned:\t\t{task_prc_dict[user_check]}%
Percentage of tasks completed:\t\t{task_done_prc_dict[user_check]}%
Percentage of tasks uncompleted:\t{task_pend_prc_dict[user_check]}%
Percentage of tasks overdue:\t\t{task_late_prc_dict[user_check]}%

""")
            # Each instance of the data string is written to user_overview file.
            # Each instance will append and not overwrite.
            with open("user_overview.txt", "a") as file:
                file.write(user_specific_data)


# Function to edit the data within a specific task string.
def edit_task(x):

    # Setting variables to be used within the function.
    edit_choice = ""  # Setting edit_choice to start at blank.
    my_task_dict = {}  # Blank dictionary.
    my_task_list = []  # Blank list.
    user_tasks = call_tasks()  # Calling tasks dictionary with pre-defined function.
    my_task = user_tasks[task_choice]  # Isolating the specific task using user input as dictionary key.
    my_task_list.append(my_task)  # Moving the identified task to the blank list.

    # Loop to build the specific task dictionary.
    for line in my_task_list:

        # Running loop over task list, splitting it into individual items and adding identifying markers to each.
        task_user, task, task_desc, task_start, task_end, task_status = line.split(", ")

        # Using marker to add each item into the blank dictionary with defined keys.
        my_task_dict["User"] = task_user
        my_task_dict["Task"] = task
        my_task_dict["Description"] = task_desc
        my_task_dict["Start Date"] = task_start
        my_task_dict["Due Date"] = task_end
        my_task_dict["Task Status"] = task_status

    # If user input is '1' a specific action is taken by the function.
    if x == 1:

        # Finding and changing the task status item from 'no' to 'yes'.
        my_task_dict["Task Status"] = "Yes"

        # With status value modified, dictionary values are extracted to list.
        # Values are then joined to string, new line is added for file formatting.
        my_task_values = my_task_dict.values()
        my_task_values = ", ".join(my_task_values)
        my_task_values = my_task_values + "\n"

        # The updated task is then updated into the original user task dictionary.
        # It will overwrite the original entry with the specific number key.
        user_tasks.update({task_choice: my_task_values})

    # If user input is '2' another two options are given to user by this function.
    # This option will only pass if the task status item is 'No' ie: task is still incomplete.
    elif x == 2 and my_task_dict["Task Status"] == "No\n":

        # Additional input choice from user.
        edit_choice = int(input("""
Which information would you like to edit?
1 - User assigned to task
2 - The task due date
Your choice: """))

    # Function will update assigned user if '1'.
    if edit_choice == 1 and my_task_dict["Task Status"] == "No\n":

        new_user = input("\nEnter new assigned user: ")  # New user is entered here.

        # Task user is found, modified and updated in the same way as the status previously.
        my_task_dict["User"] = new_user
        my_task_values = my_task_dict.values()
        my_task_values = ", ".join(my_task_values)
        user_tasks.update({task_choice: my_task_values})

    # Function will update due date if '2'.
    elif edit_choice == 2 and my_task_dict["Task Status"] == "No\n":

        # New due date entered here, specific format to be followed for reporting feature.
        new_date = input("\nEnter new due date in format yyyy-mm-dd: ")

        # Due date is found, modified and updated same as before to original task dictionary.
        my_task_dict["Due Date"] = new_date
        my_task_values = my_task_dict.values()
        my_task_values = ", ".join(my_task_values)
        user_tasks.update({task_choice: my_task_values})

    elif my_task_dict["Task Status"] == "Yes\n":
        print("\nThis task is complete and can no longer be edited.")

    # Extracting values from updated user task dictionary to list.
    user_tasks_values = user_tasks.values()

    # Overwriting updated tasks data to tasks file.
    with open("tasks.txt", "w") as file:
        for line in user_tasks_values:
            file.write(line)


# Function to read data from 'tasks.txt' and return it as an enumerated dictionary.
def call_tasks():
    with open("tasks.txt", "r") as file:
        file_data = file.readlines()

    # Modifications to data, enumerating and creating a dictionary.
    # Researched this code from the following page:
    # https://www.tutorialspoint.com/How-to-create-Python-dictionary-by-enumerate-function
    file_data_enum = list(enumerate(file_data, 1))
    file_dict = dict((a, b) for a, b in file_data_enum)

    return file_dict  # Returning data in custom enumerated format.


# Function to add all registered users to a list.
def call_users():
    user_list = []  # Creating empty list to store user names.

    with open("user.txt", "r") as file:  # Opening and reading 'user.txt' file.
        file_data = file.readlines()

    for line in file_data:  # Running loop to append user names to pre-created list.
        user, password = line.split(", ")
        user_list.append(user)

    return user_list  # Users can be returned in custom created list without passwords.


# New user registration function.
def reg_user():

    users = call_users()  # Running 'all_users' function and assigning list return to variable.
    user_reg = False  # Setting username registration while loop start position.
    pass_reg = False  # Setting password registration while loop start position.

    while user_reg is False:  # Username registration while loop.
        new_username = input("\nPlease enter username: ")
        if new_username in users:  # If username already exists error message is output and loop will restart.
            print("\nThis username is already registered, please enter a different username.\n")

        else:  # If username is unique loop will end.
            user_reg = True

    while pass_reg is False:  # Password registration while loop.
        new_password = input("Please enter password: ")
        ver_password = input("Please re-enter password: ")  # Re-enter password for verification.

        if new_password != ver_password:  # If password verification fails loop will restart.
            print("\nYour passwords did not match, please try again.\n")

        else:  # If password verification passes the new username and password is written to the 'user.txt' file.
            with open("user.txt", "a") as user_file:  # Note append mode to not overwrite.
                user_file.write(f"{new_username}, {new_password}\n")
            pass_reg = True  # Password registration loop ends, 'reg_user' function ends.


# Add task function.
def add_task(a, b, c, d):
    # Assigning current date as variable.
    from datetime import date
    today = date.today()

    with open("tasks.txt", "a") as tasks_file:
        # Standard task format start date always today and status always starts at 'No'.
        tasks_file.write(f"\n{a}, {b}, {c}, {today}, {d}, No")  # Opening 'tasks.txt' and writing new task details.


# View all tasks function.
def view_all():
    with open("tasks.txt", "r") as tasks_file:
        tasks_data = tasks_file.readlines()  # Open 'tasks.txt' read it and assign data to variable.

        for line in tasks_data:  # Splitting each task entry category into separate string variable for easy output.
            task_user, task, task_desc, task_start, task_end, task_status = line.split(", ")

            # Output of all task details.
            print(f"""
    User\t\t\t{task_user}
    Title\t\t\t{task}
    Description\t\t{task_desc}
    Start Date\t\t{task_start}
    Due Date\t\t{task_end}
    Completed\t\t{task_status}
""")


# View my tasks function.
def view_mine():

    user_tasks = call_tasks()  # Running function to call the data in 'tasks.txt' file as dictionary.
    user_tasks_items = user_tasks.items()  # Adding all dictionary keys and values into one list.

    # The integer in the list is not allowing me to loop and identify item per line.
    # Found a work around from the following site to format the entire list to string.
    # https://www.geeksforgeeks.org/python-program-to-convert-list-of-integer-to-list-of-string/
    items_string = map(str, user_tasks_items)

    # Identifying each item per line for preferred print output.
    # Modifying items with undesirable characters.
    for line in items_string:
        task_num, task_user, task, task_desc, task_start, task_end, task_status = line.split(", ")
        task_status = task_status.replace("\\n", "")
        task_num = task_num.replace("(", "")
        task_user = task_user.replace("'", "")
        task_status = task_status.replace("')", "")

        if username == task_user:  # Will output only the current users task data.
            print(f"""
{task_num}\tUser\t\t\t{task_user}
\tTitle\t\t\t{task}
\tDescription\t\t{task_desc}
\tStart Date\t\t{task_start}
\tDue Date\t\t{task_end}
\tCompleted\t\t{task_status}
""")


# ****** PROGRAM RUN LOGIC: ******

# This parameter is required for the reporting function in the program.
# Setting to 5 as there were already 5 tasks generated.
task_number = 5

# ****** PROGRAM LOGIN: ******

login = False  # Setting start parameter for login while loop.

# Login while loop input prompt to keep user in function until valid entry is given.
while login is False:
    username = input("\nPlease enter your username: ")
    password = input("Please enter your password: ")

    with open("user.txt", "r") as file:
        valid_user_data = file.readlines()

    # Extracting valid usernames and passwords and storing in new variables.
    for line in valid_user_data:
        valid_user, valid_password = line.split(", ")  # Removing characters that will cause issues and splitting.
        valid_password = valid_password[0:-1]  # Removing the new line that will be written.

        # Checking if details are valid by comparing with existing details.
        if username == valid_user and password == valid_password:
            login = True  # login loop passes and program will continue

    if login is False:  # Error message if after for loop login is still false status.
        print("\nIncorrect username or password, please enter valid username and password.")

# ****** MAIN MENU: ******

while login is True:  # Will continue to run while user is logged in.

    if username == "admin":  # Expanded menu options to admin user only.
        choice = input("""\nPlease select one of the following options:
r\t-\tregister user
a\t-\tadd task
va\t-\tview all tasks
vm\t-\tview my tasks
gr\t-\tgenerate reports
ds\t-\tstatistics
e\t-\texit
Your selection: """)

    else:  # Standard menu options to all other users.
        choice = input("""\nPlease select one of the following options:
a\t-\tadd task
va\t-\tview all tasks
vm\t-\tview my tasks
gr\t-\tgenerate reports
e\t-\texit
Your selection: """)

    # ****** NEW USER REGISTRATION: ******
    if choice == "r":
        reg_user()  # This function will complete this option.

    # ****** ADD NEW TASK: ******
    elif choice == "a":
        # This is a counter that adds everytime a task is generated.
        # This will be used in the reporting feature.
        task_number += 1

        # Inputs to add task details to task file.
        task_user = input("\nWhich user is this task assigned to? ")
        task = input("Enter task title: ")
        task_desc = input("Enter description of task: ")

        # The input format is required for task editing and reporting.
        task_end = input("Enter task due date in format yyyy-mm-dd: ")

        add_task(task_user, task, task_desc, task_end)  # Running function with input parameters.

    # ****** VIEW ALL TASKS: ******
    elif choice == "va":
        view_all()  # This function will complete this option.

    # ****** VIEW AND EDIT USERS TASKS: ******
    elif choice == "vm":

        view_mine()  # Function will run and display only the users task data.
        user_tasks = call_tasks()  # Running function to call the user tasks dictionary.
        user_tasks_keys = user_tasks.keys()  # Adding variable with the enumerated task keys.

        view_task = False  # Setting start parameter for while loop.

        while view_task is False:  # Will continue to run until user inputs valid option.

            task_choice = int(input("\nEnter a task number to edit that task or enter '-1' to return to main menu: "))

            if task_choice == -1:  # This option will navigate user back to main menu.
                view_task = True

            # If a valid task number is chosen user will be able to choose the task edit option for that task.
            elif task_choice in user_tasks_keys:
                edit_choice = int(input("""
What information would you like to update?
1 - Change task status to completed
2 - Edit the task user or due date
Your choice: """))

                edit_task(edit_choice)  # Running function with user edit choice as parameter.

            else:  # Error code in case user selection is invalid.
                print("\nYou have not entered a valid option, please try again.")

    # ****** VIEW PROGRAM STATISTICS ******
    # This option is only available to the admin user.
    elif choice == "ds":

        if username == "admin":  # Verifying user is admin before function loop will start.

            # Reading and staring to variables data from 'tasks' and 'user' files.
            with open("tasks.txt", "r") as task_file:
                task_data = task_file.readlines()

            with open("user.txt", "r") as user_file:
                user_data = user_file.readlines()

            # Calculating total tasks and users and displaying on screen.
            task_total = len(task_data)
            print("\nTotal Users:\t" + str(task_total))

            user_total = len(user_data)
            print("Total Tasks:\t" + str(user_total) + "\n")

            # Require os module for the next block of code.
            # Found more info on this module here:
            # https://pythonexamples.org/python-check-if-path-is-file-or-directory/
            import os

            # Checking if files 'task_overview' and 'user_overview' exist in program directory.
            task_report_path = "C:/Users/jclsm/Dropbox/Chris Smit-96697/Introduction to Programming/Task 25/task_overview.txt"
            is_task_report_file = os.path.isfile(task_report_path)

            user_report_path = "C:/Users/jclsm/Dropbox/Chris Smit-96697/Introduction to Programming/Task 25/user_overview.txt"
            is_user_report_file = os.path.isfile(user_report_path)

            # If they exist data is read from both files and output line by line on screen.
            if is_task_report_file and is_user_report_file is True:
                with open("task_overview.txt", "r") as task_report_file:
                    task_report_data = task_report_file.readlines()

                with open("user_overview.txt", "r") as user_report_file:
                    user_report_data = user_report_file.readlines()

                for line in user_report_data:
                    print(line)

                for line in user_report_data:
                    print(line)

            # If they do not exist the 'gen_report' function is run first to create them.
            # Data is read and displayed on screen after.
            else:
                gen_report()

                with open("task_overview.txt", "r") as task_report_file:
                    task_report_data = task_report_file.readlines()

                with open("user_overview.txt", "r") as user_report_file:
                    user_report_data = user_report_file.readlines()

                for line in user_report_data:
                    print(line)

                for line in user_report_data:
                    print(line)

        else:  # Error message output if user is not admin.
            print("\nOnly the admin has access to this function.")

    # ****** GENERATE REPORTS: ******
    elif choice == "gr":

        # This function will create and write to file two reports.
        gen_report()

    # Exit program function, available to all users.
    elif choice == "e":
        exit("e")

    # Incorrect option selected.
    else:
        print("\nYou have selected an incorrect option, please try again.")
