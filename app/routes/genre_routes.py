from flask import Blueprint, request, Response
from app.models.genre import Genre
from app.models.book import Book
from .route_utilities import create_model, get_models_with_filters,validate_model
from ..db import db

bp = Blueprint("genres_bp", __name__, url_prefix="/genres")

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)

@bp.get("")
def get_all_genres():
    return get_models_with_filters(Genre, request.args)

@bp.get("/<id>")
def get_one_genres(id):
    genre = validate_model(Genre, id)

    return genre.to_dict()


@bp.put("/<id>")
def update_one_genre(id):
    genre = validate_model(Genre, id)
    request_body = request.get_json()
    genre.name = request_body["name"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_one_genre(id):
    genre = validate_model(Genre, id)

    db.session.delete(genre)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
    



@bp.post("/<genre_id>/books")
def create_book_with_genre(genre_id):
    genre = validate_model(Genre, genre_id)
    print(genre)
    request_body = request.get_json()
    print(request_body)
    request_body["genres"] = [genre]
    print(request_body)
    return create_model(Book, request_body)


@bp.get("/<genre_id>/books")
def get_books_by_genres(genre_id):
    genre = validate_model(Genre, genre_id)

    response = [book.to_dict() for book in genre.books]
    return response