from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from menu_service import get_all, create_menu, detail_menu, update_menu, delete_menu
from database import get_db
from schemas import MenuRequest

app = FastAPI()

@app.get("/menu-items")
def get_all_menus(request: Request, db: Session = Depends(get_db)):
    return get_all(request, db)

@app.post("/menu-items")
def add_menu(request: Request, menu: MenuRequest, db: Session = Depends(get_db)):
    return create_menu(request, db, menu)

@app.get("/menu-items/{item_id}")
def get_detail_menu(request: Request, item_id: int, db: Session = Depends(get_db)):
    return detail_menu(request, db, item_id)

@app.put("/menu-items/{item_id}")
def update_menus(request: Request, item_id: int, menu_update: MenuRequest, db: Session = Depends(get_db)):
    return update_menu(request, db, item_id, menu_update)

@app.delete("/menu-items/{item_id}")
def update_menus(request: Request, item_id: int, db: Session = Depends(get_db)):
    return delete_menu(request, db, item_id)