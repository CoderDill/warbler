"""Message model tests"""

import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, Message, User, Likes

#Test db
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()
class MessageModelTest(TestCase):
    """Message Tests"""

    def setUp(self):
        """Test client and sample data"""

        db.drop_all()
        db.create_all()

        u = User.signup("test", "test@test.com", "abc123", None)
        u.id = 123
        db.session.commit()

        self.u = User.query.get(u.id)
        self.client = app.test_client()

    def tearDown(self) -> None:
        """Clear sample data"""

        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Test message model"""

        m = Message(text="Test warbler", user_id=self.u.id)
        
        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "Test warbler")

    def test_message_likes(self):        

        m0 = Message(text="Test warbler", user_id=self.u.id)
        m1 = Message(text="Test warbler 2", user_id=self.u.id)

        u = User.signup("tester", "tester@tester.com", "123abc", None)
        u.id = 321
        db.session.add_all([m0, m1, u])
        db.session.commit()

        u.likes.append(m0)
        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == u.id).all()
        self.assertEqual(len(l), 2)
        self.assertEqual(l[1].message_id, m1.id)


               
