from App.models.user import Entry
from App.database import db

def add_entry(category, label, value):
    entry = Entry(category=category, label=label, value=value)
    db.session.add(entry)
    db.session.commit()
    return entry

def get_all_entries():
    return Entry.query.all()
