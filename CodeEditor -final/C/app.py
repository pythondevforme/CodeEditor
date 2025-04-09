from flask import Flask, request, jsonify,render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return open('C:\\Users\\Office\\Python\\CodeEditor\\C\\templates\\index.html').read()
   
@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json['code']
    
    try:
        with open('temp.c', 'w') as f:
            f.write(code)
    except IOError:
        return "Error: Unable to write to file"
    
    try:
        result = subprocess.run(['gcc', 'temp.c', '-o', 'temp.out', '-Wall'], stderr=subprocess.PIPE)
        if result.returncode == 0:
            return "Compilation successful"
        else:
            return "Compilation error:\n" + result.stderr.decode('utf-8')
    except FileNotFoundError:
        return "Error: Unable to execute 'gcc' command"

if __name__ == '__main__':
    app.run(debug=True)
