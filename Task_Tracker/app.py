from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        deadline DATE NOT NULL,
        priority TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def register_or_login():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Please choose a different username."

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        # Query the database for the user's credentials
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and user[2] == password:
            # Successful login, redirect to index.html
            return redirect(url_for('index'))
        else:
            return "Login failed. Invalid username or password."

    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        data = request.get_json()
        task_text = data['text']
        task_deadline = data['deadline']
        task_priority = data['priority']

        # Insert the task into the database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (text, deadline, priority) VALUES (?, ?, ?)', (task_text, task_deadline, task_priority))
        conn.commit()
        conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
