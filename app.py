"""Консольная информационная система студенческой библиотеки."""
import sqlite3
import database as db

MENU = """
СТУДЕНЧЕСКАЯ БИБЛИОТЕКА
 1 Книги                 2 Поиск по автору
 3 Читатели              4 Все выдачи
 5 Добавить книгу        6 Изменить книгу       7 Удалить книгу
 8 Выдать книгу          9 Вернуть книгу
10 Добавить читателя    11 Изменить читателя  12 Удалить читателя
13 Должники             14 Популярные книги   15 История книги
16 Статистика           17 Активные читатели
18 Экспорт книг CSV     19 Экспорт должников TXT  20 Резервная копия
 0 Выход
"""

def number(label): return int(input(label + ': '))
def show(rows):
    for row in rows: print(' | '.join(f'{k}: {v}' for k,v in row.items()))
    if not rows: print('Записей нет')
def book_fields():
    return input('Название: '), input('Автор: '), number('Год'), number('Количество')
def reader_fields():
    return input('Фамилия: '), input('Имя: '), input('Студбилет: '), input('Группа: '), input('Телефон: ')

def main():
    db.init_database()
    while True:
        print(MENU); choice=input('Выбор: ').strip()
        try:
            if choice=='0': return
            elif choice=='1': show(db.get_all_books())
            elif choice=='2': show(db.get_books_by_author(input('Автор: ')))
            elif choice=='3': show(db.get_all_readers())
            elif choice=='4': show(db.get_all_issues())
            elif choice=='5': print('ID:',db.add_book(*book_fields()))
            elif choice=='6': print('Изменено:',db.edit_book(number('ID книги'),*book_fields()))
            elif choice=='7': print('Удалено:',db.delete_book(number('ID книги')))
            elif choice=='8': print('ID выдачи:',db.issue_book(number('ID книги'),number('ID читателя'),number('Срок в днях')))
            elif choice=='9': print('Возвращено:',db.return_book(number('ID выдачи')))
            elif choice=='10': print('ID:',db.add_reader(*reader_fields()))
            elif choice=='11': print('Изменено:',db.edit_reader(number('ID читателя'),*reader_fields()))
            elif choice=='12': print('Удалено:',db.delete_reader(number('ID читателя')))
            elif choice=='13': show(db.get_debtors())
            elif choice=='14': show(db.get_most_popular_books())
            elif choice=='15': show(db.get_book_history(number('ID книги')))
            elif choice=='16': print(db.get_library_stats())
            elif choice=='17': show(db.get_active_readers())
            elif choice=='18': print('Сохранено:',db.export_books_to_csv())
            elif choice=='19': print('Сохранено:',db.export_debtors_to_txt())
            elif choice=='20': print('Сохранено:',db.backup_database())
            else: print('Неизвестный пункт')
        except (ValueError, sqlite3.Error) as e: print('Ошибка:',e)

if __name__=='__main__': main()
