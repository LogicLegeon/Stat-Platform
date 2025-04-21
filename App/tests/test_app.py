# App/tests/test_app.py
import logging
import unittest
import pytest   # only needed for the function‑style tests below

from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    update_user
)

LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Unit tests – pure model logic, no database or app context required
# ------------------------------------------------------------------

class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        """Model stores username correctly."""
        user = User("bob", "bobpass")
        self.assertEqual(user.username, "bob")

    def test_get_json(self):
        """Model returns expected JSON representation."""
        user = User("bob", "bobpass")
        expected = {"id": None, "username": "bob"}
        self.assertDictEqual(user.get_json(), expected)

    def test_hashed_password(self):
        """Password is stored hashed and can be verified."""
        password = "mypass"
        user = User("bob", password)
        self.assertNotEqual(user.password, password)  # should be hashed
        self.assertTrue(user.check_password(password))


# ------------------------------------------------------------------
# Integration tests – require application context & database
# The `app` fixture comes from App/tests/conftest.py
# ------------------------------------------------------------------

def test_authenticate(app):
    """create_user → login round‑trip works."""
    create_user("alice", "alicepass")
    assert login("alice", "alicepass") is not None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "rickpass")
        self.assertEqual(user.username, "rick")

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        usernames = {u["username"] for u in users_json}
        # make sure at least our two test users are present
        self.assertTrue({"alice", "rick"} <= usernames)

    def test_update_user(self):
        # assumes user with ID 1 exists from earlier setup
        update_user(1, "ronnie")
        user = get_user(1)
        self.assertEqual(user.username, "ronnie")

