# services/user-management-service/models.py
import uuid
import datetime

# A very simplistic in-memory user store for demonstration purposes
# In a real application, this would be a secure database (e.g., PostgreSQL, Spanner)
USERS_DB = {} # {user_id: {email, password_hash, registration_date}}

class User:
    def __init__(self, email, password_hash):
        self.user_id = str(uuid.uuid4()) # Generate a unique ID for the user
        self.email = email
        self.password_hash = password_hash # In production, use strong hashing (e.g., bcrypt)
        self.registration_date = datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "registration_date": self.registration_date
            # NEVER return password_hash in API responses
        }

def register_user_in_db(email, password_hash):
    """Registers a new user in the in-memory database."""
    if email in [user['email'] for user in USERS_DB.values()]:
        raise ValueError("User with this email already exists.")
    
    user = User(email, password_hash)
    USERS_DB[user.user_id] = user.to_dict() # Store the dict representation, excluding hash
    # For actual authentication, you'd store the hash separately with the user ID
    # and verify it upon login.
    return user.to_dict()

def get_user_by_email(email):
    """Retrieves a user by email from the in-memory database."""
    for user_id, user_data in USERS_DB.items():
        if user_data['email'] == email:
            return user_data
    return None

# Example usage (for testing models directly)
if __name__ == '__main__':
    try:
        print("Registering user1...")
        user1 = register_user_in_db("user1@example.com", "hashed_password_1")
        print("Registered:", user1)

        print("\nAttempting to register user1 again...")
        try:
            register_user_in_db("user1@example.com", "another_hash")
        except ValueError as e:
            print(f"Error: {e}")

        print("\nRetrieving user by email...")
        retrieved_user = get_user_by_email("user1@example.com")
        print("Retrieved:", retrieved_user)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")