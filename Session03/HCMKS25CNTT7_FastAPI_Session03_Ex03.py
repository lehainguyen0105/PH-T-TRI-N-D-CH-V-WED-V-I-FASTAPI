from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available": True
    }
]

@app.get("/health")
def check_health():
    return {"message": "Library API is running"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/available")
def get_available_books():
    return [b for b in books if b["is_available"] == True]

@app.get("/books/borrowed")
def get_borrowed_books():
    return [b for b in books if b["is_available"] == False]

@app.get("/books/statistics")
def get_statistics():
    total = len(books)
    available = len([b for b in books if b["is_available"] == True])
    borrowed = len([b for b in books if b["is_available"] == False])
    return {
        "total_books": total,
        "available_books": available,
        "borrowed_books": borrowed
    }

@app.get("/books/categories")
def get_categories():
    unique_categories = list(set([b["category"] for b in books]))
    return {"categories": unique_categories}

@app.get("/books/latest")
def get_latest_book():
    if not books:
        return {"message": "No books available"}
    latest_book = max(books, key=lambda b: b["year"])
    return latest_book