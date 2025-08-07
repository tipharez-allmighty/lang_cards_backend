from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Profile


async def get_profile_by_id(db: AsyncSession, user_id: UUID) -> Profile | None:
    profile = await db.execute(select(Profile).where(Profile.id == user_id))
    return profile.scalar_one_or_none()
