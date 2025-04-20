from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

### Dataset Model
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255))
    upload_type = db.Column(db.String(50))  # "manual" or "spreadsheet"
    status = db.Column(db.String(20), default="draft")  # draft, validated, published
    #upload_date = db.Column(db.DateTime)

    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    entries = db.relationship('Entry', backref='dataset', lazy=True)
    errors = db.relationship('ValidationError', backref='dataset', lazy=True)
    reports = db.relationship('Report', backref='dataset', lazy=True)


### ValidationError Model
class ValidationError(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    error_type = db.Column(db.String(100))
    details = db.Column(db.Text)
    row_column = db.Column(db.String(50))


### Report Model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_path = db.Column(db.String(255))
    is_public = db.Column(db.Boolean, default=False)

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    charts = db.relationship('Chart', backref='report', lazy=True)


### Chart Model
class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    chart_type = db.Column(db.String(50))  # "bar", "line", etc.
    title = db.Column(db.String(100))
    config_json = db.Column(db.Text)  # Chart config stored as JSON


### DataField Model
class DataField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    field_type = db.Column(db.String(50))  # "dropdown", "number", etc.
    description = db.Column(db.Text)
    
    entries = db.relationship('Entry', backref='field', lazy=True)


### Entry Model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    field_id = db.Column(db.Integer, db.ForeignKey('data_field.id'))
    value = db.Column(db.String(255))





