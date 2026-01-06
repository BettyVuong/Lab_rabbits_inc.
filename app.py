#rough idea of an entry point for a Flask application
import os
from src import create_app

app = create_app()

# Uncomment the following lines if you want to create the database tables
# with app.app_context():
#     db.create_all()  # Create database tables for our data models

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug = debug)
