from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = User.query.filter_by(username=identity).one_or_none()
    if user:
        return user.id
    return None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

  return jwt


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
