from fastapi import FastAPI

app = FastAPI()

BOOKS = [
	{'title': 'Title One', 'author': 'Author One', 'category': 'science'},
	{'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
	{'title': 'Title Three', 'author': 'Author Three', 'category': 'math'},
	{'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
	{'title': 'Title Five', 'author': 'Author Five', 'category': 'science'},
]

@app.get("/books")
async def read_all_books():
	return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
	for book in BOOKS:
		if book.get('title').casefold() == book_title.casefold():
			return book

# fastAPI는 모든 기능을 시간순으로 위에서 아래로 보기 때문에, 위의 값이 출력 된다.
# 그래서 순서를 위로 바꾸거나 해야한다.
# @app.get("/books/mybook")
# async def read_all_books():
# 	return {'book_title': 'My favorite book!'}

@app.get("/books/")
def read_category_by_query(category: str):
	books_to_return = []
	for book in BOOKS:
		if book.get('category').casefold() == category.casefold():
			books_to_return.append(book)
	return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
	books_to_return = []
	for book in BOOKS:
		if book.get('author').casefold() == book_author.casefold() and \
			book.get('category').casefold() == category.casefold():
			books_to_return.append(book)

	return  books_to_return







