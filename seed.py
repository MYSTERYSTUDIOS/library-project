"""Демонстрационные данные, повторный запуск не создаёт дубликаты."""
from datetime import date,timedelta
from database import *

def seed(db_path=None):
    init_database(db_path)
    with get_connection(db_path) as conn:
        if conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]: return
    b1=add_book('Война и мир','Лев Толстой',1869,3,db_path)
    b2=add_book('Преступление и наказание','Фёдор Достоевский',1866,2,db_path)
    b3=add_book('Мастер и Маргарита','Михаил Булгаков',1967,4,db_path)
    r1=add_reader('Иванов','Иван','СБ-001','3ИСП4','+7-900-000-00-01',db_path)
    r2=add_reader('Петрова','Анна','СБ-002','3ИСП4','+7-900-000-00-02',db_path)
    r3=add_reader('Сидоров','Максим','СБ-003','3ИСП4','+7-900-000-00-03',db_path)
    issue_book(b1,r1,7,db_path,issue_date=(date.today()-timedelta(days=30)).isoformat())
    i=issue_book(b2,r2,14,db_path,issue_date=(date.today()-timedelta(days=20)).isoformat())
    return_book(i,db_path,return_date=(date.today()-timedelta(days=10)).isoformat())
    issue_book(b3,r3,14,db_path)

if __name__=='__main__':
    seed(); print('Демонстрационная база готова')
