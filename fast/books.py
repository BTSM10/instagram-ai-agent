from fastapi import FastAPI, Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import List,Optional
app = FastAPI()

class books(BaseModel):
    id : Optional[int]= Field(default= None, gt = 0, lt = 10)
    author : str
    catagory: str
    rating : float = Field(gt=0,le=5)

BOOKS = [books(id= 1, author = 'ken', catagory='science',rating=4.5),
         books(id= 2, author = 'ben', catagory='math',rating=4.1),
         books(id= 3, author = 'ken', catagory='history',rating=3)
 
        ]
@app.get('/get_books_by_id/{book_id}')
def get_by_id(id:int = Path(gt=0,lt=10)):
    for book in BOOKS:
        if book.id == id:
            return book
    return HTTPException (status_code=404, detail='book not found')
@app.get('/book_by_author')
def by_author(author:str = Query(min_length=3, max_length=10)):
    collection =[]
    for book in BOOKS:
        if book.author == author:
            collection.append(book)
    return (book for book in collection) if len(collection) > 0 else HTTPException (status_code=404, detail='book not found')


@app.get('/all_books')
def all_books():
    return BOOKS
@app.post('/add_books')
def add_books(book:books):
    if book_id_exists(book.id):
        raise HTTPException(status_code=400, detail='book with same id already exists')
    BOOKS.append(book)
    return book

def book_id_exists(id:int):
    for book in BOOKS:
        if book.id == id:
            return True
    return False

@app.put('/update_book')
def update_book(book:books):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return BOOKS


@app.delete('/delete_book')
def delete_book(book:books):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS.pop(i)
            break
    return BOOKS
            
        