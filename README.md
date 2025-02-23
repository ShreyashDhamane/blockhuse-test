# Order Management System

This project is an **Order Management System** built using **FastAPI**, **WebSocket**, and **Docker**. It provides APIs for managing orders, real-time updates via WebSocket, and a user-friendly interface with forms and pages. The system is deployed on **AWS EC2** and uses **GitHub Actions** for CI/CD.

---

## Features

- **REST APIs**:
  - Create, view, and manage orders.
  - Error handling for invalid inputs.
- **WebSocket**:
  - Real-time updates for new orders.
  - Supports `ping`/`pong` for connection keep-alive.
- **Frontend**:
  - HTML pages for creating and viewing orders.
- **Testing**:
  - Unit tests for APIs and WebSocket.
- **CI/CD**:
  - Automated testing and deployment using GitHub Actions.
- **Docker**:
  - Containerized application for easy deployment.
- **Documentation**:
  - API documentation available via Swagger UI.

---

## Live Deployment

The application is deployed on **AWS EC2**. You can access it here:

- **Base URL**: [http://ec2-54-208-250-172.compute-1.amazonaws.com](http://ec2-54-208-250-172.compute-1.amazonaws.com)
- **WebSocket URL**: `ws://ec2-54-208-250-172.compute-1.amazonaws.com/ws/orders`
- **API Documentation**: [http://ec2-54-208-250-172.compute-1.amazonaws.com/docs](http://ec2-54-208-250-172.compute-1.amazonaws.com/docs)

---

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: HTML (Chameleon templates)
- **Database**: SQLite (for simplicity, can be replaced with any other database)
- **Real-Time Communication**: WebSocket
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: AWS EC2
- **Testing**: Pytest

---

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.8+**
2. **Docker** (for containerized deployment)
3. **Git** (for cloning the repository)

---

## Steps to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/ShreyashDhamane/blockhuse-test.git
cd blockhuse-test
```

### 2. Change the production websocket URL

```bash
Open the file /static/orders.js and change the websocket URL to the one you are using/localhost
WEBSOCKET_URL=ws://localhost:80/ws/orders
```

### 3. Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Application Locally
To run the application locally:

```bash

uvicorn main:app --host 0.0.0.0 --port 80 --reload
```

The application will be available at: http://localhost:80

API Documentation: http://localhost:8000/docs

WebSocket URL: ws://localhost:8000/ws/orders

### 5. Run with Docker
To run the application using Docker:

- Build the Docker image: docker build -t trade-order-service .
- Run the Docker container: docker run -d -p 80:80 trade-order-service
- The application will be available at: http://localhost:80



### 6. Running Tests
To run the test cases:

``` bash

pytest
```
This will execute all unit tests for the APIs and WebSocket.

### 7. CI/CD Pipeline
- The project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

- Testing: Runs unit tests on every push to the main branch.

- Docker Build: Builds the Docker image on successful tests.

- Deployment: Deploys the application to AWS EC2.

### 8. Project Structure

blockhouse-test/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── routes/                # API and WebSocket routes
│   ├── models/                # Database models
│   ├── templates/             # HTML templates
│   ├── tests/                 # Unit tests
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
├── .github/workflows/         # GitHub Actions workflows
└── README.md                  # Project documentation

