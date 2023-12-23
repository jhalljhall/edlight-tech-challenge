from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
import datetime

from app.db.base_class import Base

#? do i need to adjust this to ": Mapped[str]"

class Token(Base):
    __tablename__ = "tokens"

    def get_future_date():
        return datetime.datetime.utcnow() + datetime.timedelta(days=30)

    id = Column(Integer, primary_key=True, index=True)
    user_id = ForeignKey("users.id")
    token_type = Column(String, default="auth")
    access_token = Column(String, default="")
    expires = Column(DateTime, default=get_future_date)
