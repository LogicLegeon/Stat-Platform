# Import blueprints explicitly
from .user import user_views
from .index import index_views
from .auth import auth_views
from .entry import entry_views
from .admin import setup_admin  # Import only setup_admin, not admin
from .dashboard import dashboard_views

# Initialize the list of views
views = [
    user_views,
    index_views,
    auth_views,
    entry_views,
    dashboard_views,
]

# Export setup_admin for use in main.py
__all__ = ['views', 'setup_admin']