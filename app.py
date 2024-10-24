import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes after app and db are defined
from routes import *

# Create a Flask command to reset the database
@app.cli.command("reset-db")
def reset_db():
    """Drops all tables and recreates them."""
    db.drop_all()
    db.create_all()
    print("Database reset successfully!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
