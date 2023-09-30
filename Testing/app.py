from flask import Flask, render_template, request

app= Flask(__name__)

# SQLite database setup
import sqlite3
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()#it creates a cursor object, which is used to execute SQL commands
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
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        data = request.get_json()
        task_text = data['text']
        task_deadline = data['deadline']
        task_priority = data['priority']

        #it will insert task into  database
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (text, deadline, priority) VALUES (?, ?, ?)', (task_text, task_deadline, task_priority))
        conn.commit()
        conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)