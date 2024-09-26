import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Load fire brigade data
with open('fire_brigades_info.json', 'r', encoding='utf-8') as file:
    fire_brigades = json.load(file)

# Admin credentials (in a real application, use a database and proper authentication)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = generate_password_hash('admin123')

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD, password):
            return render_template('admin.html', brigades=fire_brigades)
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')

@app.route('/update_brigade', methods=['POST'])
def update_brigade():
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
    
    return redirect(url_for('admin'))

@app.route('/add_brigade', methods=['POST'])
def add_brigade():
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
    
    return redirect(url_for('admin'))

@app.route('/delete_brigade', methods=['POST'])
def delete_brigade():
    brigade_name = request.form.get('name')
    global fire_brigades
    fire_brigades = [brigade for brigade in fire_brigades if brigade['Name'] != brigade_name]
    
    with open('fire_brigades_info.json', 'w', encoding='utf-8') as file:
        json.dump(fire_brigades, file, ensure_ascii=False, indent=4)
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
