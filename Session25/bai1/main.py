import uuid
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status

app = FastAPI(title="Student Registration API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_COURSES = [
    "Python Basic",
    "FastAPI",
    "Data Analysis",
]

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

MAX_FILE_SIZE = 2 * 1024 * 1024  

@app.post("/students/register", status_code=status.HTTP_201_CREATED)
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    avatar: UploadFile = File(...),
):
    clean_name = full_name.strip()
    if not clean_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name is required and cannot be empty"
        )

    clean_email = email.strip()
    if "@" not in clean_email or clean_email.startswith("@") or clean_email.endswith("@"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    clean_phone = phone.strip()
    if not (clean_phone.isdigit() and len(clean_phone) == 10):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number must be exactly 10 digits"
        )

    if course not in ALLOWED_COURSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not available"
        )

    if avatar.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar must be in JPG or PNG format"
        )

    content = await avatar.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Avatar file size exceeds 2 MB limit"
        )

    file_extension = ALLOWED_IMAGE_TYPES[avatar.content_type]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "full_name": clean_name,
            "email": clean_email,
            "phone": clean_phone,
            "course": course,
            "avatar": str(file_path),
        },
    }

"""
=============================================================================
PHẦN 1: PHÁT HIỆN LỖI VÀ KỊCH BẢN KIỂM THỬ (TEST CASES)
=============================================================================
1. CÁC ĐOẠN CODE SAI TRONG HIỆN TRƯỜNG GIẢ:
- Họ tên: `full_name == ""` không dùng `.strip()` -> lọt chuỗi toàn dấu cách.
- Email: Bỏ quên logic kiểm tra ký tự '@'.
- SĐT: `len(phone) < 10` -> không chặn số > 10 ký tự và không kiểm tra số (`isdigit()`).
- Avatar: Không kiểm tra định dạng (nhận cả PDF), không kiểm tra dung lượng > 2MB.
- Lưu file: Dùng trực tiếp `avatar.filename` -> gây ghi đè file trùng tên.
- Mã lỗi: Trả về HTTP 200 OK thay vì các mã lỗi chuẩn (400, 413).

2. 5 TEST CASES CHI TIẾT:
- TC1: full_name = "   "
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Thiếu .strip()
- TC2: email = "nguyenle.gmail.com"
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Thiếu kiểm tra '@'
- TC3: phone = "09876abcde"
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Không kiểm tra số hợp lệ
- TC4: avatar = "file.pdf" (application/pdf)
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Không lọc định dạng JPG/PNG
- TC5: avatar = Dung lượng 3.5MB
  + Hiện tại: 200 OK | Kỳ vọng: 413 Payload Too Large | Nguyên nhân: Không chặn file > 2MB
=============================================================================
"""