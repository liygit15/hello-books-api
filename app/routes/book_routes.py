from flask import Blueprint, abort, make_response, request,Response
from app.models.book import Book
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters
from app.models.author import Author
# from app.models.book import books

bp = Blueprint("books", __name__, url_prefix ="/books")


@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)


# @bp.get("")
# def read_all_books():
#     # 1. 创建查询语句
#     query = db.select(Book).order_by(Book.id)

#     # 2. 执行查询并获取所有 Book 实例
#     # We could also write the line above as:
#     # books = db.session.execute(query).scalars()

#     books = db.session.scalars(query)

#     # 3. 转换为 JSON 可序列化的数据结构
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })

#     # 4. 返回响应
#     return books_response, 200

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)


@bp.get("/<model_id>")
def get_one_book(model_id):
    book = validate_model(Book, model_id)

    return book.to_dict()



@bp.put("/<model_id>")
def update_book(model_id):
    book = validate_model(Book, model_id)
    request_body = request.get_json()

    book.title = request_body.get("title", book.title)
    book.description = request_body.get("description", book.description)
    author_id = request_body.get("author_id")
    if author_id is not None:
        author = Author.query.get(author_id)
        if not author:
            abort(404, f"Author {author_id} not found")
        book.author = author  # 通过 ORM 更新关系

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<model_id>")
def delete_book(model_id):
    book = validate_model(Book, model_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
