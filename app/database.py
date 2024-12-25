import sqlite3

# Initialize database
def start_db():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            userid INTEGER UNIQUE,
            language TEXT,
            city TEXT,
            phone INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Add a new user to the database
def add_user(username, user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    try:
        curr.execute('INSERT INTO users (username, userid) VALUES (?, ?)', (username, user_id))
    except sqlite3.IntegrityError:
        pass  # Ignore if user already exists
    conn.commit()
    conn.close()

# Get user from the database
def get_user(user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
    user = curr.fetchone()
    conn.close()
    return user

# Update user language
def update_language(user_id, language):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('UPDATE users SET language = ? WHERE userid = ?', (language, user_id))
    conn.commit()
    conn.close()

# Update user city
def update_city(user_id, city):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('UPDATE users SET city = ? WHERE userid = ?', (city, user_id))
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')  # Replace with your actual database file
    return conn

# Function to update the user's name
def update_name(user_id, new_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ? WHERE userid = ?", (new_name, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to update the user's phone number
def update_phone(user_id, new_phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET phone = ? WHERE userid = ?", (new_phone, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to update the user's city
def update_city(user_id, new_city):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET city = ? WHERE userid = ?", (new_city, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_user_language(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE userid = ?", (user_id,))
    language = cursor.fetchone()
    conn.close()
    return language[0] if language else "English"


def save_feedback(user_id, username, rating, comment=None, language="English"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (userid, username, rating, comment, language) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, rating, comment, language)
    )
    conn.commit()
    cursor.close()
    conn.close()