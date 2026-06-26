from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"},
]

@app.get("/students/active")
def get_active_students():
    active_students = [s for s in students if s["status"] == "active"]

    if not active_students:
        return {"message": "Không có sinh viên đang học", "data": []}

    return {"message": "Danh sách sinh viên đang học", "data": active_students}


"""_summary_Input: Danh sách students gốc có sẵn.
    Output: JSON object chứa message và data (mảng kết quả).
    Điều kiện lọc: status == "active". 
    Các bước xử lý:
    Lọc danh sách sinh viên theo điều kiện status == "active".
    Nếu mảng rỗng  Trả về message: "Không có sinh viên đang học" và data: []
    Nếu có dữ liệu  Trả về message: "Danh sách sinh viên đang học" và data: [danh sách đã lọc].
    Nếu có dữ liệu  Trả về message: "Danh sách sinh viên đang học" và data: [danh sách đã lọc].
"""