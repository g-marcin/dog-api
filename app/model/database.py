import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

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


class BreedDescription(Base):
    __tablename__ = "breed_descriptions"

    id = Column(Integer, primary_key=True)
    breed_id = Column(Integer, ForeignKey("breeds.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    description_en = Column(Text, nullable=False)
    description_pl = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    breed = relationship("Breed")


class VariantDescription(Base):
    __tablename__ = "variant_descriptions"

    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey("breed_variants.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    description_en = Column(Text, nullable=False)
    description_pl = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    variant = relationship("BreedVariant")


