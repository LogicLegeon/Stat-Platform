# App/views/auth_views.py

from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, jsonify
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)
from App.controllers.auth import login as auth_login
from App.models.user import User

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


def admin_required(fn):
    """Decorator: only allow users with is_admin=True"""
    @jwt_required()
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not getattr(user, 'is_admin', False):
            flash("Admins only!", "danger")
            return redirect(url_for('auth_views.dashboard'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


@auth_views.route('/', methods=['GET'])
def index():
    """Public landing / login prompt."""
    return render_template('index.html')


@auth_views.route('/login', methods=['POST'])
def login_action():
    """
    Handles both form POSTs and JSON POSTs.
    - Form POST -> redirect to dashboard.
    - JSON POST -> return JSON response.
    """
    # 1) Grab credentials from either form or JSON
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    # 2) Ensure username and password are provided
    if not username or not password:
        if request.is_json:
            return jsonify({"error": "Username and password are required"}), 400
        flash("Username and password are required", "danger")
        return redirect(url_for('auth_views.index'))

    # 3) Validate credentials and generate token
    user = auth_login(username, password)
    if not user:
        if request.is_json:
            return jsonify({"error": "Invalid username or password"}), 401
        flash('Invalid username or password', 'danger')
        return redirect(url_for('auth_views.index'))

    # 4) Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    # 5) Build the response: JSON for API, redirect for form
    if request.is_json:
        resp = jsonify({"message": "Login successful", "access_token": access_token})
    else:
        resp = redirect(url_for('dashboard_views.dashboard'))
        flash('Login successful', 'success')

    # 6) Set the JWT token in a cookie
    set_access_cookies(resp, access_token)
    return resp