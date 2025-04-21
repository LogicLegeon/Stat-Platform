from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

### User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    entries = db.relationship('Entry', backref='user', lazy=True)
    datasets = db.relationship('Dataset', backref='uploader', lazy=True)
    reports = db.relationship('Report', backref='creator', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


### Dataset Model
class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255))
    upload_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default="draft")

    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    entries = db.relationship('Entry', backref='dataset', lazy=True)
    errors = db.relationship('ValidationError', backref='dataset', lazy=True)
    reports = db.relationship('Report', backref='dataset', lazy=True)


### Entry Model
class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float, nullable=False)
    year = db.Column(db.String(10))
    campus = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    field_id = db.Column(db.Integer, db.ForeignKey('data_fields.id'))

    def __repr__(self):
        return f"<Entry {self.label} ({self.category}) — {self.value} @ {self.campus}, {self.year}>"


### ValidationError Model
class ValidationError(db.Model):
    __tablename__ = 'validation_errors'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    error_type = db.Column(db.String(100))
    details = db.Column(db.Text)
    row_column = db.Column(db.String(50))


### Report Model
class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    report_path = db.Column(db.String(255))
    is_public = db.Column(db.Boolean, default=False)

    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    charts = db.relationship('Chart', backref='report', lazy=True)


### Chart Model
class Chart(db.Model):
    __tablename__ = 'charts'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    chart_type = db.Column(db.String(50))
    title = db.Column(db.String(100))
    config_json = db.Column(db.Text)


### DataField Model
class DataField(db.Model):
    __tablename__ = 'data_fields'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    field_type = db.Column(db.String(50))  # e.g. dropdown, number
    description = db.Column(db.Text)

    entries = db.relationship('Entry', backref='field', lazy=True)
