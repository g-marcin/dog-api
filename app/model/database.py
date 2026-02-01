from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.sql import func

from config import (
    DB_POSTGRES_URL,
    DB_POOL_SIZE,
    DB_MAX_OVERFLOW,
    DB_POOL_RECYCLE,
    DB_POOL_PRE_PING,
    DB_PGBOUNCER_MODE,
)


def create_db_engine():
    """
    Create SQLAlchemy engine with connection pooling configured for PgBouncer.

    - transaction mode: Use NullPool (PgBouncer handles pooling)
    - session mode: Use QueuePool with configured pool settings
    """
    if DB_PGBOUNCER_MODE == "transaction":
        # PgBouncer in transaction mode handles connection pooling
        # Use NullPool to avoid double-pooling
        return create_engine(
            DB_POSTGRES_URL,
            poolclass=NullPool,
            echo=False,
        )
    else:
        # PgBouncer in session mode or direct PostgreSQL connection
        # Use QueuePool with connection pooling settings
        return create_engine(
            DB_POSTGRES_URL,
            poolclass=QueuePool,
            pool_size=DB_POOL_SIZE,
            max_overflow=DB_MAX_OVERFLOW,
            pool_recycle=DB_POOL_RECYCLE,
            pool_pre_ping=DB_POOL_PRE_PING,
            echo=False,
        )


engine = create_db_engine()
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


