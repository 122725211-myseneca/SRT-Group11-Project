from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

movies = ["Dune part 2", "Kung Fu Panda 4", "Yodha", "Godzilla"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time_options = ["12:00 pm", "3:00 pm", "6:00 pm", "9:00 pm"]
places = ["North York", "Brampton", "Toronto Downtown", "Scarborough"]
seat_rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
seat_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]

schema_query = '''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    movie TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    place TEXT NOT NULL,
    seat_row TEXT NOT NULL,
    seat_number INTEGER NOT NULL,
    UNIQUE(day, time, place, seat_row, seat_number)
);
'''

def init_db():
    try:
        with app.app_context():
            db = sqlite3.connect('movie_booking.db')
            db.row_factory = sqlite3.Row
            db.execute(schema_query)
            db.commit()
    except Exception as e:
        print("Error during database initialization:", e)

init_db()

@app.route('/')
def index():
    return render_template('booking.html', movies=movies, days=days, time=time_options, places=places,
                           seat_rows=seat_rows, seat_numbers=seat_numbers)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    movie = request.form['movie']
    day = request.form['day']
    time = request.form['time']
    place = request.form['place']
    seat_row = request.form['seat_row']
    seat_number = int(request.form['seat_number'])

    db = sqlite3.connect('movie_booking.db')
    cursor = db.cursor()

    try:
        cursor.execute('SELECT * FROM bookings WHERE day = ? AND time = ? AND place = ? AND seat_row = ? AND seat_number = ?',
                       (day, time, place, seat_row, seat_number))
        existing_booking = cursor.fetchone()
        if existing_booking:
            flash('Seat already booked! Please choose another.', 'error')
        else:
            cursor.execute('INSERT INTO bookings (name, email, movie, day, time, place, seat_row, seat_number) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, email, movie, day, time, place, seat_row, seat_number))
            db.commit()
            flash('Booking successful! Enjoy the movie!', 'success')
    except sqlite3.IntegrityError:
        flash('Seat already booked! Please choose another.', 'error')
    finally:
        db.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
