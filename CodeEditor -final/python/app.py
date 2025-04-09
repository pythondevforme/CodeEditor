from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return open('C:\\Users\\Office\\Python\\CodeEditor\\python\\templates\\index.html').read()

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json['code']
    try:
        result = subprocess.run(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
        else:
            return "Error:\n" + result.stderr.decode('utf-8')
    except FileNotFoundError:
        return "Error: Unable to execute 'python' command"

if __name__ == '__main__':
    app.run(debug=True)
