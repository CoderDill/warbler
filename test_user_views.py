"""User model tests"""

import os
from unittest import TestCase
from models import db, Message, User, Follows

#Test db
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="test123",
                                    email="test123@test123.com",
                                    password="test123",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("testing1", "test1@test.com", "123", None)
        self.u1_id = 888
        self.u1.id = self.u1_id
        self.u2 = User.signup("testing2", "test2@test.com", "456", None)
        self.u2_id = 777
        self.u2.id = self.u2_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_index(self):
        with self.client as client:
            response = client.get("/users")

            self.assertIn("test123", str(response.data))
            self.assertIn("testing1", str(response.data))
            self.assertIn("testing2", str(response.data))

    def test_users_search(self):
        with self.client as client:
            response = client.get("/users?q=3")

            self.assertIn("test123", str(response.data))

            self.assertNotIn("testing1", str(response.data))
            self.assertNotIn("testing2", str(response.data))
    
    def test_user_show(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("test123", str(resp.data))