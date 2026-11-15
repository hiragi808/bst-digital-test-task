import re
from collections import Counter
import random

# Исходный текст
TEXT = "Во глубине сибирских руд Храните гордое терпенье, Не пропадет ваш скорбный труд И дум высокое стремленье."

def evaluate_stock(stock: dict, word_counters: list[Counter]) -> int:
    """Считает суммарную прибыль для заданного склада."""
    storage_cost = sum(stock.values()) # 1 рубль за каждую букву
    gross_profit = 0

    for wc in word_counters:
        # Считаем, сколько букв не хватает
        deficit = sum(max(0, count - stock.get(letter, 0)) for letter, count in wc.items())
        
        if deficit == 0:
            gross_profit += 40
        elif deficit == 1:
            gross_profit += 38
        else:
            gross_profit -= 10

    return gross_profit - storage_cost
    
def get_words(text: str) -> list[str]:
    """Очищает текст от пунктуации, приводит к нижнему регистру."""
    words = re.findall(r'[а-яё]+', text.lower())
    return [w.replace('ё', 'е') for w in words]

if __name__ == "__main__":
    words = get_words(TEXT)
    print(f"Найдено слов: {len(words)}")
    print(words)
