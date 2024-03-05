import unittest
from app import app
from app.auth import generate_tokens
from app.models import User
from fastapi.testclient import TestClient
import random


class TestAuthEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.test_username = f"test_user_{random.randint(1, 10000)}"
        self.test_password = f"test_password_{random.randint(1, 10000)}"
        self.test_email = f"test_{random.randint(1, 10000)}@mail.ru"
        self.test_fullname = "test test"

        # Assuming User class has a method to create a new user
        self.user = User.create(username=self.test_username, password=self.test_password, email=self.test_email,
                                fullname=self.test_fullname)

    def test_signup_unique_data(self):
        signup_request_data = {
            "username": self.test_username,
            "password": self.test_password,
            "email": self.test_email,
            "fullname": self.test_fullname,
        }

        response = self.client.post("/signup", json=signup_request_data)

        self.assertEqual(response.status_code, 400)

    def test_refresh_endpoint(self):
        access_token = generate_tokens(username=self.test_username).access_token

        response = self.client.post("/refresh", headers={"Authorization": f"Bearer {access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def tearDown(self):
        # Assuming User class has a method to delete a user
        self.user.delete()


class TestUserEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.test_username = f"test_user_{random.randint(1, 10000)}"
        self.test_password = f"test_password_{random.randint(1, 10000)}"
        self.test_email = f"test_{random.randint(1, 10000)}@mail.ru"
        self.test_fullname = "test test"

        # Assuming User class has a method to create a new user
        self.user = User.create(username=self.test_username, password=self.test_password, email=self.test_email,
                                fullname=self.test_fullname)

        self.access_token = generate_tokens(username=self.test_username).access_token

    def test_get_user_endpoint(self):
        response = self.client.get("/user", headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "username": self.test_username,
            "email": self.test_email,
            "fullname": self.test_fullname
        })

    def tearDown(self):
        self.user.delete()


if __name__ == '__main__':
    unittest.main()
