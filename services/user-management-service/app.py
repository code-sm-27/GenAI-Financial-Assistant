# services/user-management-service/app.py
from flask import Flask, request, jsonify
from models import register_user_in_db, get_user_by_email
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Basic health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "User Management Service is healthy"}), 200

@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Ensure email and password are required.
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # In a real system, password would be hashed securely (e.g., using bcrypt, Argon2)
    # password_hash = generate_password_hash(password)
    password_hash = f"hashed_{password}" # Placeholder for actual hashing for prototype

    try:
        user_data = register_user_in_db(email, password_hash)
        logging.info(f"User registered: {user_data['email']} with ID {user_data['user_id']}")
        return jsonify({"message": "User registered successfully", "user": user_data}), 201
    except ValueError as e:
        logging.warning(f"Registration failed: {e}")
        return jsonify({"error": str(e)}), 409 # Conflict, e.g., user already exists
    except Exception as e:
        logging.error(f"Internal error during registration: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Placeholder for user login (would involve password verification and token generation)
@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # In a real system: verify password_hash with provided password
    # For prototype, we're skipping actual password hash verification.
    # if check_password_hash(user['password_hash'], password):
    #     # On successful login, generate a JWT token
    #     token = generate_jwt_token(user['user_id'])
    #     return jsonify({"message": "Login successful", "user_id": user['user_id'], "token": token}), 200
    # else:
    #     return jsonify({"error": "Invalid credentials"}), 401

    # For now, just return success if user exists (simplistic for prototype)
    logging.info(f"User login attempt for: {email}")
    return jsonify({"message": "Login successful (prototype)", "user_id": user['user_id']}), 200


if __name__ == '__main__':
    # Running on a different port than API Gateway (5000) and Market Data Service (5001)
    app.run(host='0.0.0.0', port=5002)