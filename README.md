

---

# Task Management System with NLP

This is an advanced Python-based task management system that leverages Natural Language Processing (NLP) to allow users to input tasks in plain English. The system automatically parses the input to schedule tasks and send reminders, optionally using WhatsApp.

## Features

- **Natural Language Task Input**: Users can enter tasks in plain language, such as "Remind me to study physics tomorrow at 5 PM".
- **NLP-Based Parsing**: Uses `spaCy` to extract task details like task description, date, and time from natural language.
- **Task Scheduling**: Automatically schedules tasks and runs reminders using the `schedule` library.
- **Persistent Storage**: Stores tasks in an SQLite database to ensure they persist across sessions.
- **WhatsApp Integration (Optional)**: Sends task reminders via WhatsApp using `pywhatkit`.
- **Real-Time Task Monitoring**: Constantly checks for tasks due and sends reminders at the specified time.

## Installation

To run the project locally, follow these steps:

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or above
- pip (Python package manager)

### Libraries

Install the required Python libraries:

```bash
pip install spacy schedule pywhatkit sqlite3
```

Download and install the NLP model for `spaCy`:

```bash
python -m spacy download en_core_web_sm
```

### Setting up WhatsApp Integration (Optional)

For WhatsApp reminders, you need to install and configure `pywhatkit`:

1. Ensure you have WhatsApp Web logged in on your default browser.
2. Make sure you set up your country code for phone numbers in `pywhatkit`.

## Usage

1. **Run the Program**:
   After setting up, run the main program:

   ```bash
   python task_manager.py
   ```

2. **Add a Task**:
   When prompted, you can input tasks in natural language. For example:
   ```bash
   Enter your task: Remind me to study physics tomorrow at 5 PM
   ```

   The system will parse the task, date, and time from this input and schedule it.

3. **Scheduled Tasks**:
   The tasks are stored in an SQLite database and reminders are triggered at the specified times. If you have WhatsApp integration enabled, the system will send a reminder message to the specified contact.

## Project Structure

```
.
├── task_manager.py     # Main program
├── tasks.db            # SQLite database to store tasks
└── README.md           # Project documentation
```

## How It Works

- **Task Input Parsing**: The program uses `spaCy` to analyze user input and extract meaningful information like task description, date, and time.
- **Scheduling**: The `schedule` library runs tasks at specified times, checking every second whether a task is due.
- **Persistent Storage**: Tasks are stored in an SQLite database, so they are retained across program sessions.
- **WhatsApp Reminders**: Using `pywhatkit`, the system sends reminders to WhatsApp contacts when tasks are due.

## Customization

- **Changing Reminder Method**: You can modify the `send_reminder()` function to send reminders through email, SMS, or other methods if WhatsApp is not preferred.
- **Task Deletion or Modification**: Currently, tasks are automatically executed at the specified time. You can extend the system to include task modification or deletion by querying and updating the SQLite database.

## Future Improvements

- **GUI Integration**: Add a graphical user interface using `Tkinter` or `PyQt5` for easy task management.
- **Extended NLP**: Improve the NLP model to handle more complex task descriptions or integrate with more powerful language models like OpenAI.
- **Calendar Integration**: Add integration with Google Calendar or other calendar APIs for better task scheduling.

## Contributing

If you'd like to contribute to this project, feel free to submit pull requests or report issues. Any contributions are highly appreciated!
