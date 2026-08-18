from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

app = FastAPI(title="LMS Authentication System")

SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}

@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):
    if username not in USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=-5 if expired else 30
    )

    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ (thiếu sub)",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = USERS.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Người dùng không tồn tại",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa hoặc không hoạt động",
        )

    return user

@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user



"""
================ PHẦN 1: PHÁT HIỆN VÀ PHÂN TÍCH LỖ HỔNG ================

1. Vị trí code gây lỗi:
   - Dòng `payload = jwt.get_unverified_claims(token)`: Bỏ qua kiểm tra chữ ký và thời hạn token.
   - Thiếu kiểm tra `user.get("is_active")`: Không chặn tài khoản đã bị khóa/vô hiệu hóa.

2. Lý do jwt.get_unverified_claims() không an toàn:
   - Chỉ giải mã Base64 thô mà không dùng SECRET_KEY để xác thực chữ ký (Signature) và bỏ qua `exp`.
   - Kẻ tấn công có thể tùy ý sửa payload (trường `sub`) để giả mạo tài khoản khác hoặc dùng token hết hạn.

3. Test Cases:
   - TC1 (Token hợp lệ):   Token alice còn hạn            -> Thực tế: 200 OK | Kỳ vọng: 200 OK
   - TC2 (Token hết hạn):  Token alice (expired=True)     -> Thực tế: 200 OK | Kỳ vọng: 401 Unauthorized
   - TC3 (User bị khóa):   Token bob (is_active=False)    -> Thực tế: 200 OK | Kỳ vọng: 403 Forbidden

=========================================================================
"""