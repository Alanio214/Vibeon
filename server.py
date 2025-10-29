from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secretkeywhoknownhesbadexeptalanio'

# Путь к файлу пользователей
USERS_FILE = os.path.join('account-system', 'users.txt')

# Создаём файл, если его нет
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, 'w').close()

def load_users():
    users = {}
    with open(USERS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            username, pw_hash = line.split(':')
            users[username] = pw_hash
    return users

def save_user(username, pw_hash):
    with open(USERS_FILE, 'a') as f:
        f.write(f'{username}:{pw_hash}\n')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error':'Введите логин и пароль'}), 400
    users = load_users()
    if username in users:
        return jsonify({'error':'Пользователь уже существует'}), 400
    pw_hash = generate_password_hash(password)
    save_user(username, pw_hash)
    return jsonify({'success':True, 'message':'Регистрация успешна!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    users = load_users()
    pw_hash = users.get(username)
    if pw_hash and check_password_hash(pw_hash, password):
        session['username'] = username
        return jsonify({'success':True})
    else:
        return jsonify({'error':'Неверный логин или пароль'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'success':True})

@app.route('/api/me')
def me():
    if 'username' in session:
        return jsonify({'loggedIn': True, 'username': session['username']})
    else:
        return jsonify({'loggedIn': False})

# Отдаём HTML-файлы
@app.route('/auth.html')
def auth_page():
    return send_from_directory('.', 'auth.html')

@app.route('/register.html')
def register_page():
    return send_from_directory('.', 'register.html')

@app.route('/index.html')
def index_page():
    return send_from_directory('.', 'index.html')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
