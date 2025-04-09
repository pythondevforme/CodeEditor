from flask import Flask, request, jsonify, render_template
import mysql.connector
import random

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

@app.route('/')
def index():
    #return render_template('index.html')
    return open('C:\\Users\\1034493\\Office\\Python\\CodeEditor\\Randomquestions\\templates\\index.html').read()

@app.route('/get_questions', methods=['GET'])
def get_questions():
    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'})

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM questions ORDER BY RAND() LIMIT 1')
        questions = cursor.fetchall()
        return jsonify({'questions': questions})
    except mysql.connector.Error as error:
        print("Error fetching questions:", error)
        return jsonify({'error': 'Error fetching questions'})
    finally:
        if conn is not None:
            conn.close()

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    conn = connect_to_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'})

    try:
        question_id = request.json['question_id']
        answer = request.json['answer']

        cursor = conn.cursor()
        cursor.execute('SELECT correct_answer FROM questions WHERE id = %s', (question_id,))
        correct_answer = cursor.fetchone()[0]

        if answer == correct_answer:
            return jsonify({'message': 'Congratulations! Your answer is correct.'})
        else:
            return jsonify({'message': 'Incorrect answer. Try again.'})
    except mysql.connector.Error as error:
        print("Error submitting answer:", error)
        return jsonify({'error': 'Error submitting answer'})
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
