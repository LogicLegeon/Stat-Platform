# App/controllers/entry.py

from App.models.user import Entry
from App.database import db

from App.models import Entry
from App.database import db

def get_all_entries():
    return Entry.query.all()



from App.models import Entry
from App.database import db

def add_entry(category, label, value, year=None, campus=None):
    print("💾 Writing entry to DB:", category, label, value, year, campus)

    try:
        entry = Entry(
            category=category,
            label=label,
            value=value,
            year=year,
            campus=campus
        )
        db.session.add(entry)
        print("🌀 Added to session")
        db.session.commit()
        print("✅ Entry committed successfully")
    except Exception as e:
        print("❌ ERROR committing entry to DB:", e)


def submit_entries_for_review():
    # In a real app, you'd flag entries for review or notify admins
    print("🛠️ Submit for review was triggered (placeholder)")
    return True
