import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="gym_db"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def setup_tables():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Members (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS WorkoutSessions (
                    session_id INT AUTO_INCREMENT PRIMARY KEY,
                    member_id INT NOT NULL,
                    date DATE NOT NULL,
                    duration_minutes INT NOT NULL,
                    calories_burned INT NOT NULL,
                    FOREIGN KEY (member_id) REFERENCES Members (id)
                )
                """
            )
            conn.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error setting up tables: {e}")
        finally:
            conn.close()

def add_member(member_id, name, age):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)",
                (member_id, name, age)
            )
            conn.commit()
            print("Member added successfully.")
        except Error as e:
            print(f"Error adding member: {e}")
        finally:
            conn.close()

def add_workout_session(member_id, date, duration_minutes, calories_burned):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO WorkoutSessions (member_id, date, duration_minutes, calories_burned)
                VALUES (%s, %s, %s, %s)
                """,
                (member_id, date, duration_minutes, calories_burned)
            )
            conn.commit()
            print("Workout session added successfully.")
        except Error as e:
            print(f"Error adding workout session: {e}")
        finally:
            conn.close()

def update_member_age(member_id, new_age):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Members SET age = %s WHERE id = %s",
                (new_age, member_id)
            )
            if cursor.rowcount > 0:
                conn.commit()
                print("Member age updated successfully.")
            else:
                print("Member not found.")
        except Error as e:
            print(f"Error updating member age: {e}")
        finally:
            conn.close()

def delete_workout_session(session_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            if cursor.rowcount > 0:
                conn.commit()
                print("Workout session deleted successfully.")
            else:
                print("Workout session not found.")
        except Error as e:
            print(f"Error deleting workout session: {e}")
        finally:
            conn.close()

def get_members_in_age_range(start_age, end_age):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Members WHERE age BETWEEN %s AND %s",
                (start_age, end_age)
            )
            members = cursor.fetchall()
            print("Members in age range:", members)
            return members
        except Error as e:
            print(f"Error retrieving members in age range: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    setup_tables()
    add_member(1, 'Alice', 30)
    add_member(2, 'Bob', 25)
    add_workout_session(1, '2024-11-01', 60, 300)
    add_workout_session(2, '2024-11-02', 45, 250)
    update_member_age(1, 31)
    delete_workout_session(1)
    get_members_in_age_range(25, 30)
