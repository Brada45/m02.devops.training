import unittest
import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        database.init_database()
        database.delete_all_users()

    def tearDown(self):
        database.delete_all_users()

    def test_create_user(self):
        user_id = database.create_user("Srdjan", "srdjan@test.com", 25)
        self.assertIsNotNone(user_id)

    def test_create_duplicate_user(self):
        database.create_user("Srdjan", "srdjan@test.com", 25)

        with self.assertRaises(Exception):
            database.create_user("Srdjan2", "srdjan@test.com", 30)

    def test_get_user_by_id(self):
        user_id = database.create_user("Test", "test@test.com", 20)
        user = database.get_user_by_id(user_id)

        self.assertEqual(user["name"], "Test")
        self.assertEqual(user["email"], "test@test.com")

    def test_get_user_by_email(self):
        database.create_user("Test", "email@test.com", 22)
        user = database.get_user_by_email("email@test.com")

        self.assertEqual(user["name"], "Test")

    def test_get_all_users(self):
        database.create_user("A", "a@test.com", 20)
        database.create_user("B", "b@test.com", 25)

        users = database.get_all_users()
        self.assertEqual(len(users), 2)

    def test_update_user(self):
        user_id = database.create_user("Old", "old@test.com", 20)

        success = database.update_user(user_id, name="New")
        self.assertTrue(success)

        user = database.get_user_by_id(user_id)
        self.assertEqual(user["name"], "New")

    def test_update_nonexistent(self):
        success = database.update_user(9999, name="Nope")
        self.assertFalse(success)

    def test_delete_user(self):
        user_id = database.create_user("Delete", "del@test.com", 30)

        success = database.delete_user(user_id)
        self.assertTrue(success)

        user = database.get_user_by_id(user_id)
        self.assertIsNone(user)

    def test_delete_nonexistent(self):
        success = database.delete_user(9999)
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()