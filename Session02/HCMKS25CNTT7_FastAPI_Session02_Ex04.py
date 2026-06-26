from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2},
]


@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []

    for book in books:
        if "quantity" not in book:
            continue
        if book["quantity"] < 0:
            continue
        if book["quantity"] <= 5:
            low_stock_books.append(book)

    if not low_stock_books:
        return {"message": "Không có sách nào sắp hết hàng", "data": []}

    return {"message": "Danh sách sách sắp hết hàng", "data": low_stock_books}


#Phần 1: Phân tích Input/Output
#Input: Danh sách dữ liệu books chứa thông tin về sách, trong đó mỗi cuốn sách là một dictionary có thể có các trường id, title, và quantity.
#Output: Một JSON object gồm hai trường: message (thông báo trạng thái) và data (mảng chứa các sách thỏa mãn điều kiện và hợp lệ).
#Điều kiện xác định sách sắp hết hàng: 0 <= quantity <= 5 (và trường quantity bắt buộc phải tồn tại).
#Phần 2: Đề xuất giải pháp lọc dữ liệu
#Giải pháp 1: Sử dụng vòng lặp for truyền thống kết hợp hàm .get()
#Duyệt qua từng phần tử bằng vòng lặp for. Sử dụng các câu lệnh rẽ nhánh if/elif hoặc continue để kiểm tra sự tồn tại của dữ liệu, lọc bỏ các giá trị không hợp lệ (âm hoặc thiếu trường) trước khi kiểm tra điều kiện tồn kho.
#Giải pháp 2: Sử dụng List Comprehension kết hợp hàm điều kiện tự định nghĩa (Helper Function)
#Viết một hàm phụ để kiểm tra tính hợp lệ và điều kiện hết hàng của một cuốn sách. Sau đó dùng List Comprehension để gộp toàn bộ quá trình duyệt và lọc trên một dòng code duy nhất.
#1. So sánh & Lựa chọn giải pháp
#Vòng lặp for truyền thống: Dù tốn nhiều dòng code hơn nhưng luồng chạy rất tuần tự và tường minh. Việc tách các điều kiện loại bỏ bẫy dữ liệu (thiếu trường, số lượng âm) bằng câu lệnh if và continue cực kỳ dễ dàng, giúp code không bị crash và rất dễ bảo trì khi nghiệp vụ thay đổi.
#List Comprehension: Viết code rất ngắn (chỉ trên 1 dòng) nhưng lại cực kỳ phức tạp và rối mắt khi phải nhồi nhét nhiều điều kiện kiểm tra lỗi cùng lúc. Điều này làm giảm khả năng đọc hiểu và khó bắt lỗi dữ liệu.
#Lựa chọn: Vòng lặp for là giải pháp tối ưu nhất cho bài toán này để xử lý triệt để và an toàn các bẫy dữ liệu đầu vào.
#2. Các bước xử lý
#Người dùng gửi request đến endpoint GET /books/low-stock.
#Hệ thống duyệt qua từng cuốn sách trong danh sách books.
#Kiểm tra bẫy dữ liệu: Nếu sách thiếu trường quantity hoặc có quantity < 0 thì bỏ qua (continue).
#Kiểm tra điều kiện tồn kho: Nếu quantity <= 5 thì thêm cuốn sách đó vào danh sách lọc low_stock.
#Nếu danh sách lọc trống, trả về thông báo không có sách sắp hết hàng kèm mảng rỗng. Ngược lại, trả về danh sách sách đã lọc.