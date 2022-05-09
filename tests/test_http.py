"""
Date: 2022.05.09 19:13
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.05.09 22:20:39
"""
from fastapi.testclient import TestClient

from github_trending_migrator.http import app
from github_trending_migrator.http import DOMAIN_NAME

client = TestClient(app)


def test_help_route():
    """Tests if the '/'-route (help-route) returns correctly data
    about repositories/developers and built-in documentation.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "repositories": f"{DOMAIN_NAME}/repositories",
        "developers": f"{DOMAIN_NAME}/developers",
        "docs": f"{DOMAIN_NAME}/docs",
        "redoc": f"{DOMAIN_NAME}/redoc",
    }


def test_repository_route():
    response = client.get("/repositories")
    assert response.status_code == 200
