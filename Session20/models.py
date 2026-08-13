from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    bio = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="profile")

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    class_code = Column(String(50), unique=True, nullable=False)
    class_name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), default="active", nullable=False)

    students = relationship("Student", back_populates="classroom")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    student_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    class_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    classroom = relationship("Classroom", back_populates="students")
    courses = relationship("Course", secondary=enrollments, back_populates="students")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    course_name = Column(String(100), nullable=False)

    students = relationship("Student", secondary=enrollments, back_populates="courses")