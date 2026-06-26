from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]

@app.get("/students")
def get_students():
    return students

# (1) Phân tích lỗi nhanh
# Lỗi dữ liệu: Nếu dùng str(students) thì sẽ trả về chuỗi thay vì mảng JSON.
# Lỗi thiết kế: Nếu endpoint là /getStudents thì sai chuẩn RESTful, đúng phải là /students.
