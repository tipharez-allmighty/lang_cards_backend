import pytest
from fastapi.testclient import TestClient

from src.decks.router import router
from src.main import app

app.include_router(router)
client = TestClient(app)


@pytest.mark.parametrize(
    "user_input, native_lang, expected_status",
    [
        ("你好，世界", "zh", 200),
        ("Hello, World", "en", 200),
    ],
)
def test_generate_deck_parametrized(
    mock_create_deck, user_input, native_lang, expected_status
):
    response = client.post(
        "/decks/",
        json={
            "user_id": "b6a7e0a0-0000-4100-8000-000000000000",
            "user_input": user_input,
            "native_lang": native_lang,
        },
    )

    assert response.status_code == expected_status
    assert response.status_code == expected_status
    if expected_status == 200:
        mock_create_deck.assert_called_once()
    else:
        mock_create_deck.assert_not_called()
