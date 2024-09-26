import json
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

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
ADMIN_PASSWORD = generate_password_hash('admin123')

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD, password):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('admin'):
        return render_template('admin.html', brigades=fire_brigades, donation_events=donation_events)
    return redirect(url_for('admin'))

@app.route('/update_brigade', methods=['POST'])
def update_brigade():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    brigade_name = request.form.get('name')
    for brigade in fire_brigades:
        if brigade['Name'] == brigade_name:
            brigade['Alias'] = request.form.get('alias')
            brigade['Phone Number'] = request.form.get('phone')
            brigade['Instagram'] = request.form.get('instagram')
            brigade['Facebook'] = request.form.get('facebook')
            break
    
    with open('fire_brigades_info.json', 'w', encoding='utf-8') as file:
        json.dump(fire_brigades, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/add_brigade', methods=['POST'])
def add_brigade():
    if not session.get('admin'):
        return redirect(url_for('admin'))
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
    
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_brigade', methods=['POST'])
def delete_brigade():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    brigade_name = request.form.get('name')
    global fire_brigades
    fire_brigades = [brigade for brigade in fire_brigades if brigade['Name'] != brigade_name]
    
    with open('fire_brigades_info.json', 'w', encoding='utf-8') as file:
        json.dump(fire_brigades, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/add_event', methods=['POST'])
def add_event():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    new_event = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'phone_number': request.form.get('phone_number'),
        'location': request.form.get('location'),
        'instagram': request.form.get('instagram')
    }
    donation_events.append(new_event)
    
    with open(donation_events_file, 'w', encoding='utf-8') as file:
        json.dump(donation_events, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/update_event', methods=['POST'])
def update_event():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    event_name = request.form.get('name')
    for event in donation_events:
        if event['name'] == event_name:
            event['description'] = request.form.get('description')
            event['phone_number'] = request.form.get('phone_number')
            event['location'] = request.form.get('location')
            event['instagram'] = request.form.get('instagram')
            break
    
    with open(donation_events_file, 'w', encoding='utf-8') as file:
        json.dump(donation_events, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    event_name = request.form.get('name')
    global donation_events
    donation_events = [event for event in donation_events if event['name'] != event_name]
    
    with open(donation_events_file, 'w', encoding='utf-8') as file:
        json.dump(donation_events, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
