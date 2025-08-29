from datetime import datetime
from uuid import uuid4

from src.core.schemas import WordList
from src.flashcards.models import FlashCard

mock_user_id = uuid4()

mock_valid_image = {"id": uuid4(), "url": "https://example.com/image.png"}

mock_valid_word = {"id": uuid4(), "word": "Hello", "image": mock_valid_image}

mock_valid_flashcard = {
    "id": uuid4(),
    "native_lang": "en",
    "target_lang": "zh",
    "data": {"example": "data"},
    "created_at": datetime.now(),
    "word": mock_valid_word,
}

mock_valid_deck = {
    "id": uuid4(),
    "title": "Fake Deck",
    "created_at": datetime.now(),
    "flashcards": [mock_valid_flashcard],
}

mock_valid_word_list = WordList(
    language="English",
    title="Fruits Vocabulary",
    words=["apple", "banana", "orange", "grape", "pear"],
)

flashcard_mock = FlashCard(
    id=uuid4(),
    word_id=uuid4(),
    native_lang="en",
    target_lang="es",
    data={"example": "data"},
    created_at=datetime.now(),
)
mock_missing_words = ["word1", "word2"]
