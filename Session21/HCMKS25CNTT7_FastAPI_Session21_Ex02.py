import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super_secret_key_rikkei_academy"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token đã hết hạn sử dụng")
    except jwt.InvalidTokenError:
        raise Exception("Token không hợp lệ hoặc chữ ký sai")

token = create_access_token(
    data={
        "sub": "student01@gmail.com",
        "user_id": 1,
        "role": "student"
    },
    expires_minutes=30
)

print(token)
print(decode_access_token(token))

"""Câu hỏi bổ sung
1.Ba phần của JWT là gì?

Gồm 3 phần phân cách bởi dấu chấm (.): Header, Payload, và Signature.

2.Payload của JWT có được mã hóa để che giấu dữ liệu hay không?

Không. Payload chỉ được mã hóa dạng Base64URL (dễ dàng giải mã để đọc dữ liệu), không phải mã hóa bảo mật (Encryption) nên tuyệt đối không lưu dữ liệu nhạy cảm như mật khẩu.

3.Signature có vai trò gì?

Đảm bảo tính toàn vẹn dữ liệu (Data Integrity) và xác thực nguồn gốc; giúp Server kiểm tra xem Token có đúng do chính mình phát hành và có bị thay đổi trên đường truyền hay không.

4.Điều gì xảy ra nếu người dùng tự sửa trường role trong Payload?

Chữ ký Signature mới được tính toán lại sẽ không khớp với Chữ ký cũ do người dùng không có SECRET_KEY. Khi gửi lên Server, hệ thống sẽ phát hiện sai lệch chữ ký, báo lỗi InvalidTokenError và từ chối truy cập ngay lập tức.
    """