


    
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
import sqlite3, datetime, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

DB = 'site.db'

    
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        message TEXT,
        time TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS software(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        filename TEXT,
        time TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/software')
def software():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, filename FROM software ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template('software.html', softwares=data)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    name = request.form.get("name")
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO software(name,filename,time) VALUES(?,?,?)",
                  (name,file.filename,str(datetime.datetime.now())))
        conn.commit()
        conn.close()
    return redirect(url_for('software'))

@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/guestbook')
def guestbook():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name,message,time FROM messages ORDER BY id DESC")
    msgs = c.fetchall()
    conn.close()
    return render_template('guestbook.html', messages=msgs)

@app.route('/add_message', methods=['POST'])
def add_message():
    name = request.form.get("name")
    message = request.form.get("message")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO messages(name,message,time) VALUES(?,?,?)",
              (name,message,str(datetime.datetime.now())))
    conn.commit()
    conn.close()
    return redirect(url_for('guestbook'))

if __name__ == '__main__':
    init_db()
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

