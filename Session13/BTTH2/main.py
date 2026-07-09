from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from boarding_service import get_all, create_slot, detail_slot, update_slot, delete_slot
from database import get_db
from schemas import SlotRequest

app = FastAPI(title="Pet Boarding Slots Management")

@app.get("/boarding-slots")
def get_all_slots(request: Request, db: Session = Depends(get_db)):
    return get_all(request, db)

@app.post("/boarding-slots")
def add_slot(request: Request, slot: SlotRequest, db: Session = Depends(get_db)):
    return create_slot(request, db, slot)

@app.get("/boarding-slots/{slot_id}")
def get_detail_slot(request: Request, slot_id: int, db: Session = Depends(get_db)):
    return detail_slot(request, db, slot_id)

@app.put("/boarding-slots/{slot_id}")
def update_slots(request: Request, slot_id: int, slot_update: SlotRequest, db: Session = Depends(get_db)):
    return update_slot(request, db, slot_id, slot_update)

@app.delete("/boarding-slots/{slot_id}")
def delete_slots(request: Request, slot_id: int, db: Session = Depends(get_db)):
    return delete_slot(request, db, slot_id)