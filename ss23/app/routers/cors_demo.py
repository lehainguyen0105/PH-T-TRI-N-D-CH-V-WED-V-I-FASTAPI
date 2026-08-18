from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/cors-demo",
    tags=["CORS Demo"]
)

@router.get("/warehouses")
async def get_warehouses():
    """
    Endpoint công khai để demo CORS.
    Khi cấu hình CORS thành công, trình duyệt của Frontend App (VD: React tại http://localhost:3000)
    sẽ fetch được dữ liệu này mà KHÔNG bị trình duyệt chặn.
    Nếu domain của Frontend KHÔNG có trong danh sách trắng (whitelist),
    trình duyệt sẽ tự động chặn và báo lỗi: "CORS policy: No 'Access-Control-Allow-Origin' header".
    """
    warehouses_data = [
        {"id": 1, "name": "Kho Hà Nội", "address": "Quận Long Biên, Hà Nội"},
        {"id": 2, "name": "Kho TP. Hồ Chí Minh", "address": "Quận 9, TP. HCM"}
    ]
    return JSONResponse(content={"status": "success", "data": warehouses_data})

@router.get("/products")
async def get_products():
    """
    Endpoint thứ 2 để demo CORS.
    Mọi endpoint trong ứng dụng đều được bảo vệ bởi CORSMiddleware tầng gloabl,
    không cần cấu hình riêng cho từng endpoint.
    """
    products_data = [
        {"id": 1, "name": "Laptop Dell XPS", "stock": 50},
        {"id": 2, "name": "iPhone 15 Pro", "stock": 120}
    ]
    return JSONResponse(content={"status": "success", "data": products_data})
