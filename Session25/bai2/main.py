"""
=============================================================================
PHẦN 1: PHÁT HIỆN LỖI VÀ KỊCH BẢN KIỂM THỬ (TEST CASES)
=============================================================================
1. TỐI THIỂU 5 LỖI TRONG HIỆN TRƯỜNG GIẢ:
- Lấy đuôi file: Dùng `split('.')[1]` -> Bị lỗi `IndexError` nếu file không có đuôi (README) 
  hoặc nhận sai đuôi với file nhiều dấu chấm (`baitap.pdf.exe` lấy ra `pdf` thay vì `exe`).
- Thư mục lưu trữ: Không tự động tạo thư mục `storage/documents` -> Crash `FileNotFoundError`.
- File rỗng & Kích thước: Không kiểm tra file 0 byte và không chặn file vượt quá 10 MB.
- Chuẩn hóa & Validate: Không chuẩn hóa `course_code` sang chữ HOA, không kiểm tra `document_type` và `title`.
- Bảo mật file: Dùng trực tiếp `document.filename` -> Dễ bị tấn công Path Traversal và ghi đè file trùng tên.
- HTTP Status Code: Trả về 200 OK cho mọi trường hợp lỗi thay vì mã HTTP chuẩn (400, 413).

2. 5 TEST CASES CHI TIẾT:
- TC1: File nhiều dấu chấm (filename = "baitap.pdf.exe")
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: `split('.')[1]` nhận diện nhầm thành 'pdf'.
- TC2: File không có phần mở rộng (filename = "README")
  + Hiện tại: Crash 500 (IndexError) | Kỳ vọng: 400 Bad Request | Nguyên nhân: Không tìm thấy phần tử thứ 2.
- TC3: File rỗng (Size = 0 byte)
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Không kiểm tra dung lượng `len(content) == 0`.
- TC4: Mã môn học viết thường (course_code = "it215")
  + Hiện tại: Lưu "it215" | Kỳ vọng: Lưu "IT215" | Nguyên nhân: Thiếu hàm `.upper()`.
- TC5: Loại tài liệu sai (document_type = "exam_cheat")
  + Hiện tại: 200 OK | Kỳ vọng: 400 Bad Request | Nguyên nhân: Không kiểm tra danh sách loại tài liệu hợp lệ.
=============================================================================
"""

import uuid
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status

app = FastAPI(title="Academic Document Management API")


UPLOAD_FOLDER = Path("storage/documents")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# 2. Định nghĩa các danh mục và quy tắc hợp lệ
ALLOWED_DOCUMENT_TYPES = ["lecture", "assignment", "reference"]
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@app.post("/documents", status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str = Form(...),
    course_code: str = Form(...),
    document_type: str = Form(...),
    description: str = Form(""),
    document: UploadFile = File(...),
):
    clean_title = title.strip()
    if not clean_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document title is required and cannot be empty"
        )

    clean_course_code = course_code.strip().upper()
    if not clean_course_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code is required"
        )

    clean_doc_type = document_type.strip().lower()
    if clean_doc_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type. Allowed types: {', '.join(ALLOWED_DOCUMENT_TYPES)}"
        )

    original_filename = document.filename or ""
    file_extension = Path(original_filename).suffix.lower()

    if not file_extension or file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '{file_extension}' is not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    content = await document.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file cannot be empty (0 byte)"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the maximum limit of 10 MB"
        )

    stored_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = UPLOAD_FOLDER / stored_filename

    with open(file_path, "wb") as output_file:
        output_file.write(content)

    return {
        "success": True,
        "message": "Document uploaded successfully",
        "data": {
            "title": clean_title,
            "course_code": clean_course_code,
            "document_type": clean_doc_type,
            "description": description.strip(),
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "file_path": str(file_path),
        },
    }