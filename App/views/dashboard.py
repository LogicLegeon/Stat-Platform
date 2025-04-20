from flask import Blueprint, render_template, session, redirect, url_for

dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('auth_views.login'))  # Replace with your login view
    return render_template('dashboard.html')
