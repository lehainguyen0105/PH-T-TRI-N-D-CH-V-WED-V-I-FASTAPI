from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Any

from database import Base, engine, get_db
import student_services
import schemas

app = FastAPI(
    title="HỆ THỐNG QUẢN LÝ SINH VIÊN THEO LỚP HỌC"
)

Base.metadata.create_all(bind=engine)

def format_response(status_code: int, message: str, path: str, data: Any = None, error: Any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": jsonable_encoder(data),
            "error": error,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "path": path
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return format_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        path=request.url.path,
        data=None,
        error="HTTPException"
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return format_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Dữ liệu không hợp lệ",
        path=request.url.path,
        data=None,
        error=exc.errors()
    )

@app.get("/students", status_code=status.HTTP_200_OK, tags=["Students"])
def get_students(
    request: Request,
    search: Optional[str] = None,
    class_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    students = student_services.get_students(db, search, class_id)
    student_data = [schemas.StudentDetailResponse.model_validate(s) for s in students]
    return format_response(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách sinh viên thành công",
        path=request.url.path,
        data=student_data
    )

@app.get("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
def get_student_detail(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    student = student_services.get_student_detail(db, student_id)
    student_data = schemas.StudentDetailResponse.model_validate(student)
    return format_response(
        status_code=status.HTTP_200_OK,
        message="Lấy chi tiết sinh viên thành công",
        path=request.url.path,
        data=student_data
    )

@app.post("/students", status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(
    data: schemas.StudentCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    new_student = student_services.create_student(db, data)
    student_data = schemas.StudentDetailResponse.model_validate(new_student)
    return format_response(
        status_code=status.HTTP_201_CREATED,
        message="Thêm mới sinh viên thành công",
        path=request.url.path,
        data=student_data
    )

@app.put("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
def update_student(
    student_id: int,
    data: schemas.StudentUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    updated_student = student_services.update_student(db, student_id, data)
    student_data = schemas.StudentDetailResponse.model_validate(updated_student)
    return format_response(
        status_code=status.HTTP_200_OK,
        message="Cập nhật thông tin sinh viên thành công",
        path=request.url.path,
        data=student_data
    )