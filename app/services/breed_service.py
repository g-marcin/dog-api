from pathlib import Path
from typing import Dict, List
import config

def scan_breeds() -> Dict[str, List[str]]:
    breeds = {}
    if not config.ASSETS_DIR.exists():
        return breeds
    
    for breed_dir in config.ASSETS_DIR.iterdir():
        if not breed_dir.is_dir():
            continue
        
        breed_name = breed_dir.name
        sub_breeds = []
        
        for item in breed_dir.iterdir():
            if item.is_dir():
                sub_breeds.append(item.name)
        
        breeds[breed_name] = sub_breeds if sub_breeds else []
    
    return breeds

def get_breed_images(breed: str, sub_breed: str = None) -> List[Path]:
    breed_path = config.ASSETS_DIR / breed
    
    if not breed_path.exists():
        return []
    
    images = []
    
    if sub_breed:
        sub_breed_path = breed_path / sub_breed
        if sub_breed_path.exists() and sub_breed_path.is_dir():
            images.extend([item for item in sub_breed_path.iterdir() if item.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    else:
        for item in breed_path.iterdir():
            if item.is_file() and item.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                images.append(item)
            elif item.is_dir():
                for img in item.rglob('*'):
                    if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        images.append(img)
    
    return images

def get_image_url(image_path: Path) -> str:
    relative_path = image_path.relative_to(config.ASSETS_DIR)
    return f"{config.BASE_URL_IMG}/images/{relative_path.as_posix()}"

def get_all_images() -> List[Path]:
    all_images = []
    
    for breed_dir in config.ASSETS_DIR.iterdir():
        if not breed_dir.is_dir():
            continue
        
        images = get_breed_images(breed_dir.name)
        all_images.extend(images)
    
    return all_images

