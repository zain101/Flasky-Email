__author__ = 'zainul'

import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaiser(AttributeError):
            u.password

    def test_password_verification(self):
        u = User('cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salt_are_random(self):
        u = User('cat')
        v = User('dog')
        self.assertTrue(u.password_hash != v.password_hash)