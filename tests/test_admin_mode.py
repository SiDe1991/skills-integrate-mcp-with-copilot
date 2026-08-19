from fastapi.testclient import TestClient

from src.app import app


def make_client():
    return TestClient(app)


def test_valid_teacher_login_sets_session_cookie():
    client = make_client()

    response = client.post(
        "/login",
        json={"username": "teacher", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "teacher"
    assert "teacher_session" in response.cookies


def test_student_signup_requires_teacher_login():
    client = make_client()

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 401


def test_teacher_can_register_student():
    client = make_client()
    login = client.post(
        "/login",
        json={"username": "teacher", "password": "password123"},
    )
    teacher_cookie = login.cookies["teacher_session"]

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newteacheruser@mergington.edu"},
        cookies={"teacher_session": teacher_cookie},
    )

    assert response.status_code == 200
    assert "newteacheruser@mergington.edu" in response.json()["participants"]


def test_teacher_can_unregister_student():
    client = make_client()
    login = client.post(
        "/login",
        json={"username": "teacher", "password": "password123"},
    )
    teacher_cookie = login.cookies["teacher_session"]

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "newteacheruser@mergington.edu"},
        cookies={"teacher_session": teacher_cookie},
    )

    assert response.status_code == 200
    assert "newteacheruser@mergington.edu" not in response.json()["participants"]
