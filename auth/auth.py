from passlib.context import CryptContext
from db.database import SessionLocal, User

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def register_user(username, password):
    db = SessionLocal()
    hashed = hash_password(password)

    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.close()

def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if user and verify_password(password, user.password):
        return user
    return None