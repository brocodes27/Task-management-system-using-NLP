import spacy
import schedule
import time
import pywhatkit
import sqlite3
from datetime import datetime

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
    time = None
    date = None
    for token in doc:
        if token.ent_type_ == "TIME":
            time = token.text
        elif token.ent_type_ == "DATE":
            date = token.text
        else:
            task.append(token.text)
    return " ".join(task), date, time

# Schedule task for reminder
def schedule_task(task, task_date, task_time):
    task_datetime = datetime.strptime(f'{task_date} {task_time}', '%Y-%m-%d %H:%M')
    schedule.every().day.at(task_time).do(send_reminder, task)

# Send reminder via WhatsApp (you can use email or any other service)
def send_reminder(task):
    pywhatkit.sendwhatmsg_instantly("+911234567890", f"Reminder: {task}", 15, True, 2)

# Main loop
def main():
    init_db()
    while True:
        user_input = input("Enter your task: ")
        task, task_date, task_time = parse_task(user_input)
        add_task(task, task_date, task_time)
        schedule_task(task, task_date, task_time)
        print(f"Task '{task}' scheduled on {task_date} at {task_time}")

        # Check if it's time to execute any task
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
