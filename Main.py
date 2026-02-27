from MySQLConnection import MySQLConnection
from TaskManagerRepository import TaskManagerRepository
import InputHelpers as ih

# Options
PRIORITY_LEVELS = ["Low", "Medium", "High"]
STATUS_OPTIONS = ["Pending", "In Progress"]
ITEMS_PER_PAGE = 5

# Credentials
TASK_APP_DB_HOST = "127.0.0.1"
TASK_APP_DB_PORT = 3306
TASK_APP_DB_USER = "root"
TASK_APP_DB_PASS = ""


def InitializeDatabase() -> MySQLConnection:
    db_context = MySQLConnection(
        host=TASK_APP_DB_HOST,
        port=TASK_APP_DB_PORT,
        user=TASK_APP_DB_USER,
        password=TASK_APP_DB_PASS,
    )

    with db_context as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_manager_db;")
        cursor.execute("USE task_manager_db;")
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATE,
            priority_level ENUM('Low', 'Medium', 'High') NOT NULL DEFAULT 'Medium',
            status ENUM('Pending', 'In Progress', 'Completed') NOT NULL DEFAULT 'Pending',
            creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        )

    return db_context

# App Tasks

def add_task(repo: TaskManagerRepository):
    print("\nAdd New Task:")
    title = ih.input_non_empty("Title: ")
    description = ih.input_optional("Description (optional): ")
    due_date = ih.input_date("Due Date (MM-DD-YYYY, optional): ")
    priority = ih.input_choice_number("Select Priority Level:", PRIORITY_LEVELS)
    status = ih.input_choice_number("Select Status:", STATUS_OPTIONS)

    repo.add_new_task(title, description, due_date, priority, status)
    print("Task added successfully!")


def list_tasks(repo: TaskManagerRepository):
    print("\nList Tasks:")
    sort_by = ih.input_optional(
        "Sort by (1: due_date, 2: priority, 3: status, leave blank for none): "
    )
    sort_map = {"1": "due_date", "2": "priority", "3": "status"}
    sort_column = sort_map.get(sort_by) if sort_by else None

    page = 1
    while True:
        tasks, total_pages = repo.list_all_tasks(
            page=page, sort_by=sort_column, items_per_page=ITEMS_PER_PAGE
        )
        if not tasks:
            print("No tasks found.")
            break

        headers = ["ID", "Title", "Description", "Status", "Priority", "Due Date"]
        col_widths = [5, 20, 50, 15, 10, 12]

        # header
        header_line = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
        print("\n" + header_line)
        print("-" * sum(col_widths))

        # iterate through all tasks
        for t in tasks:
            due = t["due_date"] or "None"
            desc = (t["description"] or "").replace("\n", " ")
            row = [
                str(t["task_id"]),
                t["title"][: col_widths[1] - 1],
                desc[: col_widths[2] - 1],
                t["status"],
                t["priority_level"],
                str(due),
            ]
            print("".join(f"{c:<{w}}" for c, w in zip(row, col_widths)))

        # page handler
        print(f"\nPage {page}/{total_pages}")
        if page >= total_pages:
            break
        next_page = input("Press Enter for next page or 'q' to quit: ").strip().lower()
        if next_page == "q":
            break
        page += 1


def update_task(repo: TaskManagerRepository):
    print("\nUpdate Task:")
    task_id = ih.input_task_id(repo)
    title = ih.input_optional("New Title (leave blank to keep current): ")
    description = ih.input_optional("New Description (leave blank to keep current): ")
    due_date = ih.input_date("New Due Date (MM-DD-YYY, leave blank to keep current): ")
    priority = (
        ih.input_choice_number(
            "New Priority (leave blank to keep current):", PRIORITY_LEVELS
        )
        if ih.input_optional("Change priority? (y/n): ") == "y"
        else None
    )
    status = (
        ih.input_choice_number("New Status (leave blank to keep current):", STATUS_OPTIONS)
        if ih.input_optional("Change status? (y/n): ") == "y"
        else None
    )

    try:
        repo.update_task(task_id, title, description, due_date, priority, status)
        print("Task updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def mark_task_completed(repo: TaskManagerRepository):
    print("\nMark Task Completed:")
    task_id = ih.input_task_id(repo)
    repo.mark_task_completed(task_id)
    print(f"Task {task_id} marked as completed!")


def delete_task(repo: TaskManagerRepository):
    print("\nDelete Task:")
    task_id = ih.input_task_id(repo)
    confirm = (
        input(f"Are you sure you want to delete task {task_id}? (y/n): ")
        .strip()
        .lower()
    )
    if confirm == "y":
        repo.delete_task(task_id)
        print("Task deleted.")
    else:
        print("Delete cancelled.")


def Main():
    db_context = InitializeDatabase()
    task_mgr_repo = TaskManagerRepository(db_context)

    menu_options = {
        "1": ("Add Task", lambda: add_task(task_mgr_repo)),
        "2": ("List Tasks", lambda: list_tasks(task_mgr_repo)),
        "3": ("Update Task", lambda: update_task(task_mgr_repo)),
        "4": ("Mark Task Completed", lambda: mark_task_completed(task_mgr_repo)),
        "5": ("Delete Task", lambda: delete_task(task_mgr_repo)),
        "6": ("Quit", lambda: exit()),
    }

    while True:
        print("\nTask Manager:")
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")

        choice = input("Choose an option: ").strip()
        action = menu_options.get(choice)
        if action:
            _, task_to_run = action
            task_to_run()
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    Main()
