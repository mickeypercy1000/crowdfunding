# Crowdfunding App

This is a FastAPI-powered crowdfunding application that allows users to:
- Sign up and log in to the platform
- Create projects with a goal amount
- Contribute to projects
- View project details and contributions

The app runs on Uvicorn and allows easy interaction with endpoints for user authentication, project creation, and contribution tracking.

## Features

- **User Authentication**: Users can sign up and log in using their credentials.
- **Project Creation**: Users can create crowdfunding projects by specifying a title, description, goal amount, and deadline.
- **Contributions**: Users can contribute funds to projects and track their contributions.
- **View Projects**: Users can view all available projects and their details.
- **View Contributions**: Users can see the list of contributors for a specific project.

## Prerequisites

- Python 3.7 or higher
- Uvicorn
- FastAPI
- PostgreSQL (or another database of your choice)
- Other dependencies as specified in the application's `requirements.txt` file

## Installation

1. Clone the repository:
   ```bash
   git clone via SSH at `git@github.com:mickeypercy1000/crowdfunding.git` or via HHTPS at `https://github.com/mickeypercy1000/crowdfunding.git`
   cd crowdfunding-app

2. Create a virtual environment and activate it:
    - `python -m venv venv`(on windows)
    - `source venv/bin/activate`(on mac)

3. Install the required dependencies:
    - `pip install -r requirements.txt` or sometimes `pip3 install -r requirements.txt`(for mac users)

4. Set up your database (PostgreSQL recommended):

    Ensure your database is running and accessible.
    Update the `DATABASE_URL` in your .env file or configuration file to match your database settings.

5. Run the app with Uvicorn:
    - `uvicorn app.main:app --reload`

6. Visit http://127.0.0.1:8000/docs in your browser to interact with the application's APIs.



**API Endpoints**
1. User Authentication

    - POST /api/v1/users/register: Registers a new user.
    - POST /api/v1/users/login: Logs in a user and returns an access token.
    - GET /api/v1/users/me: Fetches the authenticated user's details.

2. Project Management

    - POST /api/v1/projects: Creates a new project.
    - GET /api/v1/projects: Lists all available projects.
    - GET /api/v1/projects/`{project_id}`: View details of a specific project.

3. Contributions

    - POST /api/v1/projects/`{project_id}`/contributions: contributions: Makes a contribution to a project.
    - GET /api/v1/projects/`{project_id}`/contributions: Lists all contributions for a project.


**Environment Variables**

1. You may need to set the following environment variables:

    - DATABASE_URL: The URL for your PostgreSQL or other database. Format: postgresql://<user>:<password>@<host>:<port>/<database_name>
    - SECRET_KEY: A secret key used for encoding JWT tokens.
    - ALGORITHM: Algorithm for encoding.

**TESTS**
You can run the tests with the following command:
`python -m unittest discover tests/api/v1`

**License**
This project is currently unlicensed.
Feel free to contribute to this project or fork it for your own use. If you have any questions or issues, please open an issue or reach out to me directly.


### Explanation:
- **Features**: Describes the functionalities of the app, such as user signup, project creation, and contributions.
- **Installation**: Step-by-step instructions for setting up the project on your local machine.
- **API Endpoints**: A summary of the available endpoints for user authentication, project management, and contributions.
- **Environment Variables**: Lists the necessary environment variables for configuring the app.
- **Tests**: Instructions on running tests with `python -m unittest discover tests/api/v1`.
- **License**: You can specify the license type for the project.

This README will help users and developers get up and running with your app easily.
