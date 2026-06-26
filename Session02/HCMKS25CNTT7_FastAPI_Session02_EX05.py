from fastapi import FastAPI

app = FastAPI()


@app.get("/products")
def get_products():
    return {"message": "Danh sách toàn bộ sản phẩm"}


@app.get("/products/detail")
def get_product_detail():
    return {"message": "Thông tin chi tiết sản phẩm"}


@app.post("/products")
def create_product():
    return {"message": "Thêm sản phẩm mới thành công"}


@app.put("/products/update")
def update_product():
    return {"message": "Cập nhật thông tin sản phẩm thành công"}


@app.delete("/products/delete")
def delete_product():
    return {"message": "Xóa sản phẩm thành công"}


@app.get("/products/statistics")
def get_product_statistics():
    return {"message": "Thống kê tổng số lượng và doanh thu kho hàng"}


@app.get("/products/best-sellers")
def get_best_sellers():
    return {"message": "Danh sách sản phẩm bán chạy nhất tháng"}


@app.get("/products/clearance")
def get_clearance_products():
    return {"message": "Danh sách sản phẩm đang giảm giá xả kho"}


#1. Thiết kế kiến trúc routing (Quản lý sản phẩm)
#Chủ đề đã chọn: Quản lý sản phẩm (Products)
#Các endpoint chính:
#GET /products: Lấy danh sách toàn bộ sản phẩm.
#GET /products/detail: Xem thông tin chi tiết một sản phẩm.
#POST /products: Thêm sản phẩm mới vào hệ thống.
#PUT /products/update: Cập nhật thông tin sản phẩm.
#DELETE /products/delete: Xóa sản phẩm khỏi hệ thống.
#GET /products/statistics: Xem thống kê tổng quan kho hàng.
#Các endpoint sáng tạo mở rộng:
#GET /products/best-sellers: Lấy danh sách sản phẩm bán chạy nhất.
#GET /products/clearance: Lấy danh sách sản phẩm đang giảm giá xả kho.