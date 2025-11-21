"""
Tests for user management endpoints
"""
import pytest


def test_create_user(client):
    """Test user registration"""
    response = client.post(
        "/users/",
        json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "name": "New User",
            "role": "customer"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["name"] == "New User"
    assert "password" not in data  # Password should never be returned


def test_create_duplicate_user(client, test_user):
    """Test that duplicate email returns error"""
    response = client.post(
        "/users/",
        json={
            "email": test_user.email,
            "password": "password123",
            "name": "Duplicate User",
            "role": "customer"
        }
    )
    assert response.status_code == 400


def test_get_current_user(client, auth_headers, test_user):
    """Test getting current user profile"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


def test_get_current_user_unauthorized(client):
    """Test that accessing /users/me without token fails"""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client):
    """Test that invalid token is rejected"""
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code == 401
