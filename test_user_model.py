"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u0 = User.signup("test1", "test1@test.com", "abc123", None)
        u0.id = 123
        
        u1 = User.signup("tester2", "tester2@tester.com", "123abc", None)
        u1.id = 456

        db.session.commit()

        u0 = User.query.get(u0.id)
        u1 = User.query.get(u1.id)

        self.u0 = u0
        self.uid0 = u0.id
        self.u1 = u1
        self.uid1 = u1.id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_signup(self):
        test_user = User.signup("testing", "test3@test3.com", "abc123", None)
        test_user.id = 1111
        
        db.session.commit()

        test_user = User.query.get(test_user.id)
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.username, "testing")
        self.assertEqual(test_user.email, "test3@test3.com")
        self.assertNotEqual(test_user.password, "abc123")
        self.assertTrue(test_user.password.startswith('$2b$'))


    def test_valid_authentication(self):
        u = User.authenticate(self.u0.username, "abc123")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid0)

    def test_user_follows(self):
        self.u0.following.append(self.u1)
        db.session.commit()

        self.assertEqual(len(self.u0.following), 1)
        self.assertEqual(len(self.u1.following), 0)
        self.assertEqual(len(self.u1.followers), 1)
        self.assertEqual(len(self.u0.followers), 0)

    def test_is_followed_by(self):
        self.u0.following.append(self.u1)

        self.assertTrue(self.u1.is_followed_by(self.u0))

    def test_is_following(self):
        self.u0.following.append(self.u1)
        db.session.commit()

        self.assertTrue(self.u0.is_following(self.u1))