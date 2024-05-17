import sqlite3

def create_tables():
    conn = sqlite3.connect('kanye.db')
    c = conn.cursor()

    # Create payments table
    c.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_number TEXT NOT NULL,
        card_number TEXT NOT NULL,
        expiration_month INTEGER NOT NULL,
        expiration_year INTEGER NOT NULL,
        cvv TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
