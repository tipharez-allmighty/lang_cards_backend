from uuid import UUID, uuid4

from fastapi import APIRouter

from src.decks.schemas import DeckBase
from src.decks.tasks import create_deck_task
from src.broker import result_backend

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.post("/", response_model=DeckBase)
async def generate_deck(
    user_id: UUID = uuid4(),
    user_input: str = "你好，世界",
    native_lang: str = "en",
) -> dict[str, str]:
    task = await create_deck_task.kiq(user_id, user_input, native_lang)
    return {"id": task.task_id}


@router.get("/{task_id}", response_model=DeckBase | dict)
async def get_deck(task_id: str) -> DeckBase | dict:
    result = await result_backend.get_result(task_id)
    if not result.is_ready():
        return {"status": "Processing"}
    return DeckBase.model_validate(result.return_value)
