from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"},
]

@app.get("/students")
def get_all_students():
    return students


"""Endpoint hiện tại: /student

Lỗi 404: Do trong code cấu hình đường dẫn số ít (/student), khi gọi /students (số nhiều) hệ thống không tìm thấy nên báo lỗi 404.

Sai Naming Convention: Lấy danh sách thì endpoint phải dùng danh từ số nhiều /students theo chuẩn RESTful. Dùng số ít dễ hiểu lầm là lấy một sinh viên.

Sai nghiệp vụ: Dòng return students[0] chỉ trả về phần tử đầu tiên (sinh viên An) chứ không trả về toàn bộ danh sách.

API đúng yêu cầu: GET /students
"""