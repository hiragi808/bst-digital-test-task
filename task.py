import re
from collections import Counter
import random
random.seed(42) 
# Исходный текст
TEXT = "Во глубине сибирских руд Храните гордое терпенье, Не пропадет ваш скорбный труд И дум высокое стремленье."
PRICE_PER_WORD = 40
EXPRESS_DELIVERY_COST = 2
PENALTY_MISSING_WORDS = 10
STORAGE_COST_PER_LETTER = 1
def evaluate_stock(stock: dict, word_counters: list[Counter]) -> int:
    """Считает суммарную прибыль для заданного склада."""
    days = len(word_counters)
    storage_cost = sum(stock.values()) * days * STORAGE_COST_PER_LETTER
    
    gross_profit = 0

    for wc in word_counters:
        deficit = sum(max(0, count - stock.get(letter, 0)) for letter, count in wc.items())
        if deficit == 0:
            gross_profit += PRICE_PER_WORD
        elif deficit == 1:
            gross_profit += (PRICE_PER_WORD - EXPRESS_DELIVERY_COST)
        else:
            gross_profit -= PENALTY_MISSING_WORDS

    return gross_profit - storage_cost
def optimize_stock(word_counters: list[Counter], letters: list[str], max_need: dict, iterations=500) -> dict:
    """Ищет оптимальный склад методом локального поиска."""
    best_stock = {}
    best_profit = float('-inf')

    for _ in range(iterations):
        # Случайная инициализация
        current_stock = {letter: random.randint(0, max_need[letter]) for letter in letters}
        current_profit = evaluate_stock(current_stock, word_counters)
        
        improved = True
        while improved:
            improved = False
            for letter in letters:
                for delta in (1, -1):
                    new_val = current_stock[letter] + delta
                    if new_val < 0 or new_val > max_need[letter]:
                        continue
                    
                    old_val = current_stock[letter]
                    current_stock[letter] = new_val
                    new_profit = evaluate_stock(current_stock, word_counters)
                    
                    if new_profit > current_profit:
                        current_profit = new_profit
                        improved = True
                    else:
                        current_stock[letter] = old_val

        if current_profit > best_profit:
            best_profit = current_profit
            best_stock = current_stock.copy()

    return {k: v for k, v in best_stock.items() if v > 0}, best_profit
def get_words(text: str) -> list[str]:
    """Очищает текст от пунктуации, приводит к нижнему регистру."""
    words = re.findall(r'[а-яё]+', text.lower())
    return [w.replace('ё', 'е') for w in words]

def main():
    words = get_words(TEXT)
    print(f"Всего слов: {len(words)}")
    
    # Подготовка данных
    word_counters = [Counter(w) for w in words]
    letters = sorted(set(c for wc in word_counters for c in wc))
    
    # Максимальное количество каждой буквы (больше хранить бессмысленно)
    max_need = {letter: max(wc.get(letter, 0) for wc in word_counters) for letter in letters}

    # Запуск оптимизации
    print("Идет поиск оптимального склада...")
    optimal_stock, max_profit = optimize_stock(word_counters, letters, max_need, iterations=200)

    # Красивый вывод
    print("\n" + "="*40)
    print("ОПТИМАЛЬНЫЙ СЛОВАРЬ (СКЛАД):")
    print(optimal_stock)
    print(f"\nСуммарная прибыль за {len(words)} дней: {max_profit} руб.")
    print(f"Средняя прибыль в день: {max_profit / len(words):.2f} руб.")
    print("="*40)

if __name__ == "__main__":
    if len(TEXT) != 0:
       main()
    else: print("Пучсте четверостишие")
