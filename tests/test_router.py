# import pytest
# from fastapi.testclient import TestClient
#
# from src.decks.router import router
# from src.main import app
# from tests.mocks import mock_user_id
#
# app.include_router(router)
# client = TestClient(app)
#
#
# @pytest.mark.parametrize(
#     "user_input, native_lang, expected_status",
#     [
#         ("你好，世界", "zh", 200),
#     ],
# )
# def test_generate_deck_parametrized(
#     mock_create_deck, user_input, native_lang, expected_status
# ):
#     response = client.post(
#         "/decks/",
#         json={
#             "user_id": str(mock_user_id),
#             "user_input": user_input,
#             "native_lang": native_lang,
#         },
#     )
#
#     assert response.status_code == expected_status
