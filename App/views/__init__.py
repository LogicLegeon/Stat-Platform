# filepath: /Users/slintbot/Desktop/Stat-Platform/App/views/__init__.py

# Import blueprints explicitly
from .user import user_views
from .index import index_views
from .auth import auth_views
from .entry import entry_views
from .admin import setup_admin  # Import only setup_admin, not admin
from .dashboard import dashboard_views

# App/views/__init__.py

from .auth           import auth_views
from .index          import index_views
from .entry          import entry_views
from .dashboard      import dashboard_views
from .admin          import setup_admin

# Now include auth_views in the list of site blueprints
views = [
    auth_views,      # ← add this
    index_views,
    entry_views,
    dashboard_views,
]


# Initialize the list of views
views = [user_views, index_views, auth_views, entry_views, dashboard_views]

# Export setup_admin for use in main.py
__all__ = ['views', 'setup_admin']