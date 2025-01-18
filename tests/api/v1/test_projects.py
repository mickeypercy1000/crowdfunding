from fastapi.testclient import TestClient
from app.main import app
from tests.api.v1.fakedb_setup import cleanup_db
from tests.api.v1.fake_data import generate_bad_contribution_data, generate_contribution_data, generate_sample_user_data, generate_sample_project
import unittest

client = TestClient(app)

class TestProjectAndContributions(unittest.TestCase):

    def setUp(self):
        self.contributions_endpoint = "/api/v1/projects/{project_id}/contributions"
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
        self.assertEqual(details["title"], details["title"])
        self.assertEqual(details["goal_amount"], details["goal_amount"])
        self.assertEqual(details["deadline"], details["deadline"])

    def test_user_create_contributions(self):
        user_data = generate_sample_user_data()
        client.post(self.signup_endpoint, json=user_data).json()
        response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]}).json()
        access_token = response["access_token"]
        project = client.post(self.projects_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=generate_sample_project()).json()
        project_id = project["id"]
        contributions_endpoint = self.contributions_endpoint.format(project_id=project_id)
        contrib = generate_contribution_data()
        contribute = client.post(contributions_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=contrib).json()
        self.assertEqual(contribute["amount"], contrib["amount"])

    def test_user_get_contributions(self):
        user_data = generate_sample_user_data()
        client.post(self.signup_endpoint, json=user_data).json()
        response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]}).json()
        access_token = response["access_token"]
        project = client.post(self.projects_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=generate_sample_project()).json()
        project_id = project["id"]
        contributions_endpoint = self.contributions_endpoint.format(project_id=project_id)
        contrib = generate_contribution_data()
        client.post(contributions_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=contrib).json()
        client.post(contributions_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=contrib).json()
        contribute = client.get(contributions_endpoint).json()
        self.assertGreater(len(contribute), 1)
        self.assertGreaterEqual(contribute[0]["amount"], 100)
        self.assertIn("contributor", contribute[0])

    def test_get_projects(self):
        user_data = generate_sample_user_data()
        response = client.post(self.signup_endpoint, json=user_data).json()
        response = client.post(self.login_endpoint, json={"email": user_data["email"], "password": user_data["password"]}).json()
        access_token = response["access_token"]

        project_data = generate_sample_project()
        response = client.post(self.projects_endpoint, headers={"Authorization": f"Bearer {access_token}"}, json=project_data).json()        
        response = client.get(self.projects_endpoint).json()
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)