# KỊCH BẢN KIỂM THỬ HỆ THỐNG MEDCARE E-PRESCRIPTION

## Chuẩn bị dữ liệu mẫu
1. Đăng ký Bác sĩ:
   POST /api/v1/medical/register
   Body: {"username": "bs_nam", "password": "SecurePassword123@", "role": "doctor"}
2. Đăng ký Dược sĩ:
   POST /api/v1/medical/register
   Body: {"username": "ds_lan", "password": "SecurePassword123@", "role": "pharmacist"}

---

## Test Case 1: Bác sĩ đăng nhập và tạo đơn thuốc thành công
* Bước 1: Login tài khoản `bs_nam` tại `POST /api/v1/medical/login`.
  -> Nhận Token JWT (Role: doctor).
* Bước 2: Gọi `POST /api/v1/prescriptions` kèm Header `Authorization: Bearer <TOKEN_BAC_SI>`.
  Body:
  {
    "patient_id": "BN-9921",
    "patient_name": "Nguyen Van A",
    "diagnosis": "Viêm phế quản cấp",
    "medicines": [{"name": "Augmentin 1g", "dosage": "2 vien/ngay", "quantity": 14}]
  }
* Kết quả kỳ vọng: 
  - Status Code: 201 Created
  - Dữ liệu trả về có `signed_by_doctor`: "bs_nam".

---

## Test Case 2: Phân quyền Dược sĩ (Tạo đơn bị 403, Xem đơn được 200)
* Bước 1: Login tài khoản `ds_lan` tại `POST /api/v1/medical/login`.
  -> Nhận Token JWT (Role: pharmacist).
* Bước 2: Dùng Token Dược sĩ gọi `POST /api/v1/prescriptions`.
  - Kết quả kỳ vọng: 
    - Status Code: 403 Forbidden
    - Detail: "Không đủ quyền hạn truy cập tài nguyên này"
* Bước 3: Dùng Token Dược sĩ gọi `GET /api/v1/prescriptions/view`.
  - Kết quả kỳ vọng: 
    - Status Code: 200 OK
    - Danh sách đơn thuốc đã tạo ở Test Case 1 hiển thị đầy đủ.

---

## Test Case 3: Token giả mạo chữ ký hoặc sai định dạng bị chặn
* Bước 1: Lấy token hợp lệ của `bs_nam`.
* Bước 2: Sửa đổi 1 ký tự bất kỳ ở phần cuối Token (phần Signature).
* Bước 3: Gửi request `GET /api/v1/prescriptions/view` với Token đã bị sửa.
* Kết quả kỳ vọng: 
  - Status Code: 401 Unauthorized
  - Detail: "Token không hợp lệ hoặc chữ ký bị giả mạo"