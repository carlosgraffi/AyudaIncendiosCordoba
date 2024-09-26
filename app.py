import json
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load fire brigade data
with open('fire_brigades_info.json', 'r', encoding='utf-8') as file:
    fire_brigades = json.load(file)

# Load donation events data
donation_events_file = 'donation_events.json'
if os.path.exists(donation_events_file):
    with open(donation_events_file, 'r', encoding='utf-8') as file:
        donation_events = json.load(file)
else:
    donation_events = []

# Admin credentials (in a real application, use a database and proper authentication)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@app.route('/')
def index():
    return render_template('index.html', brigades=fire_brigades, donation_events=donation_events)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = [
        brigade for brigade in fire_brigades
        if query in brigade['Name'].lower() or query in brigade.get('Alias', '').lower()
    ]
    return jsonify(results)

@app.route('/submit_brigade', methods=['GET', 'POST'])
def submit_brigade():
    if request.method == 'POST':
        new_brigade = {
            'Name': request.form.get('name'),
            'Alias': request.form.get('alias'),
            'Phone Number': request.form.get('phone'),
            'Instagram': request.form.get('instagram'),
            'Facebook': request.form.get('facebook')
        }
        fire_brigades.append(new_brigade)
        with open('fire_brigades_info.json', 'w', encoding='utf-8') as file:
            json.dump(fire_brigades, file, ensure_ascii=False, indent=4)
        flash('Brigade submission successful!', 'success')
        return redirect(url_for('index'))
    return render_template('submit_brigade.html')

@app.route('/submit_event', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
        new_event = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'phone_number': request.form.get('phone_number'),
            'location': request.form.get('location'),
            'instagram': request.form.get('instagram'),
            'link': request.form.get('link')
        }
        donation_events.append(new_event)
        with open(donation_events_file, 'w', encoding='utf-8') as file:
            json.dump(donation_events, file, ensure_ascii=False, indent=4)
        flash('Donation event submission successful!', 'success')
        return redirect(url_for('index'))
    return render_template('submit_event.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
