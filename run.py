#rough idea of an entry point for a Flask application
from src import create_app

app = create_app()

# Uncomment the following lines if you want to create the database tables
# with app.app_context():
#     db.create_all()  # Create database tables for our data models

if __name__ == '__main__':
    app.run(debug=True)
