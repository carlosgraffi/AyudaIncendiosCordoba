import json
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import CSRFError

app = Flask(__name__)
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)

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
    approved_events = [event for event in donation_events if event.get('status') == 'approved']
    return render_template('index.html', brigades=fire_brigades, donation_events=approved_events)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = [
        brigade for brigade in fire_brigades
        if query in brigade['Name'].lower() or query in brigade.get('Alias', '').lower()
    ]
    return jsonify(results)

@app.route('/submit_brigade', methods=['GET', 'POST'])
@csrf.exempt  # Temporarily disable CSRF protection for this route
def submit_brigade():
    if request.method == 'POST':
        try:
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
        except Exception as e:
            app.logger.error(f"Error submitting brigade: {str(e)}")
            flash('An error occurred while submitting the brigade', 'error')
            return redirect(url_for('submit_brigade'))
    
    # Print CSRF token value for debugging
    csrf_token = csrf._get_token()
    print(f"CSRF Token: {csrf_token}")
    
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
            'link': request.form.get('link'),
            'status': 'pending'
        }
        donation_events.append(new_event)
        with open(donation_events_file, 'w', encoding='utf-8') as file:
            json.dump(donation_events, file, ensure_ascii=False, indent=4)
        flash('Donation event submission successful! Waiting for admin approval.', 'success')
        return redirect(url_for('index'))
    return render_template('submit_event.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    pending_events = [event for event in donation_events if event.get('status') == 'pending']
    approved_events = [event for event in donation_events if event.get('status') == 'approved']
    return render_template('admin.html', brigades=fire_brigades, pending_events=pending_events, approved_events=approved_events)

@app.route('/admin/approve_event/<int:event_index>', methods=['POST'])
@csrf.exempt
def approve_event(event_index):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    try:
        if 0 <= event_index < len(donation_events):
            donation_events[event_index]['status'] = 'approved'
            with open(donation_events_file, 'w', encoding='utf-8') as file:
                json.dump(donation_events, file, ensure_ascii=False, indent=4)
            flash('Event approved successfully', 'success')
        else:
            flash('Invalid event index', 'error')
    except Exception as e:
        app.logger.error(f"Error approving event: {str(e)}")
        flash('An error occurred while approving the event', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_event/<int:event_index>', methods=['POST'])
@csrf.exempt
def reject_event(event_index):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    try:
        if 0 <= event_index < len(donation_events):
            donation_events.pop(event_index)
            with open(donation_events_file, 'w', encoding='utf-8') as file:
                json.dump(donation_events, file, ensure_ascii=False, indent=4)
            flash('Event rejected and removed', 'success')
        else:
            flash('Invalid event index', 'error')
    except Exception as e:
        app.logger.error(f"Error rejecting event: {str(e)}")
        flash('An error occurred while rejecting the event', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    app.logger.error(f"CSRF Error: {str(e)}")
    return render_template('csrf_error.html', reason=e.description), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
