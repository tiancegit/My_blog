import unittest
from flask import current_app
from app import create_app, db


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = current_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertFalse(current_app.config['TESTING'])
