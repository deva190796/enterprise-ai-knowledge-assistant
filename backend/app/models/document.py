from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # Original filename shown to user
    original_filename = Column(String(255), nullable=False)

    # UUID filename stored on disk
    filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)