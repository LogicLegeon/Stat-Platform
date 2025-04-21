from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from functools import wraps

from App.models import User
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


# ---------- ADMIN-ONLY DECORATOR ----------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Admins only!", "danger")
            return redirect(url_for('auth_views.dashboard'))
        
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash("Admins only!", "danger")
            return redirect(url_for('auth_views.dashboard'))

        return f(*args, **kwargs)
    return decorated_function


# ---------- INDEX (public landing page) ----------
@auth_views.route('/')
def index():
    return render_template('index.html')


# ---------- LOGIN ----------
@auth_views.route('/login', methods=['POST'])
def login_action():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login successful!')
    else:
        flash('Invalid username or password')
    
    return redirect(url_for('auth_views.dashboard'))


# ---------- LOGOUT ----------
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    session.clear()
    flash("👋 You have been logged out.")
    return redirect(url_for('auth_views.index'))


# ---------- DASHBOARD ----------
@auth_views.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        flash('Please log in to access the dashboard.')
        return redirect(url_for('auth_views.index'))

    return render_template('dashboard.html')
