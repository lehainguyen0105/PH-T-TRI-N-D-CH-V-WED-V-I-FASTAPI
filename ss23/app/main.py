from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import auth, protected, cors_demo
# Import cả 2 model để SQLAlchemy nhận biết và tạo đủ bảng khi khởi động
from app.models import user, role  # noqa: F401


# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Demo Authentication FastAPI",
    description="Ứng dụng mẫu Đăng ký và Đăng nhập với FastAPI và MySQL dành cho sinh viên.",
    version="1.0.0"
)

# Tạo tất cả các bảng trong Database (nếu chưa có)
# Lưu ý: Trong thực tế dự án lớn thường dùng thư viện Alembic để quản lý database migration thay vì tạo trực tiếp.
Base.metadata.create_all(bind=engine)

# ==============================================================================
# DEMO CORS (Cross-Origin Resource Sharing)
# ==============================================================================
# Vấn đề: Trình duyệt (Chrome, Firefox,...) có cơ chế bảo mật gọi là Same-Origin Policy.
# Mặc định, script trên trang web tại "http://localhost:3000" (React) sẽ BỊ CHẶN
# nếu cố gắng fetch dữ liệu từ một server khác địa chỉ, ví dụ "http://localhost:8000" (FastAPI).
# Giải pháp: Server (FastAPI) phải nói cho trình duyệt biết rằng nó cho phép
# các nguồn (origins) nào được phép gọi tới thông qua CORSMiddleware.
# ==============================================================================

# Bước 1: Khai báo danh sách các domain được phép kết nối (Whitelist)
origins_whitelist = [
    "http://localhost:3000",             # Môi trường phát triển của Frontend React/Vue
    "http://localhost:5173",             # Môi trường phát triển của Frontend Vite
    "https://admin.myapp.com",          # Hệ thống quản trị nội bộ trên Production
    "https://myapp.com",                # Trang chủ chính thức
]

# Bước 2: Tích hợp CORSMiddleware vào ứng dụng (tầng Global - áp dụng cho TẤT CẢ endpoint)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_whitelist,     # Chỉ cho phép các nguồn trong danh sách trắng
                                         # (Dùng ["*"] để cho phép tất cả - KHÔNG nên dùng trên Production!)
    allow_credentials=True,             # Cho phép Client gửi kèm Cookies / Authorization Headers
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Giới hạn các phương thức được phép
    allow_headers=["Content-Type", "Authorization"], # Giới hạn các Header được gửi lên
)

# Nhúng router xử lý auth vào ứng dụng chính
app.include_router(auth.router)

# Nhúng router xử lý các API cần xác thực (Authorization)
app.include_router(protected.router)

# Nhúng router demo CORS
app.include_router(cors_demo.router)

@app.get("/")
def root():
    return {"message": "Chào mừng đến với API Authentication Demo. Hãy truy cập /docs để test."}

