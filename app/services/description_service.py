from typing import Optional
from app.model.database import (
    SessionLocal,
    Breed,
    BreedVariant,
    BreedDescription,
    VariantDescription,
)
from app.model.responses import DescriptionMessage


def get_breed_description(breed_name: str) -> Optional[DescriptionMessage]:
    """Get description for a breed by name."""
    db = SessionLocal()
    try:
        breed = db.query(Breed).filter(Breed.breed == breed_name).first()
        if not breed:
            return None

        description = (
            db.query(BreedDescription)
            .filter(BreedDescription.breed_id == breed.id)
            .first()
        )
        if not description:
            return None

        return DescriptionMessage(
            breed=breed_name,
            description_en=description.description_en,
            description_pl=description.description_pl,
        )
    finally:
        db.close()


def get_variant_description(breed_name: str, variant_name: str) -> Optional[DescriptionMessage]:
    """Get description for a variant by breed and variant name."""
    db = SessionLocal()
    try:
        breed = db.query(Breed).filter(Breed.breed == breed_name).first()
        if not breed:
            return None

        variant = (
            db.query(BreedVariant)
            .filter(BreedVariant.breed_id == breed.id, BreedVariant.variant == variant_name)
            .first()
        )
        if not variant:
            return None

        description = (
            db.query(VariantDescription)
            .filter(VariantDescription.variant_id == variant.id)
            .first()
        )
        if not description:
            return None

        return DescriptionMessage(
            breed=breed_name,
            variant=variant_name,
            description_en=description.description_en,
            description_pl=description.description_pl,
        )
    finally:
        db.close()
