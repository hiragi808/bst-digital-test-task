import re
from collections import Counter
import random

# Исходный текст
TEXT = "Во глубине сибирских руд Храните гордое терпенье, Не пропадет ваш скорбный труд И дум высокое стремленье."

def get_words(text: str) -> list[str]:
    """Очищает текст от пунктуации, приводит к нижнему регистру."""
    words = re.findall(r'[а-яё]+', text.lower())
    return [w.replace('ё', 'е') for w in words]

if __name__ == "__main__":
    words = get_words(TEXT)
    print(f"Найдено слов: {len(words)}")
    print(words)
