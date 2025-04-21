from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

# filepath: /Users/slintbot/Desktop/Stat-Platform/App/controllers/auth.py
from App.models.user import User
from werkzeug.security import check_password_hash

def login(username, password):
    """Validate user credentials and return the User object if valid."""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


# App/controllers/auth.py

from flask_jwt_extended import JWTManager

def setup_jwt(app):
    jwt = JWTManager(app)
    return jwt


  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  


# Context processor to make 'is_authenticated' available to all templates
from flask import session
from App.models import User

def add_auth_context(app):
  @app.context_processor
  def inject_user():
      user_id = session.get('user_id')
      current_user = User.query.get(user_id) if user_id else None
      return dict(
          is_authenticated=bool(user_id),
          current_user=current_user,
          username=session.get('username'),
          role=session.get('role')
      )
