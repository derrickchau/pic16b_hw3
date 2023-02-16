from flask import Flask
from flask import render_template, g, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    '''
    Renders submit.html
    '''
    if request.method == 'GET': 
        return render_template('submit.html') # Render submit.html when initially entering page
    else:
        message, handle = insert_message() # Insert message into bank and render submit.html
        return render_template('submit.html', submitted=True, message=message, handle=handle)


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    '''
    Renders submit.html
    '''
    if request.method == 'GET':
        return render_template('submit.html') # Render submit.html when initially entering page
    else:
        message, handle = insert_message() # Insert message into bank and render submit.html
        return render_template('submit.html', submitted=True, message=message, handle=handle)


def get_message_db():
    '''
    Get or create a database to hold the messages
    '''

    try:
        return g.message_db
    
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite") # Connect to a SQL database 
        # Creates table if it doesn't already exist holding id, message, handle
        cmd = \
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                handle TEXT NOT NULL)
            """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db


def insert_message():
    '''
    Inserts the message into the existing database
    '''

    # Extracts message and handle from request
    message = request.form['message']
    handle = request.form['handle']

    # Retrieves database with all messages and inserts message
    conn = get_message_db()
    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ('{message}', '{handle}')
    """

    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()

    return message, handle


def random_messages(n):
    '''
    Randomly chooses and returns n messages from the database
    '''
    conn = get_message_db()

    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """
    cursor = conn.cursor()
    cursor.execute(cmd)
    result = cursor.fetchall()
    conn.close()

    return result


@app.route('/view/')
def view(): 
    return render_template('view.html', messages=random_messages(5))