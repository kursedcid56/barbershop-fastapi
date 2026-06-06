from passlib.context import CryptContext

# Khai báo thuật toán băm là bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tạo một hàm chuyên dùng để băm mật khẩu
def hash_password(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)