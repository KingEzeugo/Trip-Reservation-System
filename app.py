from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from utils.helpers import get_cost_matrix, generate_reservation_code, calculate_total_sales

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DATABASE = './db/reservations.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'Admin' and password == 'P455W0RD':
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    reservations = conn.execute('SELECT * FROM reservations').fetchall()
    total_sales = calculate_total_sales()
    conn.close()

    seating_chart = [['Available' for _ in range(4)] for _ in range(12)]
    for reservation in reservations:
        seating_chart[reservation['row'] - 1][reservation['col'] - 1] = 'Reserved'

    return render_template('seating_chart.html', seating_chart=seating_chart, total_sales=total_sales)


@app.route('/reserve', methods=['GET', 'POST'])
def reserve_seat():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        seat_row = int(request.form['seat_row'])
        seat_col = int(request.form['seat_col'])

        conn = get_db_connection()
        seat_check = conn.execute(
            'SELECT * FROM reservations WHERE row = ? AND col = ?', (seat_row, seat_col)
        ).fetchone()

        if seat_check:
            flash('Seat already reserved. Choose another.', 'error')
        else:
            reservation_code = generate_reservation_code()
            cost_matrix = get_cost_matrix()
            seat_cost = cost_matrix[seat_row - 1][seat_col - 1]

            conn.execute(
                'INSERT INTO reservations (first_name, last_name, row, col, cost, code) VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, last_name, seat_row, seat_col, seat_cost, reservation_code),
            )
            conn.commit()
            conn.close()

            return render_template('confirmation.html', code=reservation_code, cost=seat_cost)

    return render_template('reserve_seat.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
