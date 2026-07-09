from fastapi import status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model import BoardingSlot
from schemas import SlotRequest, SlotResponse, standard_response

def get_all(request: Request, db: Session):
    slots = db.query(BoardingSlot).all()
    slot_dto = [SlotResponse.model_validate(s) for s in slots]

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=slot_dto,
        error=None,
        message="Lấy danh sách thành công",
        path=request.url.path
    )

def create_slot(request: Request, db: Session, slot_data: SlotRequest):
    new_slot = BoardingSlot(**slot_data.model_dump())
    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        slot_dto = SlotResponse.model_validate(new_slot)

        return standard_response(
            status_code=status.HTTP_201_CREATED,
            data=slot_dto,
            error=None,
            message="Thêm khoang lưu trú thành công!",
            path=request.url.path
        )
    except IntegrityError:
        db.rollback()
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            data=None,
            error="Bad Request",
            message="Slot number already exists",
            path=request.url.path
        )
    except Exception as e:
        db.rollback()
        raise e

def detail_slot(request: Request, db: Session, slot_id: int):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if slot is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error="Not Found",
            message="Boarding slot not found",
            path=request.url.path
        )
    
    slot_dto = SlotResponse.model_validate(slot)

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=slot_dto,
        error=None,
        message="Lấy chi tiết khoang lưu trú thành công!",
        path=request.url.path
    )

def update_slot(request: Request, db: Session, slot_id: int, slot_update: SlotRequest):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if slot is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error="Not Found",
            message="Boarding slot not found",
            path=request.url.path
        )

    try:
        update_dict = slot_update.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(slot, key, value)

        db.commit()
        db.refresh(slot)
        slot_dto = SlotResponse.model_validate(slot)
    except IntegrityError:
        db.rollback()
        return standard_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            data=None,
            error="Bad Request",
            message="Slot number already exists",
            path=request.url.path
        )
    except Exception as error:
        db.rollback()
        return standard_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            error=str(error),
            message="Cập nhật khoang lưu trú thất bại!",
            path=request.url.path
        )

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=slot_dto,
        error=None,
        message="Cập nhật thông tin thành công!",
        path=request.url.path
    )

def delete_slot(request: Request, db: Session, slot_id: int):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if slot is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error="Not Found",
            message="Boarding slot not found",
            path=request.url.path
        )

    try:
        db.delete(slot)
        db.commit()
    except Exception as error:
        db.rollback()
        return standard_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            error=str(error),
            message="Xóa khoang lưu trú thất bại!",
            path=request.url.path
        )

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=None,
        error=None,
        message="Xóa khoang lưu trú thành công!",
        path=request.url.path
    )