"""Лабораторна робота 5: класи Fruit і FruitSalad.

Модуль містить класи для опису фруктів і фруктового салату
з автоматичним вибором топінгу за смаком фруктів.
"""

import random
from collections import Counter
from enum import Enum


class Taste(Enum):
    """Смак."""

    SWEET = "солодкий"
    SOUR = "кислий"
    NEUTRAL = "нейтральний"


class Topping(Enum):
    """Топінг та його характеристика."""

    HONEY = ("Мед", Taste.SWEET)
    LEMON_JUICE = ("Лимонний сік", Taste.SOUR)
    YOGURT = ("Йогурт", Taste.NEUTRAL)

    def __init__(self, title, taste):
        self._title = title
        self._taste = taste

    @property
    def title(self):
        """Повертає назву топінгу."""
        return self._title

    @property
    def taste(self):
        """Повертає смак топінгу."""
        return self._taste


class Fruit:
    """Фрукт з назвою, розміром, кольором і смаком."""

    def __init__(self, name, size, color, taste):
        """Конструктор перебирає дані через сеттери."""
        self.name = name
        self.size = size
        self.color = color
        self.taste = taste
        print(f"[+] Створено фрукт: {self.name}")

    def __del__(self):
        """Деструктор фрукта."""
        print(f"[-] Видалено фрукт: {getattr(self, '_name', 'невідомо')}")

    @property
    def name(self):
        """Повертає назву фрукта."""
        return self._name

    @name.setter
    def name(self, value):
        """Встановлює назву фрукта."""
        if not isinstance(value, str):
            raise TypeError("Назва має бути рядком")
        if not value.strip():
            raise ValueError("Назва не може бути порожньою")
        self._name = value

    @property
    def size(self):
        """Повертає розмір фрукта."""
        return self._size

    @size.setter
    def size(self, value):
        """Встановлює розмір фрукта."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Розмір має бути числом")
        if value <= 0:
            raise ValueError("Розмір має бути додатним")
        self._size = value

    @property
    def color(self):
        """Повертає колір фрукта."""
        return self._color

    @color.setter
    def color(self, value):
        """Встановлює колір фрукта."""
        if not isinstance(value, str):
            raise TypeError("Колір має бути рядком")
        if not value.strip():
            raise ValueError("Колір не може бути порожнім")
        self._color = value

    @property
    def taste(self):
        """Повертає смак фрукта."""
        return self._taste

    @taste.setter
    def taste(self, value):
        """Встановлює смак фрукта."""
        if not isinstance(value, Taste):
            raise TypeError("Смак має бути елементом Taste")
        self._taste = value

    def __str__(self):
        """Повертає текстовий опис фрукта."""
        return f"{self.name}, {self.size} см, {self.color}, {self.taste.value}"

    def display(self):
        """Виводить інформацію про фрукт."""
        print(self)


class FruitSalad:
    """Фруктовий салат з набору фруктів і топінгу."""

    def __init__(self, fruits=None, topping=None):
        """Конструктор: список фруктів і топінг необов'язкові."""
        self._fruits = []
        for fruit in fruits or []:
            self.add_fruit(fruit)
        self.topping = topping
        print("[+] Створено салат")

    def __del__(self):
        """Деструктор салату."""
        print("[-] Видалено салат")

    @property
    def fruits(self):
        """Повертає копію списку фруктів."""
        return list(self._fruits)

    @property
    def topping(self):
        """Повертає топінг (або None)."""
        return self._topping

    @topping.setter
    def topping(self, value):
        """Встановлює топінг салату."""
        if value is not None and not isinstance(value, Topping):
            raise TypeError("Топінг має бути елементом Topping")
        self._topping = value

    def add_fruit(self, fruit):
        """Додає фрукт до салату."""
        if not isinstance(fruit, Fruit):
            raise TypeError("Додавати можна лише об'єкти Fruit")
        self._fruits.append(fruit)

    def choose_topping(self):
        """Обирає топінг, який врівноважує смак фруктів.

        Більше кислих: мед. Більше солодких: лимонний сік.
        Порівну (або домінують нейтральні): йогурт.
        """
        counts = Counter(fruit.taste for fruit in self._fruits)
        if counts[Taste.SOUR] > counts[Taste.SWEET]:
            self.topping = Topping.HONEY
        elif counts[Taste.SWEET] > counts[Taste.SOUR]:
            self.topping = Topping.LEMON_JUICE
        else:
            self.topping = Topping.YOGURT
        return self._topping

    def shuffle(self):
        """Перемішує фрукти у випадковому порядку."""
        random.shuffle(self._fruits)

    def display(self):
        """Виводить склад салату."""
        print("Фруктовий салат:")
        for number, fruit in enumerate(self._fruits, start=1):
            print(f"  {number}. {fruit}")
        topping = self._topping
        if topping is None:
            print("  Топінг: відсутній")
        else:
            print(f"  Топінг: {topping.title} ({topping.taste.value})")


def main():
    """Демонстрація роботи класів."""
    apple = Fruit("яблуко", 8, "червоний", Taste.SWEET)
    lemon = Fruit("лимон", 6, "жовтий", Taste.SOUR)
    kiwi = Fruit("ківі", 5, "зелений", Taste.SOUR)
    banana = Fruit("банан", 18, "жовтий", Taste.NEUTRAL)

    print("\n--- Функції доступу ---")
    apple.display()
    banana.color = "світло-жовтий"
    print(f"Новий колір банана: {banana.color}")

    print("\n--- Перевірка валідації ---")
    try:
        Fruit("слива", -3, "синій", Taste.SWEET)
    except ValueError as error:
        print(f"Помилка: {error}")
    try:
        Fruit(None, 5, "синій", Taste.SWEET)
    except TypeError as error:
        print(f"Помилка: {error}")
    try:
        Fruit("слива", "5", "синій", Taste.SWEET)
    except TypeError as error:
        print(f"Помилка: {error}")
    try:
        FruitSalad(["не фрукт"])
    except TypeError as error:
        print(f"Помилка: {error}")

    print("\n--- Салат ---")
    salad = FruitSalad([apple, lemon, kiwi])
    salad.add_fruit(banana)
    salad.display()

    print("\n--- Вибір топінгу ---")
    chosen = salad.choose_topping()
    print(f"Обрано: {chosen.title}")
    salad.display()

    print("\n--- Перемішування ---")
    salad.shuffle()
    salad.display()

    print("\n--- Деструктори ---")
    del salad
    del apple, lemon, kiwi, banana
    print("Кінець програми")


if __name__ == "__main__":
    main()
