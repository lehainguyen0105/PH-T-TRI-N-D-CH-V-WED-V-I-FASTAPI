import bcrypt

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes= bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password:str, hash_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')
    hash_bytes = hash_password.encode('uft-8')
    return bcrypt.checkpw(plain_bytes, hash_bytes)

password ="Rikkei@123"

hashed_password = hash_password(password)
print(hashed_password)
print(verify_password("Rikkei@123", hashed_password))
print(verify_password("Rikkei@456", hashed_password))


"""Câu hỏi bổ sung:
1.Vì sao không nên lưu mật khẩu trực tiếp vào database?
Tránh rò rỉ mật khẩu gốc của người dùng nếu database bị hack hoặc lộ file backup.

2.Vì sao cùng một mật khẩu nhưng hai lần băm ra kết quả khác nhau?
Do mỗi lần băm, thuật toán tự động tạo ra một chuỗi ngẫu nhiên (Salt) khác nhau nối vào mật khẩu.

3.Salt có tác dụng gì trong việc chống Rainbow Table?
Làm thay đổi chuỗi hash đầu ra, khiến hacker không thể tra cứu mật khẩu trong bảng tính sẵn (Rainbow Table) có sẵn.
    """