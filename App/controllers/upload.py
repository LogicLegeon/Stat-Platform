import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from App.database import db
from App.models import Dataset
from werkzeug.utils import secure_filename
from datetime import datetime

upload_views = Blueprint('upload_views', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'App/static/uploads'

@upload_views.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('user_id'):
        return redirect(url_for('auth_views.login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        data_type = request.form['data_type']
        file = request.files['datafile']

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            dataset = Dataset(
                title=title,
                description=description,
                filename=filename,
                data_type=data_type,
                uploaded_by=session['user_id'],
                upload_date=datetime.utcnow()
            )
            db.session.add(dataset)
            db.session.commit()

            flash('✅ File uploaded successfully!')
            return redirect(url_for('dashboard_views.dashboard'))

    return render_template('upload.html')

