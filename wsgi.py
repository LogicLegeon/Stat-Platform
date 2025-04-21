# wsgi.py
from App.main import create_app

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # only for local debugging; use gunicorn in production
    app.run(host="0.0.0.0", port=8000)
# wsgi.py

