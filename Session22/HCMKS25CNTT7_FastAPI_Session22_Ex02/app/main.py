from fastapi import FastAPI
from app.core.config import settings
from app.db.session import Base, engine
from app.router import auth, prescription

# Khởi tạo bảng cơ sở dữ liệu
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Đăng ký Router
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(prescription.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "service": "MedCare E-Prescription Core"}


