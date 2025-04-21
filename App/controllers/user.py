from App.models import User
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

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


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    