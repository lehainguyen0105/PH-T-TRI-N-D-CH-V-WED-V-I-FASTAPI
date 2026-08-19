from enum import Enum
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class Role(str, Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    STAFF = "STAFF"

ROUTE_PERMISSIONS = {
    "/api/v1/system/settings": [Role.ADMIN],
    "/api/v1/salary/modify": [Role.ADMIN, Role.HR],
    "/api/v1/profile": [Role.ADMIN, Role.HR, Role.STAFF],
}

app = FastAPI(
    title="MegaMart ERP Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://internal.megamart.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-User-Role"],
)

@app.middleware("http")
async def rbac_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    path = request.url.path

    for protected_path, allowed_roles in ROUTE_PERMISSIONS.items():
        if path.startswith(protected_path):
            user_role = request.headers.get("X-User-Role")
            if not user_role or user_role not in allowed_roles:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"error": "Permission Denied"}
                )
            break

    response = await call_next(request)
    return response

@app.get("/api/v1/salary/modify")
async def modify_salary(request: Request):
    current_role = request.headers.get("X-User-Role")
    return {
        "status": "success",
        "role": current_role,
        "message": "Truy cập chức năng cập nhật bảng lương thành công."
    }

@app.get("/api/v1/system/settings")
async def system_settings(request: Request):
    current_role = request.headers.get("X-User-Role")
    return {
        "status": "success",
        "role": current_role,
        "message": "Truy cập cấu hình hệ thống máy chủ ERP thành công."
    }

@app.get("/api/v1/profile")
async def get_profile(request: Request):
    current_role = request.headers.get("X-User-Role")
    return {
        "status": "success",
        "role": current_role,
        "message": "Xem thông tin hồ sơ cá nhân thành công."
    }