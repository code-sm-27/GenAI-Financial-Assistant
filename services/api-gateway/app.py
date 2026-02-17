import os, re, time, requests, logging, jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# FIX 1: Use a 32-byte (256-bit) key to satisfy RFC 7518
app.config['SECRET_KEY'] = 'finsense_ultra_secure_production_key_32_chars_long!!'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://shivamani:password123@db:5432/finsense_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    __tablename__ = 'app_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Interaction(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'), nullable=False)
    query = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- CRITICAL FIX: FORCE DB INIT ---
def force_initialize_database():
    """Blocks execution until the database tables are confirmed to exist."""
    print("--- WAITING FOR DATABASE CONNECTION ---")
    with app.app_context():
        for attempt in range(30):  # Try for 30 seconds
            try:
                # 1. Try to create tables
                db.create_all()
                # 2. VERIFY they exist by selecting from them
                db.session.execute(db.text("SELECT 1 FROM app_users LIMIT 1"))
                db.session.commit()
                print("--- SUCCESS: DATABASE TABLES VERIFIED ---")
                return
            except Exception as e:
                print(f"Database not ready... retrying ({attempt+1}/30)")
                time.sleep(2)
        print("--- CRITICAL ERROR: COULD NOT CREATE TABLES ---")
        exit(1)

# Run this IMMEDIATELY when the file loads
force_initialize_database()

# --- ROUTES ---
@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Check if user exists
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({"error": "Username already taken"}), 400
        
        hashed = generate_password_hash(data.get('password'), method='pbkdf2:sha256')
        new_user = User(username=data.get('username'), password=hashed)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    try:
        user = User.query.filter_by(username=data.get('username')).first()
        if user and check_password_hash(user.password, data.get('password')):
            token = jwt.encode({
                'u_id': user.id, 
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token})
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    token = request.headers.get('Authorization')
    if not token: return jsonify({"error": "No token"}), 401
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        u_id = payload['u_id']
        
        # FIX 2: Verify user exists in current DB before proceeding
        user = db.session.get(User, u_id)
        if not user:
            return jsonify({"error": "User session invalid. Please re-login."}), 401

        data = request.json
        # Call AI Service
        ai_res = requests.post("http://genai-inference-service:5003/generate", 
                               json={"user_query": data['query'], "task": "chat"}, timeout=30)
        advice = ai_res.json().get('advice')

        # Save with verified u_id
        db.session.add(Interaction(user_id=u_id, query=data['query'], response=advice))
        db.session.commit()
        return jsonify({"advice": advice})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Session expired or invalid"}), 401
    
@app.route('/')
def home(): return render_template('index.html')

@app.route('/login')
def login_page(): return render_template('login.html')

@app.route('/register')
def register_page(): return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)