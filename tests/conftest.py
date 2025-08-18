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
