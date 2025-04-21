# App/views/dashboard.py
from flask import Blueprint, redirect, render_template, session, url_for
from App.models import Report, Entry
import json

dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('auth_views.index'))

    # --- Admin‐published Reports ---
    reports = Report.query.filter_by(is_public=True).all()
    report_data = []
    for rpt in reports:
        if not rpt.charts:
            continue
        chart = rpt.charts[0]
        cfg   = json.loads(chart.config_json)
        report_data.append({
            'id':          rpt.id,
            'title':       rpt.title,
            'description': rpt.dataset.description,
            'type':        chart.chart_type,
            'config':      cfg
        })

    # --- Published User Entries ---
    published_entries = Entry.query.filter_by(status='published').all()
    entry_labels = [e.label for e in published_entries]
    entry_values = [e.value for e in published_entries]

    return render_template(
        'dashboard.html',
        reports=report_data,
        published_entries=published_entries,
        entry_labels=entry_labels,
        entry_values=entry_values
    )

