import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load fire brigade data
with open('fire_brigades_info.json', 'r', encoding='utf-8') as file:
    fire_brigades = json.load(file)

@app.route('/')
def index():
    return render_template('index.html', brigades=fire_brigades)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = [
        brigade for brigade in fire_brigades
        if query in brigade['Name'].lower() or query in brigade.get('Alias', '').lower()
    ]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
