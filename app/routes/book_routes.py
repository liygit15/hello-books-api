from flask import Blueprint, abort, make_response, request,Response
from app.models.book import Book
from ..db import db
# from app.models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix ="/books")


@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201


@books_bp.get("")
def read_all_books():
    # 1. 创建查询语句
    query = db.select(Book).order_by(Book.id)

    # 2. 执行查询并获取所有 Book 实例
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    books = db.session.scalars(query)

    # 3. 转换为 JSON 可序列化的数据结构
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    # 4. 返回响应
    return books_response, 200





# @books_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response


@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title":book.title,
        "description":book.description,
    }


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        response = {"message": f"book {book_id} not found"}
        abort(make_response(response, 404))
    
    return book

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")



