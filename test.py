__author__ = 'Beryl'

import os
import unittest

from views import app, db
from models import User
from config import basedir

TEST_DB = 'test.db'

class Users(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_user_setup(self):
        new_user = User("mherman", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "mherman"

    if __name__ == "__main__":
        unittest.main()
