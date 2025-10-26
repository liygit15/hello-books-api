from flask import Flask
from .db import db, migrate
from .models import book 
from .routes.book_routes import books_bp


def create_app():
    # __name__ stores the name of the module we're in 
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(books_bp)
    return app



# from flask import Flask
# from .routes.cat_routes import cats_bp # only import what you need. import too much is a waste, but they still in memory.

# def create_app():
#     # __name__ stores the name of the module we are in
#     app = Flask(__name__)
    
#     app.register_blueprint(cats_bp)

#     return app