# Weather Decision Service

The **Weather Decision Service** is a Python-based application that integrates with the OpenWeather API to provide actionable decisions about whether it's suitable to go out based on real-time weather conditions. The service includes AI/ML processing, database support, and a robust development workflow.

---

## Features
- Fetch real-time weather data using the OpenWeather API.
- Process weather data with AI/ML logic for decision-making.
- RESTful API built with FastAPI.
- Database migration management using Alembic.
- Dockerized setup for seamless deployment.

---

## Installation

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- PostgreSQL (optional if using Docker for DB)
- OpenWeather API Key

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kulsss/weather-decision-service.git
   cd weather-decision-service
2. **Set Up Environment Variables: Create a .env file in the root directory - Example**
DATABASE_URL=postgresql+psycopg2://user:password@localhost/weather_db
OPENWEATHER_API_KEY=5573debcbbc67c80c90a4bdbabe3504d

3. **Run the Application:**

**With Python:**
  pip install -r requirements.txt
  alembic upgrade head
  uvicorn apps.weather_service.main:app --host 0.0.0.0 --port 8000 --reload

**With Docker Compose:**
  docker-compose up --build

4. **API Endpoints**    
    Weather Decision
    Endpoint: GET /decision
    Parameters:
    city: Name of the city (query parameter).
    Response:
    decision: "Yes" or "No".
    reason: Explanation for the decision.

**Example**
  curl -X GET "http://localhost:8000/decision?city=London"

5. **Development Workflow**

Pre-commit Hooks
This project includes pre-commit hooks for maintaining code quality. To install:
    pre-commit install
    
Hooks include:

    Code Formatting: black, isort
    Linting: flake8, pylint
    Type Checking: mypy
    Security Scanning: bandi

6. **Testing**
Run tests with pytest:
    pytest

**Folder Structure**
.
├── apps/
│   ├── weather_service/
│   ├── ai_service/
├── libs/
│   ├── models/
│   ├── utils/
├── migrations/
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md

**Contributing**
Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request for review.



"# Monorepo_project" 
"# Monorepo_project" 
