from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, random
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change for production

# ---------------------- DATABASE CONNECTION ---------------------- #
def get_db_connection():
    conn = sqlite3.connect('railway.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------- HOME PAGE ---------------------- #
@app.route('/')
def home():
    return render_template('index.html')

# ---------------------- USER SIGNUP ---------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                         (username, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            conn.close()
            return render_template('signup.html', error="Username or Email already exists!")
    return render_template('signup.html')

# ---------------------- USER LOGIN ---------------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect(url_for('view_trains'))
        else:
            return render_template('login.html', error="Invalid Email or Password!")
    return render_template('login.html')

# ---------------------- USER LOGOUT ---------------------- #
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------------------- VIEW TRAINS ---------------------- #
@app.route('/view_trains')
def view_trains():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    trains = conn.execute("SELECT * FROM train").fetchall()
    conn.close()
    return render_template('view_trains.html', trains=trains)

# ---------------------- BOOK TICKET PAGE ---------------------- #
@app.route('/book_ticket')
def book_ticket_page():
    if 'user' not in session:
        return redirect(url_for('login'))

    train_no = request.args.get('train_no')
    return render_template('book_ticket.html', train_no=train_no)

# ---------------------- BOOK TICKET PROCESS ---------------------- #
@app.route('/book', methods=['POST'])
def book_ticket():
    if 'user' not in session:
        return redirect(url_for('login'))

    name = session['user']  # Logged-in username
    train_no = request.form['train_no']
    seats = int(request.form['seats_booked'])

    conn = get_db_connection()
    train = conn.execute("SELECT * FROM train WHERE train_no=?", (train_no,)).fetchone()

    if train and train['total_seats'] >= seats:
        total_fare = seats * train['fare']

        conn.execute("INSERT INTO booking (passenger_name, train_no, seats_booked, total_fare) VALUES (?, ?, ?, ?)",
                     (name, train_no, seats, total_fare))
        conn.execute("UPDATE train SET total_seats = total_seats - ? WHERE train_no=?", (seats, train_no))
        conn.commit()

        booking_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()

        return redirect(url_for('ticket', booking_id=booking_id))
    else:
        conn.close()
        return render_template('bookings.html', message="❌ Not enough seats available.")

# ---------------------- MY BOOKINGS PAGE ---------------------- #
@app.route('/my_bookings')
def my_bookings():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.booking_id, b.train_no, b.seats_booked, b.total_fare,
               t.train_name, t.source, t.destination
        FROM booking b
        JOIN train t ON b.train_no = t.train_no
        WHERE b.passenger_name = ?
    ''', (username,)).fetchall()
    conn.close()
    return render_template('my_bookings.html', bookings=bookings, user_name=username)

# ---------------------- VIEW TICKET PAGE ---------------------- #
@app.route('/ticket/<int:booking_id>')
def ticket(booking_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    ticket = conn.execute('''
        SELECT b.booking_id, b.passenger_name, b.train_no, b.seats_booked, b.total_fare,
               t.train_name, t.source, t.destination, t.arrival_time, t.destination_time
        FROM booking b
        JOIN train t ON b.train_no = t.train_no
        WHERE b.booking_id = ?
    ''', (booking_id,)).fetchone()
    conn.close()

    if not ticket:
        return render_template('bookings.html', message="❌ Ticket not found.")

    random_ticket_no = random.randint(100000, 999999)
    return render_template('ticket.html', ticket=ticket, ticket_no=random_ticket_no)

# ---------------------- CANCEL BOOKING ---------------------- #
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    booking = conn.execute("SELECT * FROM booking WHERE booking_id=?", (booking_id,)).fetchone()

    if not booking:
        conn.close()
        return render_template('bookings.html', message="❌ Booking not found.")

    conn.execute("UPDATE train SET total_seats = total_seats + ? WHERE train_no=?",
                 (booking['seats_booked'], booking['train_no']))
    conn.execute("DELETE FROM booking WHERE booking_id=?", (booking_id,))
    conn.commit()
    conn.close()

    return render_template('bookings.html', message=f"✅ Booking ID {booking_id} has been cancelled successfully!")

# ---------------------- RUN THE APP ---------------------- #
if __name__ == '__main__':
    app.run(debug=True)

