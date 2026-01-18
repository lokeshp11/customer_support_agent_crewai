import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/users.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Table
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            email TEXT,
            address TEXT,
            phone TEXT,
            service_opted TEXT,
            plan TEXT,
            start_date TEXT,
            end_date TEXT,
            monthly_cost REAL,
            dues REAL,
            next_billing_date TEXT,
            billing_cycle TEXT
        )
    ''')
    
    # Seed Data
    users = [
        (
            'John Doe', 'john.doe@example.com', '123 Pulse Ave, Tech City', '555-0101', 
            'Broadband', 'Pulse GigaFiber', '2025-01-01', '2026-01-01', 
            99.99, 0.0, '2025-02-01', 'Monthly'
        ),
        (
            'Jane Smith', 'jane.smith@example.com', '456 Signal St, Data Town', '555-0102', 
            'Mobile', 'Pulse Unlimited 5G', '2024-06-15', '2025-06-15', 
            49.99, 49.99, '2025-02-15', 'Monthly'
        ),
        (
            'Bob Jones', 'bob.jones@example.com', '789 Node Rd, Server Valley', '555-0103', 
            'Broadband', 'Pulse Home Basic', '2023-11-20', '2024-11-20', 
            39.99, 120.00, '2024-12-20', 'Monthly'
        )
    ]
    
    cursor.executemany('''
        INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    ''', users)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH} with {len(users)} users.")

if __name__ == "__main__":
    init_db()
