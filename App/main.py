import os
from flask import Flask, render_template, jsonify
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request
from App.database import init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import views, setup_admin
from App.models.user import User

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)

    # Configure file uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    # Register blueprints
    add_views(app)

    # Initialize database
    init_db(app)

    # Setup JWT
    jwt = setup_jwt(app)

    # Setup admin functionality
    setup_admin(app)

    # Custom unauthorized response for JWT
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return jsonify({"error": "Unauthorized access", "message": error}), 401

    # Context processor to inject user data from JWT
    @app.context_processor
    def inject_user():
        try:
            # Verify JWT and get user identity
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)

            if not current_user:
                raise Exception("User not found")

            return {
                'is_authenticated': True,
                'current_user': current_user,
                'username': current_user.username
            }
        except Exception as e:
            # Log the error for debugging
            print(f"JWT Error: {e}")
            return {
                'is_authenticated': False,
                'current_user': None,
                'username': None
            }

    return app