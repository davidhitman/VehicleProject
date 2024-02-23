import sqlite3

# Step 1: Create a SQLite3 database and connect to it
conn = sqlite3.connect("nextbike.db")
cursor = conn.cursor()

# Step 2: Define the schema for the "charge_vehicle" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS charge_vehicle (
        operator INTEGER,
        battery_count INTEGER
    )
''')

# Step 3: Fetch operator IDs from the "user_details" table where "role_type" is "Operator"
cursor.execute("SELECT user_id FROM user_details WHERE role_type = 'Operator'")
operator_ids = cursor.fetchall()

# Step 4: Insert the operator IDs and battery counts into the "charge_vehicle" table
battery_counts = [5, 10, 7]  # You can modify this list as needed

for operator_id in operator_ids:
    battery_count = battery_counts.pop(0) if battery_counts else 0
    cursor.execute("INSERT INTO charge_vehicle (operator, battery_count) VALUES (?, ?)", (operator_id[0], battery_count))

# Commit the changes and close the database connection
conn.commit()
conn.close()
