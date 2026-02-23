import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset activities to original state before each test
    orig = copy.deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interscholastic games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["lucas@mergington.edu", "sophia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and various artistic techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in school plays and theatrical productions",
            "schedule": "Mondays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["mia@mergington.edu", "liam@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": ["noah@mergington.edu", "charlotte@mergington.edu"]
        }
    })
    activities.clear()
    activities.update(copy.deepcopy(orig))
    yield

client = TestClient(app)

def test_get_activities():
    # Arrange: None needed, uses fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]

def test_unregister_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
