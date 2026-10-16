import tempfile
import unittest
from pathlib import Path
from database import init_database, add_book, add_reader, search_books, list_readers

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / 'test.db'
        init_database(self.db_path)

    def tearDown(self):
        self.temp.cleanup()

    def test_add_and_find_book(self):
        add_book('Война и мир', 'Лев Толстой', 1869, 3, self.db_path)
        self.assertEqual(len(search_books('Толстой', self.db_path)), 1)

    def test_add_reader(self):
        add_reader('Иванов', 'Иван', 'СБ-001', db_path=self.db_path)
        self.assertEqual(len(list_readers(self.db_path)), 1)

    def test_empty_search(self):
        self.assertEqual(search_books('нет', self.db_path), [])

if __name__ == '__main__':
    unittest.main()
