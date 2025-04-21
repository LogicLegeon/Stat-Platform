from flask import Blueprint, render_template

dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')