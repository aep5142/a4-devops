from flask import Flask, request
import os
from dotenv import load_dotenv
import mysql.connector

# Loading the .env file
load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = int(os.getenv("DB_PORT", 3306))

app = Flask(__name__)

def init_db():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                todo VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"DB init error: {err}")

@app.route("/add")
def add_records():
    to_add = request.args.get("to_add_item")
    if not to_add:
        return "Error: no todo item provided", 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        cursor = conn.cursor()
        
        sql = "INSERT INTO todo_table (todo) VALUES (%s)"
        values = (to_add,)
        cursor.execute(sql, values)
         # Commit changes
        conn.commit()

        cursor.close()
        conn.close()

        return f"Added {to_add} successfully to the to-do list"

    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route("/delete")
def delete_records():
    # Get the item to delete from the query parameter
    to_delete = request.args.get("to_delete_item")
    if not to_delete:
        return "Error: no todo item provided", 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        cursor = conn.cursor()

        # Use parameterized query to delete the item safely
        sql = "DELETE FROM todo_table WHERE todo = %s"
        cursor.execute(sql, (to_delete,))

        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()

        # Check if anything was actually deleted
        if cursor.rowcount == 0:
            return f"No record found matching '{to_delete}'"
        return f"Deleted {to_delete} successfully from the to-do list"

    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route("/view")
def view_records():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, todo FROM todo_table")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        todos = [r[1] for r in results]
        return todos

    except mysql.connector.Error as err:
        return f"Error: {err}"


if __name__ == "__main__":
    # Call once at startup
    init_db()
    app.run(host="0.0.0.0", port=5000)


# LLM's references:
# I used ChatGPT to do the command of creating first table, and then the
# instructions on how to view, add and delete items from the db