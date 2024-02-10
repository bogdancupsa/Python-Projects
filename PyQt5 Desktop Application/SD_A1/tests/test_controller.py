import unittest

from model.user_repository import UserRepository
from model.user import User
from model.show import Show
from model.show_repository import ShowRepository
from logic.controller import Controller

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()

    # test get_user
    def test_get_user(self):
        # create a user and add it to the database
        user = User("testuser", "password", "admin")
        user_repository = UserRepository()
        user_repository.add_user(user)

        # call the get_user method and check if it returns the correct user object
        retrieved_user = user_repository.get_user("testuser")
        assert retrieved_user == user
    
    # test get_all_shows
    def test_get_all_shows(self):
        result = self.controller.get_all_shows()
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(show, dict) for show in result))

    # test add_show
    def test_add_show(self):
        initial_count = len(self.controller.get_all_shows())
        self.controller.add_show("Test Show", "Test Singer", "2022-04-01", 100, "Test Genre")
        new_count = len(self.controller.get_all_shows())
        self.assertEqual(new_count, initial_count + 1)

    # test update_show
    def test_update_show(self):
        self.controller.add_show("Test Show", "Test Singer", "2022-04-01", 100, "Test Genre")
        self.controller.update_show("Test Show", "Test Singer", "2022-04-01", 50, "Test Genre")
        result = self.controller.show_repository.get_show("Test Show")
        self.assertEqual(result.num_tickets, 50)

    # test delete_show
    def test_delete_show(self):
        self.controller.add_show("Test Show", "Test Singer", "2022-04-01", 100, "Test Genre")
        initial_count = len(self.controller.get_all_shows())
        self.controller.delete_show("Test Show")
        new_count = len(self.controller.get_all_shows())
        self.assertEqual(new_count, initial_count - 1)