from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from model import predict_life

app = Flask(__name__)
app.secret_key = "aede2be57ee5034c5b613f158a6b65fdd483b3c5145c70d8"  # Required for flash messages

# Database configuration
DATABASE = 'smart_shelf.db'


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


@app.route('/')
def index():
    """Fetches all items from the database and renders the dashboard."""
    try:
        conn = get_db_connection()
        # Fetching items sorted by newest first
        items = conn.execute('SELECT * FROM inventory ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('index.html', items=items)
    except sqlite3.OperationalError:
        return "Database not initialized. Please run database.py first."


@app.route('/add', methods=['POST'])
def add_item():
    """
    Handles form submission:
    1. Receives item name and category.
    2. Calls the ML model to predict shelf life.
    3. Saves everything to SQLite.
    """
    item_name = request.form.get('name')
    category_id = request.form.get('category')

    if not item_name or category_id is None:
        flash("Please provide both an item name and a category.")
        return redirect(url_for('index'))

    try:
        category_id = int(category_id)
        # ML Prediction Step
        # 1 represents 'Fridge' as the default storage type for this logic
        predicted_days = predict_life(category_id, 1)

        # Mapping ID back to String for display
        categories = ["Fruit", "Dairy", "Meat"]
        category_name = categories[category_id]

        # Database Insertion
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO inventory (item_name, category, predicted_expiry) 
            VALUES (?, ?, ?)
        ''', (item_name, category_name, predicted_days))

        conn.commit()
        conn.close()

        flash(f"Successfully added {item_name}!")
    except Exception as e:
        flash(f"An error occurred: {e}")

    return redirect(url_for('index'))


@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    """Removes an item from the shelf."""
    conn = get_db_connection()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Ensure the database exists before starting the app
    if not os.path.exists(DATABASE):
        print("Database not found. Initializing...")
        from database import init_db

        init_db()

    app.run(debug=True, port=5000)