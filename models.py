from sqlalchemy import Column, Integer, String, Float, Text, Date
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(
        String, default=datetime.datetime.now().strftime("%Y-%m-%d"), nullable=False
    )

    def __repr__(self):
        return f"<Income(id={self.id}, amount={self.amount}, source='{self.source}', category='{self.category}', date='{self.date}')>"


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(
        String, default=datetime.datetime.now().strftime("%Y-%m-%d"), nullable=False
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category='{self.category}', description='{self.description}', date='{self.date}')>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(
        String(255), nullable=False
    )  # Storing hashed passwords recommended

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


if __name__ == "__main__":
    from config import engine

    Base.metadata.create_all(engine)  # Create all tables
    print("Database tables created successfully.")
