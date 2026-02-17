import os, time, requests, logging, jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'finsense_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@db:5432/finsense_db')
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

# --- Helper Function ---
def setup_database():
    """Retries DB connection until successful."""
    with app.app_context():
        retries = 10
        while retries > 0:
            try:
                print("--- WAITING FOR DATABASE CONNECTION ---")
                db.create_all()
                print("--- SUCCESS: DATABASE TABLES VERIFIED ---")
                return
            except Exception as e:
                print(f"Database not ready yet... Retrying ({retries} left)")
                print(e)
                time.sleep(5)
                retries -= 1
        print("!!! CRITICAL: COULD NOT CONNECT TO DATABASE !!!")

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@app.route('/api/v1/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data.get('username')).first()
        if user and check_password_hash(user.password, data.get('password')):
            token = jwt.encode({
                'u_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({"token": token})
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"Login Error: {e}")
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    token = request.headers.get('Authorization')
    if not token: return jsonify({"error": "No token"}), 401
    
    try:
        # 1. Verify Token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        u_id = payload['u_id']
        
        # 2. Get Data
        data = request.json
        user_query = data.get('query')

        # 3. Connect to AI Service (FIXED LOGIC)
        # Use the Environment Variable, NOT the hardcoded URL
        genai_url = os.getenv('GENAI_SERVICE_URL')
        
        if not genai_url:
            logger.error("GENAI_SERVICE_URL environment variable is missing!")
            return jsonify({"advice": "System Error: AI Service URL not configured."})

        # Ensure no trailing slash issues
        genai_url = genai_url.rstrip('/') 

        # Call the AI
        try:
            logger.info(f"Connecting to AI Service at: {genai_url}/generate")
            ai_res = requests.post(f"{genai_url}/generate", 
                                  json={"user_query": user_query, "task": "chat"}, 
                                  timeout=30)
            
            # Check if we got JSON back (or HTML error page)
            try:
                ai_data = ai_res.json()
                advice = ai_data.get('advice', "No advice returned.")
            except ValueError:
                logger.error(f"AI Service returned non-JSON: {ai_res.text[:100]}")
                advice = "Error: AI Service returned an invalid response."

        except Exception as e:
            logger.error(f"Failed to connect to AI Service: {e}")
            advice = "I am currently unable to reach the AI engine. Please try again later."

        # 4. Save Interaction
        db.session.add(Interaction(user_id=u_id, query=user_query, response=advice))
        db.session.commit()
        
        return jsonify({"advice": advice})
        
    except Exception as e:
        logger.error(f"Chat Route Error: {e}")
        return jsonify({"error": "Session invalid or server error"}), 401

# --- Execution Entry Point ---
if __name__ == '__main__':
    setup_database()  # This now matches the function name above
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)