import pytest
import tests.mocks as mocks
from src.decks.service import create_deck


@pytest.mark.parametrize(
    "missing_words",
    [(["word1", "word2"]), ([])],
)
@pytest.mark.asyncio
async def test_create_deck(
    mock_db,
    mock_supabase,
    mock_word_list_generation,
    mock_get_flash_cards_by_list,
    mock_create_flashcard,
    mock_upload_deck,
    missing_words,
):
    mock_word_list_generation.return_value = mocks.mock_valid_word_list
    mock_get_flash_cards_by_list.return_value = (
        [mocks.mock_valid_flashcard],
        missing_words,
    )
    mock_upload_deck.return_value = mocks.mock_valid_deck

    deck = await create_deck(
        mock_db, mock_supabase, mocks.mock_user_id, "Hello, World", "eng"
    )

    assert deck == mock_upload_deck.return_value

    mock_word_list_generation.assert_awaited_once()
    mock_get_flash_cards_by_list.assert_awaited_once()
    if mock_get_flash_cards_by_list.return_value[1]:
        mock_create_flashcard.assert_awaited()
    else:
        mock_create_flashcard.assert_not_awaited()
