# To_Do_List
# This project is a simple Command Line Interface (CLI) To_Do_List application written in Python.

This project includes automated unit tests written using Python’s built-in unittest framework.
The application allows users to manage their daily tasks directly from the terminal using basic commands. 
Tasks can be added, marked as completed, removed, and listed at any time.
The program is designed to demonstrate:
 - Object-Oriented Programming (OOP)
 - Exception handling
 - Command parsing
 - Dictionary-based task management
 - Interactive CLI applications in Python

# Features
- The application supports the following commands:
1. ADD <task_description> --- Adds a new task
2. REMOVE <task_id> --- Removes a task
3. DONE <task_id> --- Marks a task as completed
4. LIST --- Displays all tasks
5. EXIT --- Closes the application
   
Each task contains:
 - Unique ID.
 - Task description.
 - Completion status.

# Examples:
'''
>ADD LISTA

>LIST

0:[ ]LISTA

>DONE 0

>ADD TWO

>LIST

0:[X]LISTA

1:[ ]TWO

>REMOVE 0

>LIST

1:[ ]TWO

'''

#How to run:
Check your Python version:
- python --version

Clone the repository
- git clone https://github.com/TWOJ_LOGIN/TWOJE_REPO.git
 Navigate to the project folder
- cd YOUR_REPOSITORY
 Run the application
- python main.py
