
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = 'testpro.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tab (id INTEGER PRIMARY KEY, content TEXT, date_created TIMESTAMP)')
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM tab ORDER BY date_created')
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task(content):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO tab (content, date_created) VALUES (?, ?)', (content, datetime.utcnow()))
    conn.commit()
    conn.close()

def delete_task(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM tab WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_task(id, content):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE tab SET content = ? WHERE id = ?', (content, id))
    conn.commit()
    conn.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        add_task(task_content)
        return redirect('/')
    else:
        tasks = get_tasks()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task(id)
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = None
    if request.method == 'POST':
        content = request.form['content']
        update_task(id, content)
        return redirect('/')
    else:
        tasks = get_tasks()
        for t in tasks:
            if t[0] == id:
                task = t
                break
        return render_template('update.html', task=task)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)