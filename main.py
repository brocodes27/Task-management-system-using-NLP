import spacy
import schedule
import time
import pywhatkit
import sqlite3
from datetime import datetime
from tkinter import *

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, time TEXT, date TEXT)''')
    conn.commit()
    conn.close()

# Add task to database
def add_task(task, task_date, task_time):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, time, date) VALUES (?, ?, ?)", (task, task_time, task_date))
    conn.commit()
    conn.close()

# Retrieve tasks from database
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# Parse task using NLP
def parse_task(task_string):
    doc = nlp(task_string)
    task = []
    task_time = None
    task_date = None
    for token in doc:
        if token.ent_type_ == "TIME":
            task_time = token.text
        elif token.ent_type_ == "DATE":
            task_date = token.text
        else:
            task.append(token.text)
    return " ".join(task), task_date, task_time

# Schedule task for reminder
def schedule_task(task, task_date, task_time):
    task_datetime = datetime.strptime(f'{task_date} {task_time}', '%Y-%m-%d %H:%M')
    schedule.every().day.at(task_time).do(send_reminder, task)

# Send reminder via WhatsApp (you can use email or any other service)
def send_reminder(task):
    pywhatkit.sendwhatmsg_instantly("+911234567890", f"Reminder: {task}", 15, True, 2)

# Add task from GUI
def add_task_from_gui():
    user_input = task_entry.get()
    task, task_date, task_time = parse_task(user_input)
    if task and task_date and task_time:
        add_task(task, task_date, task_time)
        schedule_task(task, task_date, task_time)
        task_entry.delete(0, END)
        display_tasks()

# Display tasks in the GUI
def display_tasks():
    tasks = get_tasks()
    task_listbox.delete(0, END)  # Clear the listbox before updating
    for task in tasks:
        task_listbox.insert(END, f"Task: {task[1]}, Date: {task[3]}, Time: {task[2]}")

# Main GUI setup
def create_gui():
    global task_entry, task_listbox

    root = Tk()
    root.title("Task Manager with NLP")
    
    # Task input area
    Label(root, text="Enter Task:").grid(row=0, column=0)
    task_entry = Entry(root, width=50)
    task_entry.grid(row=0, column=1)
    
    add_task_btn = Button(root, text="Add Task", command=add_task_from_gui)
    add_task_btn.grid(row=0, column=2)

    # Task list display
    task_listbox = Listbox(root, width=80, height=15)
    task_listbox.grid(row=1, column=0, columnspan=3)

    # Run display
    display_tasks()

    root.mainloop()

# Main loop
def main():
    init_db()
    create_gui()

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
