import asyncio
import uuid
from datetime import datetime

from supabase import AsyncClient

from src.config import settings


async def upload_image(image_bytes: bytes, supabase: AsyncClient) -> str:
    timestamp = datetime.now()
    path = f"{settings.IMAGE_FOLDER}/{timestamp.strftime('%Y-%m-%d_%H-%M-%S-%f')}-{uuid.uuid4()}.webp"
    response = await supabase.storage.from_(settings.IMAGE_BUCKET).upload(
        file=image_bytes,
        path=path,
        file_options={
            "cache-control": "3600",
            "upsert": "true",
            "contentType": "image/webp",
        },
    )

    return response.path


async def get_image_url(image_path: str, supabase: AsyncClient) -> str:
    public_url = await supabase.storage.from_(settings.IMAGE_BUCKET).get_public_url(
        path=image_path,
        # options={"transform": {"width": 500, "height": 600}},
    )
    return public_url


async def remove_images(image_paths: list[str], supabase: AsyncClient) -> list:
    response = await supabase.storage.from_(settings.IMAGE_BUCKET).remove(
        paths=image_paths
    )
    failed_deletions = []
    for file in response:
        metadata = file.get("metadata")
        if metadata:
            status = metadata.get("httpStatusCode")
            if status and status != 200:
                failed_deletions.append(file)
    return failed_deletions
