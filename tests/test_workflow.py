import tempfile
from pathlib import Path
import pytest
from database import *

@pytest.fixture
def dbfile(tmp_path):
    p=tmp_path/'test.db'; init_database(p); return p

def test_full_workflow(dbfile,tmp_path):
    b=add_book('Тест','Автор',2020,1,dbfile)
    r=add_reader('Иванов','Иван','ABC-001',db_path=dbfile)
    assert get_books_by_author('Авт',dbfile)[0]['id']==b
    assert len(get_all_books(dbfile))==1
    assert len(get_all_readers(dbfile))==1
    i=issue_book(b,r,7,dbfile,issue_date='2024-01-01')
    assert len(get_all_issues(dbfile))==1
    assert get_debtors(dbfile,'2024-02-01')[0]['overdue_days']==24
    with pytest.raises(ValueError): issue_book(b,r,7,dbfile)
    assert get_most_popular_books(db_path=dbfile)[0]['issue_count']==1
    assert get_book_history(b,dbfile)[0]['id']==i
    assert get_active_readers(db_path=dbfile)[0]['issue_count']==1
    assert get_library_stats(dbfile)['issues_active']==1
    assert return_book(i,dbfile,'2024-01-09')
    assert get_library_stats(dbfile)['issues_returned']==1
    assert get_debtors(dbfile,'2024-02-01')==[]
    assert edit_book(b,'Тест2','Автор2',2021,2,dbfile)==1
    assert edit_reader(r,'Петров','Пётр','ABC-002',db_path=dbfile)==1
    assert Path(export_books_to_csv(tmp_path/'books.csv',dbfile)).exists()
    assert Path(export_debtors_to_txt(tmp_path/'debtors.txt',dbfile)).exists()
    backup_database(tmp_path/'backup.db',dbfile)
    with get_connection(tmp_path/'backup.db') as conn:
        assert conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]==1
    with pytest.raises(Exception): delete_book(b,dbfile)  # history protected by FK

def test_validation_and_deletion(dbfile):
    b=add_book('Тест','Автор',2020,2,dbfile)
    r=add_reader('Тестов','Тест','X-1',db_path=dbfile)
    assert delete_book(b,dbfile)==1
    assert delete_reader(r,dbfile)==1
    with pytest.raises(ValueError): add_book('','Автор',2020,1,dbfile)
