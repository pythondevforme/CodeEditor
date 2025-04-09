from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database connection parameters
DB_USER = 'test'
DB_PASSWORD = 'test'
DB_HOST = 'localhost'
DB_DATABASE = 'test'

# Function to establish database connection
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_DATABASE
        )
        return conn
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

# Serve the frontend HTML file
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to execute SQL queries
@app.route('/execute', methods=['POST'])
def execute_query():
    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'})

    query = request.json['query']
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'result': result})
    except mysql.connector.Error as error:
        print("Error executing query:", error)
        return jsonify({'error': str(error)})
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
