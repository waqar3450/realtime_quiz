## Part 1: System Design

### Architecture Diagram
Here is a high-level architecture diagram of the real-time quiz system:

```
+-----------------+        +-----------------+        +-----------------+
|                 |        |                 |        |                 |
|    Frontend     +-------->   WebSocket     +-------->   Backend       |
|  (React, HTML)  |  WS    |    Server       |  API   |  (Django)       |
|                 |        |  (Django +      |        |                 |
+-----------------+        |  Channels)      |        +-----------------+
        |                           ^                            |
        | HTTP                      | WS                         |
        v                           |                            v
+-----------------+        +-----------------+        +-----------------+
|                 |        |                 |        |                 |
|  User Clients   +-------->   Redis Pub/Sub +-------->  Database       |
|  (Browsers)     |        |                 |        |  (PostgreSQL)   |
|                 |        |                 |        |                 |
+-----------------+        +-----------------+        +-----------------+
```

### Component Description

1. **Frontend (React, HTML)**
   - **Role**: This component provides the user interface for users to join quiz sessions, submit answers, and view the real-time leaderboard. It communicates with the backend using WebSockets for real-time updates.
   
2. **WebSocket Server (Django + Channels)**
   - **Role**: This server handles real-time communication between the frontend and backend using WebSockets. It manages user connections, broadcasts score updates, and updates the leaderboard in real-time.

3. **Backend (Django)**
   - **Role**: The backend processes quiz logic, calculates scores, and maintains the state of quiz sessions. It exposes APIs for the frontend to interact with and updates the database with user scores and quiz results.

4. **Redis Pub/Sub**
   - **Role**: Redis is used for real-time messaging and communication between the WebSocket server and backend. It ensures that score updates and leaderboard changes are propagated in real-time.

5. **Database (PostgreSQL)**
   - **Role**: The database stores user information, quiz data, and scores. It provides persistent storage and ensures data consistency.

### Data Flow

1. **User Joins Quiz**: 
   - User enters a unique quiz ID in the frontend.
   - Frontend sends a request to the backend to join the quiz.
   - Backend validates the quiz ID and adds the user to the quiz session.

2. **User Submits Answer**:
   - User submits an answer through the frontend.
   - Frontend sends the answer to the backend via the WebSocket server.
   - Backend processes the answer, updates the score, and sends the updated score back through the WebSocket server.

3. **Score Update**:
   - Backend publishes the score update to Redis.
   - WebSocket server subscribes to the Redis channel and receives the update.
   - WebSocket server broadcasts the updated score to all connected clients.

4. **Leaderboard Update**:
   - As scores are updated, the backend recalculates the leaderboard.
   - Backend sends the updated leaderboard to Redis.
   - WebSocket server receives the update and broadcasts it to all clients.

### Technologies and Tools

1. **Frontend**: React for a dynamic and responsive user interface.
2. **WebSocket Server**: Django Channels for handling real-time WebSocket connections.
3. **Backend**: Django for robust and scalable backend logic.
4. **Redis**: For real-time messaging and pub/sub functionality.
5. **Database**: PostgreSQL for reliable and consistent data storage.

