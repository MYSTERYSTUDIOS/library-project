from database import init_database
from books import get_all_books, add_book, search_books
from readers import get_all_readers, add_reader
from issues import issue_book, return_book, get_all_issues
from reports import get_library_stats, get_most_popular_books

def main():
    init_database()
    actions = {
      '1': lambda: print(*get_all_books(), sep='\n'),
      '2': lambda: print(*get_all_readers(), sep='\n'),
      '3': lambda: print('ID:', add_book(input('Название: '), input('Автор: '), int(input('Год: ')), int(input('Экземпляров: ')))),
      '4': lambda: print('ID:', add_reader(input('Фамилия: '), input('Имя: '), input('Билет: '), input('Группа: '))),
      '5': lambda: print('Выдача:', issue_book(int(input('ID книги: ')), int(input('ID читателя: ')))),
      '6': lambda: print('Возврат:', return_book(int(input('ID выдачи: ')))),
      '7': lambda: print(*get_all_issues(), sep='\n'),
      '8': lambda: print(get_library_stats()),
      '9': lambda: print(*get_most_popular_books(), sep='\n'),
      '10': lambda: print(*search_books(input('Поиск: ')), sep='\n'),
    }
    while True:
      print('\nСТУДЕНЧЕСКАЯ БИБЛИОТЕКА | 1 Книги | 2 Читатели | 3 Добавить книгу | 4 Добавить читателя | 5 Выдать | 6 Вернуть | 7 Выдачи | 8 Статистика | 9 Популярные | 10 Поиск | 0 Выход')
      choice = input('Пункт: ').strip()
      if choice == '0': break
      try:
        actions.get(choice, lambda: print('Нет такого пункта'))()
      except (ValueError, TypeError) as exc:
        print('Ошибка ввода:', exc)

if __name__ == '__main__':
    main()
