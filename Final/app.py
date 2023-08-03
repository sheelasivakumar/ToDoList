from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = "your_secret_key_here"

def create_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, status INTEGER NOT NULL, user_id INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

def create_user_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Adding a data to table 
def register_user(username,password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
    conn.commit()
    conn.close()

def is_authenticated():
    return "user_id" in session

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/home')
def home():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    user_id = session["user_id"]
    user = session["username"]
    c.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?",(user_id,))
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE status = 1 AND user_id = ?",(user_id,))
    complete_tasks = c.fetchone()[0]
    not_completed_task = total_tasks - complete_tasks
    c.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY id",(user_id,))
    tasks = c.fetchall()
    conn.close()
    return render_template('home.html', tasks=tasks,total_todo = total_tasks,completed_todo=complete_tasks,uncompleted = not_completed_task,user=user)

# Registration Page Action
@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        register_user(username,password)
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("index"))
    else:
        flash
        return render_template("register.html")

# Login Page Action 
@app.route('/login',methods =["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT username,password FROM users WHERE username=? and password=?",(username,password))
        result = c.fetchone()
        if result:
            session["user_id"] = result[0]
            session["username"] = username
            return redirect(url_for("home"))
        else:
             flash("Invalid credentials. Please try again.", "error")
             return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/add', methods=["POST"])
def add_task():
    if not is_authenticated():
        flash("Please log in to add tasks.", "error")
        return redirect(url_for('login'))

    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"] 

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)",
              (title, description, 0, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if not is_authenticated():
        flash("Please log in to complete tasks.", "error")
        return redirect(url_for('login'))
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    status = c.fetchone()[0]
    new_status = 0 if status == 1 else 1
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if not is_authenticated():
        flash("Please log in to delete tasks.", "error")
        return redirect(url_for('login'))
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id =?",(task_id,))
    c.execute("SELECT id FROM tasks")
    rows = c.fetchall()
    for i,row in enumerate(rows,start=1):
        c.execute("UPDATE tasks SET id = ? WHERE id=?",(i,row[0]))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    session.pop("username",None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))  

if __name__ == "__main__":
    create_table()
    create_user_table()
    app.run(debug=True)