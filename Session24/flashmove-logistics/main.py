from enum import Enum
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class Role(str, Enum):
    DISPATCHER = "DISPATCHER"
    DRIVER = "DRIVER"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"

ROUTE_PERMISSIONS = {
    "/api/v1/orders/assign": [Role.DISPATCHER],
    "/api/v1/orders/status": [Role.DISPATCHER, Role.DRIVER],
    "/api/v1/orders/track": [Role.DISPATCHER, Role.DRIVER, Role.CUSTOMER_SUPPORT],
}

app = FastAPI(
    title="FlashMove Logistics Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://driver.flashmove.io",
        "https://hub.flashmove.io"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "X-Role-Identity"],
)

@app.middleware("http")
async def rbac_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    path = request.url.path

    for protected_path, allowed_roles in ROUTE_PERMISSIONS.items():
        if path.startswith(protected_path):
            user_role = request.headers.get("X-Role-Identity")
            if not user_role or user_role not in allowed_roles:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"status": "Rejected", "reason": "Unauthorized action for this role"}
                )
            break

    response = await call_next(request)
    return response

@app.post("/api/v1/orders/assign")
async def assign_order(request: Request):
    current_role = request.headers.get("X-Role-Identity")
    return {
        "status": "success",
        "role": current_role,
        "message": "Gán đơn hàng cho tài xế thành công."
    }

@app.patch("/api/v1/orders/status")
async def update_order_status(request: Request):
    current_role = request.headers.get("X-Role-Identity")
    return {
        "status": "success",
        "role": current_role,
        "message": "Cập nhật trạng thái đơn hàng thành công."
    }

@app.get("/api/v1/orders/track")
async def track_order(request: Request):
    current_role = request.headers.get("X-Role-Identity")
    return {
        "status": "success",
        "role": current_role,
        "message": "Xem tiến trình đơn hàng thành công."
    }