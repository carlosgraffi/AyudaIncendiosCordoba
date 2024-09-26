import os
import json
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

def load_brigades():
    with open('static/data/brigades.json', 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/brigades')
def get_brigades():
    brigades = load_brigades()
    for brigade in brigades:
        # Convert date strings to Argentinian format
        brigade['fecha_actualizacion'] = datetime.strptime(brigade['fecha_actualizacion'], '%Y-%m-%d').strftime('%d/%m/%Y')
    return jsonify(brigades)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
