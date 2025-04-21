# App/main.py

import os
from flask import Flask, render_template, jsonify
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from App.database import init_db       # your function that does db.init_app + migrate.init_app
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import views, setup_admin
from App.models.user import User       # for context processor

def create_app(overrides={}):
    # 1) create & configure
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)

    # 2) auth context (puts token in requests, etc.)
    add_auth_context(app)

    # 3) file uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    # 4) register blueprints (all your views)
    for bp in views:
        app.register_blueprint(bp)

    # 5) database + migrations
    init_db(app)

    # 6) JWT setup (registers token callbacks, cookie settings)
    jwt = setup_jwt(app)

    # 7) admin setup
    setup_admin(app)

    # 8) CLI commands (init‑db, user, test, etc.)
    from App.commands import init_app as register_commands
    register_commands(app)

    # 9) custom unauthorized response for JWT
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return jsonify({"error": "Unauthorized", "message": error}), 401

    # 10) inject current_user and flags into all templates
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                raise RuntimeError("User not found")
            return {
                'is_authenticated': True,
                'username': user.username,
                'current_user': user,
            }
        except Exception:
            return {
                'is_authenticated': False,
                'username': None,
                'current_user': None,
            }

    return app
