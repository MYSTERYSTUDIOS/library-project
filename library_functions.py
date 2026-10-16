"""Validation and formatting helpers used by the library application."""
from datetime import date


def validate_year(year):
    if type(year) is not int or not 1000 <= year <= 2100:
        raise ValueError('Год должен быть целым числом от 1000 до 2100')
    return True


def validate_quantity(quantity):
    if type(quantity) is not int or quantity <= 0:
        raise ValueError('Количество должно быть положительным целым числом')
    return True


def validate_student_card(student_card):
    if not isinstance(student_card, str) or not student_card.strip() or len(student_card) > 20:
        raise ValueError('Номер билета: от 1 до 20 символов')
    return True


def calculate_overdue_days(due_date, return_date):
    try:
        due = date.fromisoformat(due_date)
        returned = date.fromisoformat(return_date)
    except (TypeError, ValueError) as exc:
        raise ValueError('Даты должны быть в формате YYYY-MM-DD') from exc
    return max(0, (returned - due).days)


def format_book_title(title, max_length=30):
    if not isinstance(title, str) or not title.strip():
        raise ValueError('Название не может быть пустым')
    if type(max_length) is not int or max_length < 3:
        raise ValueError('Максимальная длина должна быть не меньше 3')
    return title if len(title) <= max_length else title[:max_length - 3] + '...'
