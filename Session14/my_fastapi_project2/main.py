import uvicorn
from fastapi import FastAPI
from app.routers.student import router as student_router
# từ bài tập 1 (nếu muốn): from app.routers.product import router as product_router

app = FastAPI(
    title="Student Management API",
    description="Hệ thống API CRUD Quản lý Sinh viên - Bài tập tổng hợp 2",
    version="1.0.0"
)

# Đăng ký router Sinh viên
app.include_router(student_router)

@app.get("/")
def root():
    return {"message": "Welcome to Student Management API. Go to /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)