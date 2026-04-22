from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///kundali.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(Text)
    response = Column(Text)

def save_chat(user_id, msg, res):
    db = SessionLocal()
    chat = ChatHistory(user_id=user_id, message=msg, response=res)
    db.add(chat)
    db.commit()
    db.close()

def get_chat_history(user_id):
    db = SessionLocal()
    chats = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).all()
    db.close()

    return [(c.message, c.response) for c in chats]
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Kundali(Base):
    __tablename__ = "kundali"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    birth_data = Column(Text)
    chart_data = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
    
