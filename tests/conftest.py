from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.mocks import mock_valid_deck

mock_supabase_client = MagicMock()
mock_db_session = MagicMock()


@pytest.fixture
def mock_supabase():
    return mock_supabase_client


@pytest.fixture
def mock_db():
    return mock_db_session


@pytest.fixture
def mock_create_deck(mocker):
    mock_deck = mocker.patch(
        "src.decks.router.create_deck",
        new_callable=AsyncMock,
        return_value=mock_valid_deck,
    )
    return mock_deck


@pytest.fixture
def mock_upload_deck(mocker):
    mock_deck = mocker.patch("src.decks.service.upload_deck", new_callable=AsyncMock)
    return mock_deck


@pytest.fixture
def mock_word_list_generation(mocker):
    mock_list = mocker.patch(
        "src.decks.service.word_list_generation",
        new_callable=AsyncMock,
    )
    return mock_list


@pytest.fixture
def mock_get_flash_cards_by_list(mocker):
    mock_flash_cards = mocker.patch(
        "src.decks.service.get_flash_cards_by_list", new_callable=AsyncMock
    )
    return mock_flash_cards


@pytest.fixture
def mock_create_flashcard(mocker):
    mock_flash_card = mocker.patch(
        "src.decks.service.create_flashcard", new_callable=AsyncMock
    )
    return mock_flash_card


@pytest.fixture
def mock_text_generation(mocker):
    mock_text = mocker.patch(
        "src.flashcards.service.text_generation", new_callable=AsyncMock
    )
    return mock_text


@pytest.fixture
def mock_get_or_create_image_with_word(mocker):
    word_image = mocker.patch(
        "src.flashcards.service.get_or_create_image_with_word", new_callable=AsyncMock
    )
    return word_image


@pytest.fixture
def mock_get_word(mocker):
    word = mocker.patch("src.flashcards.service.get_word", new_callable=AsyncMock)
    return word
