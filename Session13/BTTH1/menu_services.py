from fastapi import status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model import MenuItem
from schemas import MenuRequest, MenuResponse, standard_response

def get_all(request: Request, db: Session):
    menus = db.query(MenuItem).all()
    menu_dto = [MenuResponse.model_validate(menu) for menu in menus]

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=menu_dto,
        error=None,
        message="Thêm menu thành công!",
        path=request.url.path
    )

def create_menu(request: Request, db: Session, menu: MenuRequest):
    new_menu = MenuItem(**menu.model_dump())
    try:
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)

        menu_dto = MenuResponse.model_validate(new_menu)

        return standard_response(
            status_code=status.HTTP_201_CREATED,
            data=menu_dto,
            error=None,
            message="Thêm menu thành công!",
            path=request.url.path
        )
    except IntegrityError as err:
        db.rollback()
         
        return standard_response(
            status_code=status.HTTP_409_CONFLICT,
            data=None,
            error="Dist code đã tồn tại",
            message="Thêm menu thất bại!",
            path=request.url.path
        )
    except Exception as e:
        raise e
    
def detail_menu(request: Request, db: Session, menu_id: int):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if menu is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error=None,
            message="Menu không tồn tại!",
            path=request.url.path
        )
    menu_dto = MenuResponse.model_validate(menu)

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=menu_dto,
        error=None,
        message="Lấy thông tin menu thành công!",
        path=request.url.path
    )

def update_menu(request: Request, db: Session, menu_id: int, menu_update: MenuRequest):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if menu is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error=None,
            message="Menu không tồn tại!",
            path=request.url.path
        )
    
    menu.dish_code = menu_update.dish_code
    menu.dish_name = menu_update.dish_name
    menu.calorie_count = menu_update.calorie_count
    menu.price = menu_update.price
    menu.status = menu_update.status

    try:
        db.commit()
        db.refresh(menu)
        menu_dto = MenuResponse.model_validate(menu)
    except Exception as error:
        db.rollback()
        return standard_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            error=str(error),
            message="Cập nhật menu thất bại!",
            path=request.url.path
        )

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=menu_dto,
        error=None,
        message="Cập nhật menu thành công!",
        path=request.url.path
    )
   
def delete_menu(request: Request, db: Session, menu_id: int):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if menu is None:
        return standard_response(
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
            error=None,
            message="Menu không tồn tại!",
            path=request.url.path
        )
    
    db.delete(menu)
    db.commit()
    
    menu_dto = MenuResponse.model_validate(menu)

    return standard_response(
        status_code=status.HTTP_200_OK,
        data=menu_dto,
        error=None,
        message="Xóa menu thành công!",
        path=request.url.path
    )