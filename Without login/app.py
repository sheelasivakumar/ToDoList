# Importing Necessary dependencies 
from flask import Flask, render_template, redirect, url_for,request

import  sqlite3

# Creating a function for Creating a table: To store the task 
def create_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, status INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Creating an Instance of the Flask class
app = Flask(__name__,static_url_path='/static')
app.secret_key = "xksasrstahaiak"

# Creating an index 
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 1")
    complete_tasks = c.fetchone()[0]
    not_completed_task = total_tasks - complete_tasks
    c.execute("SELECT * FROM tasks ORDER BY id")
    tasks = c.fetchall()
    conn.close()
    return render_template('home.html', tasks=tasks,total_todo = total_tasks,completed_todo=complete_tasks,uncompleted = not_completed_task)


# Adding task 
@app.route('/add',methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, description, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Toggle the task b/w completed or not 
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    status = c.fetchone()[0]
    new_status = 0 if status == 1 else 1

    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Delete a Particular tasks
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id =?",(task_id,))
    c.execute("SELECT id FROM tasks")
    rows = c.fetchall()
    for i,row in enumerate(rows,start=1):
        c.execute("UPDATE tasks SET id = ? WHERE id=?",(i,row[0]))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))



if __name__ == "__main__":
    create_table()
    app.run(debug=True)