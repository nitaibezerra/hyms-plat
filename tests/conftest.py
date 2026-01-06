"""
Pytest configuration and fixtures.
"""

import pytest


@pytest.fixture
def user_factory():
    """
    Factory for creating test users.
    """
    from apps.users.models import User

    def _create_user(email="test@example.com", password="testpass123", **kwargs):
        return User.objects.create_user(username=email.split("@")[0], email=email, password=password, **kwargs)

    return _create_user


@pytest.fixture
def authenticated_client(client, user_factory):
    """
    Client with authenticated user.
    """
    user = user_factory()
    client.force_login(user)
    client.user = user
    return client
