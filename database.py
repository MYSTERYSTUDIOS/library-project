"""SQLite data access for the student library project."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('library.db')


def get_connection(db_path=None):
    conn = sqlite3.connect(str(db_path or DB_PATH))
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path=None):
    with get_connection(db_path) as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL CHECK(length(trim(title)) > 0),
            author TEXT NOT NULL CHECK(length(trim(author)) > 0),
            year INTEGER CHECK(year BETWEEN 1000 AND 2100),
            quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0)
        );
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            student_card TEXT NOT NULL UNIQUE,
            group_name TEXT,
            phone TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL REFERENCES books(id),
            reader_id INTEGER NOT NULL REFERENCES readers(id),
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'выдана'
                CHECK(status IN ('выдана', 'возвращена'))
        );
        ''')


def add_book(title, author, year, quantity=1, db_path=None):
    from library_functions import validate_year, validate_quantity
    if not title or not title.strip() or not author or not author.strip():
        raise ValueError('Название и автор обязательны')
    validate_year(year)
    validate_quantity(quantity)
    with get_connection(db_path) as conn:
        return conn.execute('INSERT INTO books(title,author,year,quantity) VALUES(?,?,?,?)',
                            (title.strip(), author.strip(), year, quantity)).lastrowid


def add_reader(last_name, first_name, student_card, group_name='', phone='', db_path=None):
    from library_functions import validate_student_card
    validate_student_card(student_card)
    if not last_name.strip() or not first_name.strip():
        raise ValueError('Имя и фамилия обязательны')
    with get_connection(db_path) as conn:
        return conn.execute('''INSERT INTO readers(last_name,first_name,student_card,group_name,phone)
                              VALUES(?,?,?,?,?)''',
                            (last_name.strip(), first_name.strip(), student_card.strip(), group_name, phone)).lastrowid


def search_books(query='', db_path=None):
    with get_connection(db_path) as conn:
        return [dict(row) for row in conn.execute(
            'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY title',
            (f'%{query}%', f'%{query}%'))]


def list_readers(db_path=None):
    with get_connection(db_path) as conn:
        return [dict(row) for row in conn.execute('SELECT * FROM readers ORDER BY last_name,first_name')]


# Functions for labs 3–6. All SQL statements use parameters.
from datetime import date, timedelta
import csv
import shutil


def get_all_books(db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM books ORDER BY id')]


def get_books_by_author(author, db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute('SELECT * FROM books WHERE author LIKE ? ORDER BY title', ('%' + author + '%',))]


def get_all_readers(db_path=None):
    return list_readers(db_path)


def get_all_issues(db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute("""SELECT i.*, b.title AS book_title,
             r.last_name || ' ' || r.first_name AS reader_name
             FROM issues i JOIN books b ON b.id=i.book_id
             JOIN readers r ON r.id=i.reader_id ORDER BY i.id DESC""")]


def edit_book(book_id, title, author, year, quantity, db_path=None):
    from library_functions import validate_year, validate_quantity
    validate_year(year); validate_quantity(quantity)
    if not title.strip() or not author.strip(): raise ValueError('Укажите название и автора')
    with get_connection(db_path) as conn:
        active = conn.execute("SELECT COUNT(*) FROM issues WHERE book_id=? AND return_date IS NULL", (book_id,)).fetchone()[0]
        if quantity < active: raise ValueError('Количество меньше числа выданных экземпляров')
        return conn.execute('UPDATE books SET title=?,author=?,year=?,quantity=? WHERE id=?',
                            (title.strip(),author.strip(),year,quantity,book_id)).rowcount


def delete_book(book_id, db_path=None):
    with get_connection(db_path) as conn:
        return conn.execute('DELETE FROM books WHERE id=?', (book_id,)).rowcount


def issue_book(book_id, reader_id, days=14, db_path=None, issue_date=None):
    if type(days) is not int or days < 1: raise ValueError('Срок выдачи должен быть положительным')
    issued = date.fromisoformat(issue_date) if issue_date else date.today()
    with get_connection(db_path) as conn:
        book=conn.execute('SELECT quantity FROM books WHERE id=?',(book_id,)).fetchone()
        if book is None: raise ValueError('Книга не найдена')
        if conn.execute('SELECT 1 FROM readers WHERE id=?',(reader_id,)).fetchone() is None:
            raise ValueError('Читатель не найден')
        active=conn.execute('SELECT COUNT(*) FROM issues WHERE book_id=? AND return_date IS NULL',(book_id,)).fetchone()[0]
        if active >= book['quantity']: raise ValueError('Нет доступных экземпляров')
        return conn.execute("""INSERT INTO issues(book_id,reader_id,issue_date,due_date,status)
            VALUES(?,?,?,?,?)""",(book_id,reader_id,issued.isoformat(),(issued+timedelta(days=days)).isoformat(),'выдана')).lastrowid


def return_book(issue_id, db_path=None, return_date=None):
    returned=date.fromisoformat(return_date) if return_date else date.today()
    with get_connection(db_path) as conn:
        issue=conn.execute('SELECT issue_date,return_date FROM issues WHERE id=?',(issue_id,)).fetchone()
        if issue is None: raise ValueError('Выдача не найдена')
        if issue['return_date'] is not None: raise ValueError('Книга уже возвращена')
        if returned < date.fromisoformat(issue['issue_date']): raise ValueError('Возврат раньше выдачи')
        conn.execute("UPDATE issues SET return_date=?,status='возвращена' WHERE id=?",(returned.isoformat(),issue_id))
        return True


def edit_reader(reader_id, last_name, first_name, student_card, group_name='', phone='', db_path=None):
    from library_functions import validate_student_card
    validate_student_card(student_card)
    if not last_name.strip() or not first_name.strip(): raise ValueError('Имя и фамилия обязательны')
    with get_connection(db_path) as conn:
        return conn.execute("""UPDATE readers SET last_name=?,first_name=?,student_card=?,group_name=?,phone=? WHERE id=?""",
                            (last_name.strip(),first_name.strip(),student_card,group_name,phone,reader_id)).rowcount


def delete_reader(reader_id, db_path=None):
    with get_connection(db_path) as conn:
        return conn.execute('DELETE FROM readers WHERE id=?',(reader_id,)).rowcount


def get_debtors(db_path=None, as_of=None):
    today=as_of or date.today().isoformat()
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute("""SELECT i.id AS issue_id, r.id AS reader_id,
            r.last_name,r.first_name,r.student_card,b.title,i.due_date,
            CAST(julianday(?) - julianday(i.due_date) AS INTEGER) AS overdue_days
            FROM issues i JOIN readers r ON i.reader_id=r.id JOIN books b ON i.book_id=b.id
            WHERE i.return_date IS NULL AND i.due_date < ? ORDER BY i.due_date""",(today,today))]


def get_most_popular_books(limit=10, db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute("""SELECT b.id,b.title,b.author,COUNT(i.id) AS issue_count
            FROM books b LEFT JOIN issues i ON i.book_id=b.id
            GROUP BY b.id ORDER BY issue_count DESC,b.title LIMIT ?""",(limit,))]


def get_book_history(book_id, db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute("""SELECT i.*,r.last_name,r.first_name
          FROM issues i JOIN readers r ON i.reader_id=r.id
          WHERE i.book_id=? ORDER BY i.issue_date DESC""",(book_id,))]


def get_library_stats(db_path=None):
    with get_connection(db_path) as conn:
        q=lambda sql:conn.execute(sql).fetchone()[0]
        return dict(books=q('SELECT COUNT(*) FROM books'), copies=q('SELECT COALESCE(SUM(quantity),0) FROM books'),
          readers=q('SELECT COUNT(*) FROM readers'), issues_total=q('SELECT COUNT(*) FROM issues'),
          issues_active=q('SELECT COUNT(*) FROM issues WHERE return_date IS NULL'),
          issues_returned=q('SELECT COUNT(*) FROM issues WHERE return_date IS NOT NULL'))


def get_active_readers(limit=10, db_path=None):
    with get_connection(db_path) as conn:
        return [dict(r) for r in conn.execute("""SELECT r.id,r.last_name,r.first_name,r.student_card,
         COUNT(i.id) AS issue_count FROM readers r LEFT JOIN issues i ON i.reader_id=r.id
         GROUP BY r.id ORDER BY issue_count DESC,r.last_name LIMIT ?""",(limit,))]


def export_books_to_csv(filename='books.csv', db_path=None):
    rows=get_all_books(db_path)
    with open(filename,'w',encoding='utf-8-sig',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=['id','title','author','year','quantity']); writer.writeheader(); writer.writerows(rows)
    return filename


def export_debtors_to_txt(filename='debtors.txt', db_path=None, as_of=None):
    rows=get_debtors(db_path,as_of)
    with open(filename,'w',encoding='utf-8') as file:
        file.write('Читатели с просроченными книгами\n')
        if not rows: file.write('Просроченных выдач нет\n')
        for r in rows: file.write(f"{r['last_name']} {r['first_name']} | {r['title']} | до {r['due_date']} | дней: {r['overdue_days']}\n")
    return filename


def backup_database(filename='library_backup.db', db_path=None):
    # SQLite backup API provides a consistent snapshot even when source is open.
    with get_connection(db_path) as source:
        with sqlite3.connect(str(filename)) as target: source.backup(target)
    return filename
