import sqlite3

conn = sqlite3.connect('railway.db')
c = conn.cursor()

# Train table
c.execute('''
CREATE TABLE IF NOT EXISTS train (
    train_no INTEGER PRIMARY KEY,
    train_name TEXT,
    source TEXT,
    destination TEXT,
    total_seats INTEGER,
    fare INTEGER
)
''')

# Booking table
c.execute('''
CREATE TABLE IF NOT EXISTS booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT,
    train_no INTEGER,
    seats_booked INTEGER,
    total_fare INTEGER,
    FOREIGN KEY(train_no) REFERENCES train(train_no)
)
''')

conn.commit()
conn.close()
print("✅ Database created successfully!")
