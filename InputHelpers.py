from datetime import date, datetime
from TaskManagerRepository import TaskManagerRepository

def input_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Value cannot be empty.")


def input_optional(prompt: str) -> str | None:
    val = input(prompt).strip()
    return val if val else None


def input_date(prompt: str) -> date | None:
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            return datetime.strptime(val, "%m-%d-%Y").date()
        except ValueError:
            print("Invalid date format. Use MM-DD-YYYY.")


def input_choice_number(prompt: str, choices: list[str]) -> str:
    print(prompt)
    for idx, option in enumerate(choices, 1):
        print(f"{idx}. {option}")
    while True:
        try:
            selection = int(input(f"Enter choice (1-{len(choices)}): ").strip())
            if 1 <= selection <= len(choices):
                return choices[selection - 1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def input_task_id(repo: TaskManagerRepository) -> int | None:
    while True:
        try:
            task_id = int(input_non_empty("Enter Task ID: "))
            if repo.does_task_exists(task_id):
                return task_id
            else:
                print(f"Task with ID {task_id} does not exist.")
        except ValueError:
            print("Invalid number.")