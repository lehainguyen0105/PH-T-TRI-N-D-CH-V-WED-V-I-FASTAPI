"""
================ PHẦN 1: PHÁT HIỆN VÀ PHÂN TÍCH LỖ HỔNG ================

1. Lỗi điều kiện phân quyền trong require_admin():
   - Vị trí: Dòng `if current_user["role"] == "admin" or current_user["is_active"]:`
   - Nguyên nhân: Sử dụng toán tử `or`, dẫn đến bất kỳ user nào có `is_active: True` (kể cả role user) đều được phép xóa khóa học.
   - Test case: DELETE /admin/courses/1 với user-token -> Thực tế: 200 OK | Kỳ vọng: 403 Forbidden.

2. Lỗi Middleware bắt buộc Authorization với mọi request:
   - Vị trí: Dòng `if "authorization" not in request.headers:` trong authentication_middleware.
   - Nguyên nhân: Chặn toàn bộ request không có header Authorization, làm endpoint công khai `/health` bị lỗi 401.
   - Test case: GET /health (không token) -> Thực tế: 401 Unauthorized | Kỳ vọng: 200 OK.

3. Lỗi Middleware chặn phương thức OPTIONS (CORS Preflight):
   - Vị trí: authentication_middleware xử lý trước mà không bỏ qua method OPTIONS.
   - Nguyên nhân: Request OPTIONS do trình duyệt gửi tự động không mang Authorization header, dẫn đến bị Middleware trả về 401.
   - Test case: OPTIONS /courses (Origin: http://localhost:5173) -> Thực tế: 401 Unauthorized | Kỳ vọng: 200 OK + CORS headers.

4. Lỗi cấu hình CORS cho phép mọi nguồn:
   - Vị trí: `allow_origins=["*"]` trong cấu hình CORSMiddleware.
   - Nguyên nhân: Vi phạm yêu cầu chỉ cho phép 2 domain (http://localhost:3000 và http://localhost:5173).
   - Test case: Gửi request với Origin: https://unknown-website.com -> Thực tế: Chấp nhận mọi nguồn | Kỳ vọng: Bị chặn CORS.
=========================================================================
"""

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="Course Management System")

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}

PUBLIC_PATHS = ["/health", "/docs", "/openapi.json", "/redoc"]

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path in PUBLIC_PATHS:
        response = await call_next(request)
        response.headers["X-System-Name"] = "Learning Management System"
        return response

    if "authorization" not in request.headers:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header is required"},
        )

    response = await call_next(request)
    response.headers["X-System-Name"] = "Learning Management System"
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = TOKENS.get(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa hoặc không hoạt động",
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required",
        )
    return current_user


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/courses")
def get_courses(current_user: dict = Depends(get_current_user)):
    return {
        "items": [
            {"id": 1, "name": "FastAPI Basic"},
            {"id": 2, "name": "FastAPI Security"},
        ]
    }


@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }