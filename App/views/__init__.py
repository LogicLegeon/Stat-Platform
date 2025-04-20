# Import blueprints explicitly
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .entry import entry_views

# Initialize the list of views
views = [user_views, index_views, auth_views, entry_views]

# Add a comment for setup_admin if it needs to be used elsewhere
# setup_admin is imported but not added to views. Use it as needed.