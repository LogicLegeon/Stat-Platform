# App/controllers/entry.py

from App.models.user import Entry
from App.database import db

from App.models import Entry
from App.database import db

def get_all_entries():
    return Entry.query.all()



from App.models import Entry
from App.database import db


from App.models import Entry
from App.database import db

def add_entry(category, label, value, year=None, campus=None, user_id=None):
    print("💾 Writing entry to DB:", category, label, value, year, campus, user_id)
    entry = Entry(
        category=category,
        label=label,
        value=value,
        year=year,
        campus=campus,
        user_id=user_id
    )
    db.session.add(entry)
    db.session.commit()

def get_all_entries():
    return Entry.query.all()

def submit_entries_for_review():
    # placeholder
    return True


def submit_entries_for_review():
    # In a real app, you'd flag entries for review or notify admins
    print("🛠️ Submit for review was triggered (placeholder)")
    return True
