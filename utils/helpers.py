import random
import string
import sqlite3

DATABASE = './db/reservations.db'


def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(12)]


def generate_reservation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def calculate_total_sales():
    conn = sqlite3.connect(DATABASE)
    total = conn.execute('SELECT SUM(cost) FROM reservations').fetchone()[0]
    conn.close()
    return total or 0
