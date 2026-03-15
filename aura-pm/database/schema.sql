-- Table for hardware assets
CREATE TABLE machines (
    id INTEGER PRIMARY KEY,
    model_type TEXT,
    install_date DATE,
    status TEXT -- 'Active', 'Maintenance Required', 'Failed'
);

-- Table for real-time sensor readings
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER,
    timestamp TIMESTAMP,
    temperature FLOAT,
    vibration_frequency FLOAT,
    pressure FLOAT,
    FOREIGN KEY (machine_id) REFERENCES machines(id)
);