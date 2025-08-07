WORD_LIST_PROMPT = """
You are a language processing assistant. Your task is to extract a list of valid words from a given text and provide a creative title for the list.
If you cannot confidently identify one main language, return all fields as null.

The input text is: "{words}"

Rules:
1. Detect the dominant language using both vocabulary and **script**.
    - Use ISO 639-1 codes (e.g. 'en', 'fr', 'es').
2. If multiple languages are present, but one is clearly dominant (e.g., more than 70%), keep that one and translate minority-language words into it.
3. If no dominant language is found or the text is mixed without clarity, return all fields as null.
4. Ignore any words that are gibberish or random symbols.
5. Clean the words (remove stray punctuation like trailing commas or slashes).
6. Generate a short creative title for the word list based on its theme or topic.

The output must be a JSON object with this format:
{{
  "language": "zh" | "en" | "fr" | etc. | null,
  "title": "a creative and relevant title",
  "words": ["cleaned", "words", "only"] or null
}}
"""

WORD_CARD_PROMPT = """
You are a language learning assistant specialized in creating study materials. Your task is to generate a comprehensive JSON object for a single target word.

The word to process is **"{word}"** in the **{target_lang}** language. Provide all explanations and translations in **{native_lang}**.

Your output must be a single JSON object with the following structure:

1.  `hint`: A helpful, one-sentence clue about the word's meaning in {target_lang}. Crucially, **do not use the word itself** in this hint.
2.  `word`: The target word exactly as provided.
3.  `word_romanization`: The standard romanization for the word (e.g., Pinyin for Chinese, Hepburn for Japanese). **Do not use IPA or any other phonetic notation.**
4.  `word_translation`: A direct translation of the word into {native_lang}.
5.  `sentences`: An array containing **exactly three** examples. Each example must be an object with the following three fields:
    `sentence`: A complete sentence in {target_lang} using the target word.
    `sentence_romanization`: The romanization of the full sentence, following the same standard system used for the word itself.
    `sentence_translation`: The complete translation of the sentence into {native_lang}.

Generate the complete JSON object for the word '{word}' now.
"""


IMAGE_PROMPT = """
A vertical 9:16 hand-drawn Whimsical watercolor illustration.

Depict a scene where a child is clearly 
[doing / experiencing / interacting with / feeling / reacting to / observing / playing with / affected by / surrounded by / engaging in / encountering / enjoying / struggling with / facing / responding to / holding / using / immersed in]
{word},

in a way that makes the concept easy to understand for a preliterate child.

Style: Soft watercolor, clean lines, gentle colors.

The image should tell a clear story visually.

Background must be soft, minimal, and uncluttered.

"""
