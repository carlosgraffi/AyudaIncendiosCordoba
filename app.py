import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Load fire brigade data
with open('fire_brigades_info.json', 'r', encoding='utf-8') as file:
    fire_brigades = json.load(file)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin_password':
            user = User(1)
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', brigades=fire_brigades)

@app.route('/admin/edit/<int:brigade_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_brigade(brigade_id):
    brigade = fire_brigades[brigade_id]
    if request.method == 'POST':
        brigade['Name'] = request.form.get('name')
        brigade['Alias'] = request.form.get('alias')
        brigade['Phone Number'] = request.form.get('phone_number')
        brigade['Instagram'] = request.form.get('instagram')
        brigade['Facebook'] = request.form.get('facebook')
        
        with open('fire_brigades_info.json', 'w', encoding='utf-8') as file:
            json.dump(fire_brigades, file, indent=4, ensure_ascii=False)
        
        flash('Brigade information updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_brigade.html', brigade=brigade, brigade_id=brigade_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
