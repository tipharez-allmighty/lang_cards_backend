from uuid import UUID, uuid4

from fastapi import APIRouter
from taskiq.depends.progress_tracker import TaskState

from src.decks.schemas import Task, TaskResult
from src.decks.tasks import create_deck_task
from src.broker import result_backend
from src.logger import logger

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.post("/", response_model=Task)
async def generate_deck(
    user_id: UUID = uuid4(),
    user_input: str = "你好，世界",
    native_lang: str = "en",
) -> Task:
    task = await create_deck_task.kiq(user_id, user_input, native_lang)
    return Task(id=task.task_id)


@router.get("/{task_id}", response_model=TaskResult)
async def get_deck(task_id: str) -> TaskResult:
    task_result = await result_backend.get_result(task_id)
    if task_result:
        logger.info(f"SUCCESS: Result found for {task_id}")
        status = TaskState.SUCCESS if not task_result.is_err else TaskState.FAILURE
        return TaskResult(status=status, result=task_result.return_value)
    progress = await result_backend.get_progress(task_id)
    if progress:
        status = progress.state
        logger.info(f"PROGRESS: Task {task_id} state is {status}")
        try:
            status = TaskState(status)
        except ValueError:
            status = TaskState.FAILURE
        return TaskResult(status=status)

    logger.info(f"STARTED: No data in Redis for {task_id}")
    return TaskResult(status=TaskState.STARTED)
