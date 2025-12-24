from datetime import datetime
from uuid import uuid4

from src.core.schemas import WordList, FlashCardLLM, Sentences
from src.decks.schemas import DeckBase
from src.flashcards.schemas import FlashCardBase, ImageBase, WordBase
from src.flashcards.models import Word, Image

mock_user_id = uuid4()

mock_valid_image1 = ImageBase(id=uuid4(), url="https://example.com/image1.png")
mock_valid_image2 = ImageBase(id=uuid4(), url="https://example.com/image2.png")


mock_valid_word1 = WordBase(id=uuid4(), word="Hello", image=mock_valid_image1)
mock_valid_word2 = WordBase(id=uuid4(), word="World", image=mock_valid_image2)

mock_valid_image_orm1 = Image(**mock_valid_image1.model_dump(), path="/path1")
mock_valid_image_orm2 = Image(**mock_valid_image2.model_dump(), path="/path2")
mock_vaid_word_orm1 = Word(word=mock_valid_word1.word, image=mock_valid_image_orm1)
mock_vaid_word_orm2 = Word(word=mock_valid_word2.word, image=mock_valid_image_orm2)

mock_missing_words = ["word1", "word2"]

mock_user_input = "Hello, World"
mock_native_lang = "en"
mock_target_lang = "zh"

mock_valid_flashcards = [
    FlashCardBase(
        id=uuid4(),
        native_lang=mock_native_lang,
        target_lang=mock_target_lang,
        data={"example": "data"},
        created_at=datetime.now(),
        word=mock_valid_word1,
    ),
    FlashCardBase(
        id=uuid4(),
        native_lang=mock_native_lang,
        target_lang=mock_target_lang,
        data={"example": "data"},
        created_at=datetime.now(),
        word=mock_valid_word2,
    ),
]

mock_valid_deck = DeckBase(
    id=uuid4(),
    title="Fake Deck",
    created_at=datetime.now(),
    flashcards=mock_valid_flashcards,
)

mock_valid_word_list = WordList(
    language="English",
    title="Fruits Vocabulary",
    words=["apple", "banana", "orange", "grape", "pear"],
)

mock_text_data = FlashCardLLM(
    hint="A common fruit",
    word="apple",
    word_romanization="píngguǒ",
    word_translation="蘋果",
    sentences=[
        Sentences(
            sentence="I like apples.",
            sentence_romanization="Wǒ xǐhuān píngguǒ.",
            sentence_translation="我喜歡蘋果。",
        )
    ],
)
