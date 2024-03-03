import os
import unittest
import pandas as pd
from src.utils.sqlite_handler import SQLiteHandler

class TestSQLiteHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Setting up SQLiteHandler test class...')
        if not os.path.exists('src/data'):
            os.makedirs('src/data')
        if os.path.isfile('src/data/test.csv'):
            os.remove('src/data/test.csv')
        if os.path.isfile('src/data/test.db'):
            os.remove('src/data/test.db')
    
    def test_migrate_csv_to_sqlite(self):
        # Create a test CSV file
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        df.to_csv('src/data/test.csv', index=False)
        self.assertTrue(os.path.isfile('src/data/test.csv'))

        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', 'test_table')
        
        # Test
        handler.migrate_csv_to_sqlite()

        # Assert
        self.assertTrue(os.path.isfile('src/data/test.db'))

        # Tear down
        os.remove('src/data/test.csv')
        os.remove('src/data/test.db')
    
    def test_migrate_csv_to_sqlite_no_csv_file(self):
        # An error occurred: CSV file or table name is not provided.

        handler = SQLiteHandler('src/data/test.db', None, 'test_table')
        
        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.migrate_csv_to_sqlite()

        self.assertTrue('CSV file is not provided.' in str(context.exception))
       
    def test_migrate_csv_to_sqlite_no_table_name(self):
        # Initialize SQLiteHandler without table_name
        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', None)

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.migrate_csv_to_sqlite()

        self.assertTrue('Table name is not provided.' in str(context.exception))

    def test_fetch_data_from_sqlite(self):
        # Create a test CSV file
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        df.to_csv('src/data/test.csv', index=False)
        self.assertTrue(os.path.isfile('src/data/test.csv'))

        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', 'test_table')
        
        # Test
        handler.migrate_csv_to_sqlite()
        df = handler.fetch_data_from_sqlite()

        # Assert
        self.assertIsInstance(df, pd.DataFrame)

        # Tear down
        os.remove('src/data/test.csv')
        os.remove('src/data/test.db')

    def test_fetch_data_from_sqlite_no_sqlite_file(self):
        # Initialize SQLiteHandler without table_name
        handler = SQLiteHandler(None, 'src/data/test.csv', 'test_table')

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.fetch_data_from_sqlite()

        self.assertTrue('SQLite file is not provided.' in str(context.exception))

    def test_fetch_data_from_sqlite_no_table_name(self):
        # Initialize SQLiteHandler without table_name
        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', None)

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.fetch_data_from_sqlite()

        self.assertTrue('Table name is not provided.' in str(context.exception))


    def test_load_data_sqlite_exists(self):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        df.to_csv('src/data/test.csv', index=False)
        self.assertTrue(os.path.isfile('src/data/test.csv'))

        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', 'test_table')
        handler.migrate_csv_to_sqlite()
        self.assertTrue(os.path.isfile('src/data/test.db'))

        # Test
        df = handler.load_data()

        # Assert
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2, 2))

        # Tear down
        os.remove('src/data/test.csv')
        os.remove('src/data/test.db')

    def test_load_data_no_sqlite_csv_exists(self):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        df.to_csv('src/data/test.csv', index=False)
        self.assertTrue(os.path.isfile('src/data/test.csv'))

        handler = SQLiteHandler(None, 'src/data/test.csv', 'test_table')

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.load_data()
        self.assertTrue('SQLite file path is not provided.' in str(context.exception))

    def test_load_data_no_sqlite_no_csv_exists(self):
        handler = SQLiteHandler(None, None, 'test_table')

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.load_data()
        self.assertTrue('SQLite file path is not provided.' in str(context.exception))

    def test_load_data_no_table_name(self):
        handler = SQLiteHandler('src/data/test.db', 'src/data/test.csv', None)

        # Assert
        with self.assertRaises(Exception) as context:
            # Test
            handler.load_data()
        self.assertTrue('Table name is not provided.' in str(context.exception))

if __name__ == '__main__':
    unittest.main()