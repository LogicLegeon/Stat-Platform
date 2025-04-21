from flask import Blueprint, redirect, render_template, session, url_for

from App.models import Entry

# Blueprint for user dashboard views
# Shows only published entries

dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard')
def dashboard():
    # Ensure user is logged in
    if not session.get('user_id'):
        return redirect(url_for('auth_views.index'))

    # Fetch only entries that have been published by admin
    published_entries = Entry.query.filter_by(status='published').all()
    return render_template('dashboard.html', published_entries=published_entries)
