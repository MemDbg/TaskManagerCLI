# Task Manager CLI

A simple command-line task manager built with Python and MySQL.  
It allows you to **add, list, update, mark as completed, and delete tasks**. Tasks include title, description, due date, priority, and status.

---

## Features

- Add new tasks with priority and status
- List tasks with pagination and sorting
- Update task details selectively
- Mark tasks as completed
- Delete tasks with confirmation

---

## Requirements

- Python 3.10+
- MySQL server
- Python package: `mysql-connector-python`

---

## Setup

1. **Clone the repository**.  
```bash
git clone https://github.com/MemDbg/TaskManagerCLI.git
```

2. **Install dependencies**:  
```bash
pip install -r requirements.txt
```

3. **Ensure MySQL server is running** and accessible (update `Main.py` if different).

   * Default host: `127.0.0.1`
   * Default port: `3306`
   * Default user: `root` 

4. **Run the program**:

```bash
python Main.py
```

> **Note:** The database and table are automatically created by the Python code if it does not exist.