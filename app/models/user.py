#import sqlalchemy as sa
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import text
from typing import List
from app.schemas.user import UserInDB
from app.db.base_class import Base

#USER MODEL - PARENT
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(Boolean(), default=True)
    is_superuser: Mapped[bool] = Column(Boolean(), default=False)
    # add to given user model...
    created: Mapped[DateTime] = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    # where a profile pic would be added ---> profile_pic = Column()

# relationship

    def to_schema(self):
        
        return UserInDB(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            # add to given user schema
            created_timestamp=self.created_timestamp
        )
