# App/controllers/admin.py

import json
from werkzeug.utils import secure_filename
from App.database import db
from App.models.user import Dataset, Report, Chart

UPLOAD_FOLDER = 'App/uploads'

def save_uploaded_file(uploaded_file):
    filename = secure_filename(uploaded_file.filename)
    path = f"{UPLOAD_FOLDER}/{filename}"
    uploaded_file.save(path)
    return filename

def create_dataset(title, uploaded_file, user_id):
    fn = save_uploaded_file(uploaded_file)
    ds = Dataset(title=title, filename=fn, uploaded_by=user_id, status='pending')
    db.session.add(ds)
    db.session.commit()
    return ds

def list_datasets(status=None):
    q = Dataset.query
    if status:
        q = q.filter_by(status=status)
    return q.all()

def set_dataset_status(dataset_id, new_status):
    ds = Dataset.query.get_or_404(dataset_id)
    ds.status = new_status
    db.session.commit()
    return ds

def create_report(dataset_id, title, charts_config, user_id):
    rpt = Report(
        title=title,
        dataset_id=dataset_id,
        created_by=user_id,
        is_public=False
    )
    db.session.add(rpt)
    db.session.flush()  # so rpt.id is available

    # charts_config is a list of dicts with 'type','title','config_json'
    for cfg in charts_config:
        # ensure JSON is valid
        json.loads(cfg['config_json'])
        c = Chart(
            report_id=rpt.id,
            chart_type=cfg['type'],
            title=cfg['title'],
            config_json=cfg['config_json']
        )
        db.session.add(c)

    db.session.commit()
    return rpt

def list_reports(public_only=False):
    q = Report.query
    if public_only:
        q = q.filter_by(is_public=True)
    return q.all()

def toggle_report_public(report_id):
    rpt = Report.query.get_or_404(report_id)
    rpt.is_public = not rpt.is_public
    db.session.commit()
    return rpt
