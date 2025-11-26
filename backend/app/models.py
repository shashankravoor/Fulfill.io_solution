from sqlalchemy import Column, Integer, String, Numeric, Text, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(128), unique=True, index=True, nullable=False)
    name = Column(String(512), nullable=False)
    description = Column(Text)
    # price = Column(Numeric(10,2))
    available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
