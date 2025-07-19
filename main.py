import sqlite3

DB_NAME = "todo.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

def get_next_id():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM tasks")
        result = cursor.fetchone()[0]
        return 1 if result is None else result + 1

def add_task(task_text):
    task_id = get_next_id()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (id, task, done) VALUES (?, ?, 0)", (task_id, task_text))
        conn.commit()
    print(f"✅ Task added with an ID {task_id}.")

def list_tasks(pending_only=False):
    with get_connection() as conn:
        cursor = conn.cursor()
        if pending_only:
            cursor.execute("SELECT id, task, done FROM tasks WHERE done = 0 ORDER BY id")
        else:
            cursor.execute("SELECT id, task, done FROM tasks ORDER BY id")
        tasks = cursor.fetchall()
        if not tasks:
            print("📭 No tasks.")
        for task in tasks:
            status = "✅" if task[2] else "🕒"
            print(f"{task[0]}. {status} {task[1]}")

def mark_done(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print("⚠️ No task found.")
        else:
            conn.commit()
            print("🎉 Task is done!")

def delete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print("⚠️ No task found.")
        else:
            conn.commit()
            print("🗑️ Task deleted.")

def show_help():
    print("📒 Welcome to To-Do")
    print("Commands:")
    print('  add "Task name"   — Add task')
    print("  list                 — Show all the tasks")
    print("  list pending       — Show undone tasks only")
    print("  done <id>            — Mark task as 'Done'")
    print("  delete <id>          — Delete task")
    print("  exit                 — Exit")

def main():
    init_db()
    show_help()
    while True:
        cmd = input("👉 Enter the command: ").strip()
        if cmd.startswith("add "):
            task_text = cmd[4:].strip().strip('"')
            add_task(task_text)
        elif cmd == "list":
            list_tasks()
        elif cmd == "list pending":
            list_tasks(pending_only=True)
        elif cmd.startswith("done "):
            try:
                task_id = int(cmd[5:])
                mark_done(task_id)
            except ValueError:
                print("❗ Wrong ID form.")
        elif cmd.startswith("delete "):
            try:
                task_id = int(cmd[7:])
                delete_task(task_id)
            except ValueError:
                print("❗ Wrong ID form.")
        elif cmd == "exit":
            print("👋 Goodbye!!")
            break
        else:
            print("❓ Unknown command. Say 'help' for commands.")

if __name__ == "__main__":
    main()
