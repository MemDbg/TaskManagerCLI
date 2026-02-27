from MySQLConnection import MySQLConnection
from datetime import date
from typing import Literal


class TaskManagerRepository:
    def __init__(self, db_context: MySQLConnection):
        self.__db_context = db_context

    def does_task_exists(self, task_id: int) -> bool:
        """
        Check if a task with the given task_id exists in the database.
        """
        query = "SELECT 1 FROM tasks WHERE task_id = %s LIMIT 1"

        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")
            cursor.execute(query, (task_id,))
            result = cursor.fetchone()

        return result is not None

    def add_new_task(
        self,
        title: str,
        description: str,
        due_date: date,
        priority_level: Literal["Low", "Medium", "High"],
        status: Literal["Pending", "In Progress", "Completed"],
    ):
        """
        Creates a new task
        """

        query = """
            INSERT INTO tasks (title, description, due_date, priority_level, status)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (title, description, due_date, priority_level, status)
        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")
            cursor.execute(query, values)

    def list_all_tasks(
        self, page: int = 1, sort_by: str | None = None, items_per_page: int = 5
    ):
        """
        List tasks with pagination.
        """

        allowed_sort_columns = {
            "due_date": "due_date",
            "priority": "priority_level",
            "status": "status",
        }

        # base query for fetching tasks
        base_query = "SELECT * FROM tasks"
        if sort_by:
            column = allowed_sort_columns.get(sort_by)
            if not column:
                raise ValueError("Invalid sort field.")
            base_query += f" ORDER BY {column}"

        # calculate pagination
        offset = (page - 1) * items_per_page
        paged_query = f"{base_query} LIMIT {items_per_page} OFFSET {offset}"

        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")

            # get total count
            cursor.execute("SELECT COUNT(*) AS total FROM tasks")
            total_items = cursor.fetchone()["total"]
            total_pages = (total_items + items_per_page - 1) // items_per_page

            # fetch current page
            cursor.execute(paged_query)
            tasks = cursor.fetchall()

        return tasks, total_pages

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        due_date: date | None = None,
        priority_level: Literal["Low", "Medium", "High"] | None = None,
        status: Literal["Pending", "In Progress", "Completed"] | None = None,
    ):
        """
        Update one or more fields of a task.
        Only provided fields will be updated.
        """

        fields = []
        values = []

        if title is not None:
            fields.append("title = %s")
            values.append(title)

        if description is not None:
            fields.append("description = %s")
            values.append(description)

        if due_date is not None:
            fields.append("due_date = %s")
            values.append(due_date)

        if priority_level is not None:
            fields.append("priority_level = %s")
            values.append(priority_level)

        if status is not None:
            fields.append("status = %s")
            values.append(status)

        if not fields:
            raise ValueError("No fields provided for update.")

        query = f"""
            UPDATE tasks
            SET {', '.join(fields)}
            WHERE task_id = %s
        """

        values.append(task_id)

        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")
            cursor.execute(query, tuple(values))

    def mark_task_completed(self, task_id: int):
        """
        Sets task status to Completed.
        """

        query = """
            UPDATE tasks
            SET status = 'Completed'
            WHERE task_id = %s
        """

        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")
            cursor.execute(query, (task_id,))

    def delete_task(self, task_id: int):
        """
        Delete a task by ID.
        """

        query = "DELETE FROM tasks WHERE task_id = %s"

        with self.__db_context as cursor:
            cursor.execute("USE task_manager_db;")
            cursor.execute(query, (task_id,))
