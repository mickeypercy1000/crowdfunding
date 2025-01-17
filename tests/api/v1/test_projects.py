from datetime import datetime
import unittest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from tests.api.v1.fakedb_setup import cleanup_db
from tests.api.v1.faker import generate_sample_user_data, generate_sample_project

client = TestClient(app)

class TestUserAuth(unittest.TestCase):

    def setUp(self):
        self.signup_endpoint = "/api/v1/users/register"
        self.login_endpoint = "/api/v1/users/login"
        self.my_details_endpoint = "/api/v1/users/me"
        self.projects_endpoint = "/api/v1/projects"

    def tearDown(self):
        cleanup_db()
        
    def test_user_can_create_project(self):
        user_data = generate_sample_user_data()
        client.post(self.signup_endpoint, json=user_data).json()
        response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]}).json()
        access_token = response["access_token"]
        details = client.post(self.projects_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=generate_sample_project()).json()
        self.assertEqual(details["status"], True)
        self.assertEqual(details["title"], details["title"])
        self.assertEqual(details["goal_amount"], details["goal_amount"])
        self.assertEqual(details["deadline"], details["deadline"])

    # def test_user_can_login(self):
    #     user_data = generate_sample_user_data()
    #     client.post(self.signup_endpoint, json=user_data).json()
    #     response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("access_token", response.json())

    # def test_get_my_details(self):
    #     user_data = generate_sample_user_data()
    #     client.post(self.signup_endpoint, json=user_data).json()
    #     response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]}).json()
    #     access_token = response["access_token"]
    #     details = client.get(self.my_details_endpoint, headers={"Authorization": f"Bearer {access_token}"}).json()
        
    #     self.assertEqual(details["status"], True)
    #     self.assertEqual(details["email"], user_data["email"])
    #     self.assertEqual(details["username"], user_data["username"])
    #     self.assertEqual(details["firstname"], user_data["firstname"])
    #     self.assertEqual(details["lastname"], user_data["lastname"])
