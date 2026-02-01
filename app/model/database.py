import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    breed = Column(String(64), nullable=False, unique=True, index=True)
    variants = relationship("BreedVariant", back_populates="breed")

class BreedVariant(Base):
    __tablename__ = "breed_variants"

    id = Column(Integer, primary_key=True)
    breed_id = Column(Integer, ForeignKey("breeds.id"), nullable=False, index=True)
    variant = Column(String(64), nullable=False, index=True)
    breed = relationship("Breed", back_populates="variants")


