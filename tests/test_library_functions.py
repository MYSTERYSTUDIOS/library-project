import pytest
from library_functions import validate_year, validate_quantity, validate_student_card, calculate_overdue_days, format_book_title

@pytest.mark.parametrize('year', [1000, 1869, 2026, 2100])
def test_year_valid(year):
    assert validate_year(year)

@pytest.mark.parametrize('year', [999, 2101, '2000', None, True])
def test_year_invalid(year):
    with pytest.raises(ValueError):
        validate_year(year)

@pytest.mark.parametrize('quantity', [0, -1, 1.5, '2', True])
def test_quantity_invalid(quantity):
    with pytest.raises(ValueError):
        validate_quantity(quantity)

def test_card_empty():
    with pytest.raises(ValueError):
        validate_student_card('  ')

def test_overdue():
    assert calculate_overdue_days('2026-10-01', '2026-10-06') == 5
    assert calculate_overdue_days('2026-10-01', '2026-09-30') == 0

def test_title_truncation():
    assert format_book_title('А' * 40, 30) == 'А' * 27 + '...'
