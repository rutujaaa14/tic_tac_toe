Objective
Demonstrate your backend development skills by creating a system for a simple Tic-Tac-Toe game with user management and game history tracking.

To create a simple backend for user registration, follow these steps. I'll guide you through setting up a Node.js backend using Express.js, and MongoDB for storing user data.

Steps to Set Up the Backend
1. Set Up the Project Directory
Create a new directory for your backend project:

mkdir backend  
cd backend
2. Initialize a Node.js Project
Run the following command to create a package.json file:

npm init -y
3. Install Required Packages You will need the following packages: express: To create the server and handle routing. mongoose: To interact with MongoDB. bcryptjs: For hashing passwords. jsonwebtoken: For generating JWT tokens. dotenv: To manage environment variables. cors: To enable cross-origin requests (useful for frontend-backend communication). body-parser: To parse incoming request bodies.
4.Install these dependencies: and connect with database

npm install express mongoose bcryptjs jsonwebtoken dotenv cors body-parser  
Connection String : MONGO_URI=mongodb://localhost:27017/

6.You can test the API using Postman with the following routes.
1. User Registration : Method:POST , URL :http://localhost:4000/auth/register
2. Login : Method: POST , URL: http://localhost:4000/auth/login
3. Start Game : Method:POST , URL :http://localhost:4000/game/start
4. Make Move: Method:POST , URL : http://localhost:4000/game/move
5. Get Game History : Method:GET, URL: http://localhost:4000/game/history/{userID}

7.To run backend
nodemon server.js
