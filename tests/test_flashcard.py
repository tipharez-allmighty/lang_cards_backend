from unittest.mock import patch, AsyncMock
import pytest
import tests.mocks as mocks
from src.flashcards.service import create_flashcard
from src.flashcards.models import Word


# @pytest.mark.parametrize(
#     "missing_words",
#     [(["word1", "word2"]), ([])],
# )
@pytest.mark.asyncio
async def test_create_flashcard(
    mock_supabase,
    mock_db,
    mock_text_generation,
    mock_get_or_create_image_with_word,
    mock_get_word,
):
    with patch("src.flashcards.service.get_db", new_callable=mock_db) as mock_get_db:
        mock_get_db.return_value = mock_get_db
        mock_get_db.__aenter__ = AsyncMock()
        mock_get_db.__aexit__ = AsyncMock()

        mock_text_generation.return_value = mocks.mock_text_data
        mock_get_or_create_image_with_word.return_value = mocks.mock_vaid_word_orm1
        mock_get_word.return_value = mocks.mock_vaid_word_orm2

        flash_card = await create_flashcard(
            mock_supabase,
            "hello",
            mocks.mock_target_lang,
            mocks.mock_native_lang,
        )
    assert flash_card
