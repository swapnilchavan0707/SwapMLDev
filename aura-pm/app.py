from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import os
import secrets
from db_manager import init_db, get_db_connection, log_telemetry
from preprocessor import prepare_features

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(24))

MODEL_PATH = 'ml_engine/models/rf_v1.pkl'


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


@app.route('/')
def index():
    model = load_model()
    conn = get_db_connection()
    machines = conn.execute('SELECT * FROM machines').fetchall()

    results = []
    for m in machines:
        # Fetch last 10 readings for the trend graph
        history_rows = conn.execute('''
            SELECT temperature, vibration, pressure 
            FROM telemetry WHERE machine_id = ? 
            ORDER BY timestamp DESC LIMIT 10
        ''', (m['id'],)).fetchall()

        # Reverse to show chronological order (left to right)
        history = history_rows[::-1]

        prediction = "N/A"
        temp_data = [h['temperature'] for h in history]
        vib_data = [h['vibration'] for h in history]

        if history and model:
            # Use the very latest point for the ML prediction
            latest = dict(history[-1])
            features = prepare_features([latest])
            prediction = round(model.predict(features)[0], 1)

        results.append({
            'id': m['id'],
            'name': m['name'],
            'model': m['model'],
            'status': m['status'],
            'prediction': prediction,
            'temp_history': temp_data,
            'vib_history': vib_data
        })

    conn.close()
    return render_template('index.html', machines=results)


@app.route('/add_machine', methods=['POST'])
def add_machine():
    name, model_type = request.form['name'], request.form['model']
    conn = get_db_connection()
    conn.execute('INSERT INTO machines (name, model) VALUES (?, ?)', (name, model_type))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update_sensor/<int:id>', methods=['POST'])
def update_sensor(id):
    try:
        t, v, p = float(request.form['temp']), float(request.form['vib']), float(request.form['press'])
        log_telemetry(id, t, v, p)
        flash(f"Telemetry Archive Updated for Asset #{id}")
    except ValueError:
        flash("Invalid numerical input.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)