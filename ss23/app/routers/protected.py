from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user, RoleChecker

router = APIRouter(
    prefix="/api/protected",
    tags=["Protected Routes (Phân quyền)"]
)

# --- ENDPOINT 1: Dành cho tất cả người dùng đã đăng nhập ---
@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Bất kỳ ai có Token hợp lệ đều có thể xem thông tin cá nhân của chính mình.
    """
    return {
        "message": "Xác thực thành công!",
        "user_info": {
            "id": current_user.id,
            "email": current_user.email,
            # user.role là object Role, dùng .name để lấy chuỗi tên role
            "role": current_user.role.name if current_user.role else None
        }
    }

# --- ENDPOINT 2: Chỉ dành cho Quản trị viên (Admin) ---
# RoleChecker(["admin"]) --> chỉ user có role "admin" mới được vào
@router.get("/admin/dashboard")
async def get_admin_dashboard(current_user: User = Depends(RoleChecker(["admin"]))):
    """
    Chỉ tài khoản 'admin' mới có quyền truy cập trang quản trị hệ thống.
    RoleChecker tự động kiểm tra và chặn, không cần viết if/raise bên trong.
    """
    return {
        "status": "success",
        "message": "Chào mừng Admin!",
        "secret_data": "Đây là dữ liệu tuyệt mật chỉ Admin mới thấy."
    }

# --- ENDPOINT 3: Dành cho Admin HOẶC Manager ---
# RoleChecker(["admin", "manager"]) --> cả 2 role đều được vào
@router.get("/reports")
async def get_reports(current_user: User = Depends(RoleChecker(["admin", "manager"]))):
    """
    Cả Admin và Manager đều có thể xem báo cáo.
    Đây là điểm mạnh của RoleChecker: chỉ 1 dòng, support nhiều role cùng lúc.
    """
    return {
        "status": "success",
        "message": f"Xin chào {current_user.email}! Đây là trang báo cáo.",
        "report_data": "Doanh thu tháng 8: 150,000,000 VND"
    }

