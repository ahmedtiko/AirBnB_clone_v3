t Test for DBStorage Class
"""
import unittest
from datetime import datetime
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from os import environ, stat
import inspect
import pep8
from models.engine.db_storage import DBStorage

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """Class for testing DBStorage documentation"""

    all_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For DBStorage Class ......')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.delete_all()

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nDatabase engine\n'
        actual = db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ('\n        interacts with the MySQL database\n    ')
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestDBStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_db(self):
        """... db_storage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/engine/db_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE != 'db', "DB Storage doesn't use FileStorage")
class TestDBStorage(unittest.TestCase):
    """Class for testing DBStorage methods"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('....................................\n\n')
        cls.s = State(name="California")
        cls.c = City(state_id=cls.s.id, name="San Francisco")
        cls.u = User(email="betty@holbertonschool.com", password="pwd")
        cls.p1 = Place(user_id=cls.u.id, city_id=cls.c.id, name="a house")
        cls.p2 = Place(user_id=cls.u.id, city_id=cls.c.id, name="a house two")
        cls.a1 = Amenity(name="Wifi")
        cls.a2 = Amenity(name="Cable")
        cls.a3 = Amenity(name="Bucket Shower")
        objs = [cls.s, cls.c, cls.u, cls.p1, cls.p2, cls.a1, cls.a2, cls.a3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """initializes new objects for testing"""
        self.state = State(name="California")
        self.state.save()
        self.city = City(name="San Francisco", state_id=self.state.id)
        self.city.save()
        self.user = User(email="test@test.com", password="password")
        self.user.save()

    def tearDown(self):
        """tidies up the tests removing storage objects"""
        storage.delete_all()

    def test_all(self):
        """... checks if all() function returns all objects"""
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertGreaterEqual(len(all_objs), 3)

    def test_new_save(self):
        """... checks if new() and save() functions work correctly"""
        self.new_state = State(name="Nevada")
        storage.new(self.new_state)
        storage.save()
        self.assertIn(self.new_state, storage.all(State).values())

    def test_delete(self):
        """... checks if delete() function works correctly"""
        state_id = self.state.id
        storage.delete(self.state)
        storage.save()
        self.assertNotIn(state_id, [state.id for state in storage.all(State).values()])

    def test_get(self):
        """... checks if get() function returns the correct object"""
        state_id = self.state.id
        self.assertEqual(storage.get(State, state_id).id, state_id)
        self.assertIsNone(storage.get(State, "nonexistent-id"))

    def test_count(self):
        """... checks if count() function returns the correct count"""
        self.assertEqual(storage.count(), len(storage.all()))
        self.assertEqual(storage.count(State), len(storage.all(State)))

if __name__ == '__main__':
    unittest.main()

