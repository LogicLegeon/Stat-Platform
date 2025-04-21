# App/views/admin.py

import json
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.models import Entry, Dataset
from App.controllers.admin import create_report
from App.database import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from App.controllers.admin import (
    list_datasets, create_dataset, set_dataset_status,
    create_report, list_reports, toggle_report_public
)
from App.models.user import Dataset, Entry

admin = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='../templates/admin'
)

@admin.route('/')
@jwt_required()
def dashboard():
    pending  = list_datasets(status='pending')
    approved = list_datasets(status='approved')
    reports  = list_reports()
    return render_template(
        'admin/dashboard.html',
        pending=pending,
        approved=approved,
        reports=reports
    )

@admin.route('/upload', methods=['GET','POST'])
@jwt_required()
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file  = request.files['file']
        create_dataset(title, file, current_user.id)
        flash('Dataset uploaded, pending review', 'success')
        return redirect(url_for('admin.upload'))
    return render_template('admin/upload.html')

@admin.route('/dataset/<int:ds_id>/<action>')
@jwt_required()
def review_dataset(ds_id, action):
    if action not in ('approved','rejected'):
        flash('Invalid action', 'error')
    else:
        set_dataset_status(ds_id, action)
        flash(f'Dataset {action}', 'info')
    return redirect(url_for('admin.dashboard'))

@admin.route('/dataset/<int:ds_id>/customize', methods=['GET','POST'])
@jwt_required()
def customize(ds_id):
    # fetch the dataset or 404
    from App.models.user import Dataset
    ds = Dataset.query.get_or_404(ds_id)

    # only approved datasets may be customized
    if ds.status != 'approved':
        flash('You can only customize an approved dataset.', 'warning')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        title = request.form['report_title']

        # build chart configs from the form
        charts_cfg = []
        # here we only handle one chart (#1); extend this loop for more
        ctype   = request.form['chart_type_1']
        ctitle  = request.form['chart_title_1']
        cconfig = request.form['chart_config_1']

        # validate JSON
        import json
        try:
            json.loads(cconfig)
        except json.JSONDecodeError:
            flash('Invalid JSON in chart data.', 'error')
            return redirect(request.url)

        charts_cfg.append({
            'type':        ctype,
            'title':       ctitle,
            'config_json': cconfig
        })

        rpt = create_report(ds_id, title, charts_cfg, current_user.id)
        flash(f'Report "{rpt.title}" created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/customize.html', dataset=ds)

@admin.route('/report/<int:rid>/toggle')
@jwt_required()
def toggle_report(rid):
    rpt = toggle_report_public(rid)
    state = "published" if rpt.is_public else "unpublished"
    flash(f'Report {state}', 'info')
    return redirect(url_for('admin.dashboard'))


def setup_admin(app):
    """Register the admin blueprint on the Flask app."""
    app.register_blueprint(admin)

@admin.route('/publish-entries', methods=['GET', 'POST'])
@jwt_required()
def publish_entries():
    # Only admins should hit this — re‑use your admin_required decorator if you have one
    user_id = get_jwt_identity()

    # Fetch all user‑submitted entries
    entries = Entry.query.all()

    if request.method == 'POST':
        chart_type  = request.form['chart_type']
        title       = request.form['title']
        description = request.form['description']

        # Build chart data
        labels = [e.label for e in entries]
        values = [e.value for e in entries]
        cfg = {
          'labels': labels,
          'datasets': [{
            'label': title,
            'data': values
          }]
        }

        # 1️⃣ Create a Dataset record for this report
        ds = Dataset(
          title=title,
          description=description,
          upload_type='manual',
          uploaded_by=user_id
        )
        db.session.add(ds)
        db.session.commit()

        # 2️⃣ Use your existing admin controller to make the report+chart
        charts_cfg = [{
          'type':        chart_type,
          'title':       title,
          'config_json': json.dumps(cfg)
        }]
        rpt = create_report(ds.id, title, charts_cfg, user_id)

        flash(f"📊 Report “{rpt.title}” published!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/publish_entries.html', entries=entries)

from App.models.user import Entry
from App.database import db

@admin.route('/review-entries')
@jwt_required()
def review_entries():
    """Show all entries waiting for approval."""
    entries = Entry.query.filter_by(status='pending').all()
    return render_template('admin/review_entries.html', entries=entries)

@admin.route('/review-entries/<int:eid>/publish', methods=['POST'])
@jwt_required()
def publish_entry(eid):
    e = Entry.query.get_or_404(eid)
    e.status = 'published'
    db.session.commit()
    flash("✅ Entry published.", "success")
    return redirect(url_for('admin.review_entries'))

@admin.route('/review-entries/<int:eid>/delete', methods=['POST'])
@jwt_required()
def delete_entry(eid):
    e = Entry.query.get_or_404(eid)
    db.session.delete(e)
    db.session.commit()
    flash("🗑️ Entry deleted.", "info")
    return redirect(url_for('admin.review_entries'))
