from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Student, Classroom
from schemas import StudentCreate, StudentUpdate
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

def get_students(db: Session, search: Optional[str] = None, class_id: Optional[int] = None):
    query = db.query(Student)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Student.full_name.like(search_filter)) |
            (Student.student_code.like(search_filter)) |
            (Student.email.like(search_filter))
        )
    if class_id:
        query = query.filter(Student.class_id == class_id)
    return query.all()

def get_student_detail(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sinh viên"
        )
    return student

def create_student(db: Session, data: StudentCreate):
    classroom = db.query(Classroom).filter(Classroom.id == data.class_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học không tồn tại"
        )
    
    if classroom.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học hiện không ở trạng thái hoạt động"
        )

    current_student_count = db.query(Student).filter(Student.class_id == data.class_id).count()
    if current_student_count >= classroom.max_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đã đủ số lượng sinh viên tối đa"
        )

    if db.query(Student).filter(Student.student_code == data.student_code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã sinh viên đã tồn tại"
        )

    if db.query(Student).filter(Student.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sinh viên đã tồn tại"
        )

    try:
        new_student = Student(**data.model_dump())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu khi thêm mới sinh viên"
        )

def update_student(db: Session, student_id: int, data: StudentUpdate):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sinh viên"
        )

    if db.query(Student).filter(Student.student_code == data.student_code, Student.id != student_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã sinh viên trùng với sinh viên khác"
        )

    if db.query(Student).filter(Student.email == data.email, Student.id != student_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email trùng với sinh viên khác"
        )

    if data.class_id != student.class_id:
        new_classroom = db.query(Classroom).filter(Classroom.id == data.class_id).first()
        if not new_classroom:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lớp học mới không tồn tại"
            )
        if new_classroom.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lớp học mới không ở trạng thái hoạt động"
            )
        current_count = db.query(Student).filter(Student.class_id == data.class_id).count()
        if current_count >= new_classroom.max_students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lớp học mới đã đầy"
            )

    try:
        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(student, key, value)
            
        db.commit()
        db.refresh(student)
        return student
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cơ sở dữ liệu khi cập nhật sinh viên"
        )