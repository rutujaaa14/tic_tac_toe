**Objective**
Demonstrate your backend development skills by creating a system for a simple Tic-Tac-Toe game with
user management and game history tracking.

**Steps to Set Up the Backend**
Steps to Set Up the Backend
1. Set Up the Project Directory
    Create a new directory for your Django project and navigate into it:
        **mkdir tictactoe
        cd tictactoe**
2. Initialize the Django Project
    Run the following command to create a new Django project:
        **django-admin startproject tictactoe**
3. Create a New Django App
    Create a new Django app named game to handle game logic and user management:
          **python manage.py startapp game**
4. Install Required Packages
    
    Django: The web framework for building the backend.
    Django REST Framework: To create APIs for user and game management.
    Django Rest Framework SimpleJWT: For handling JWT authentication.
    PostgreSQL/MySQL: As the database to store user and game data.
5. Install the required dependencies:
    pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary
    You can replace psycopg2-binary with mysqlclient if you're using MySQL.

6. Run migrations to set up the database:
         **python manage.py migrate**

7.To run backend
          **python manage.py runserver**
