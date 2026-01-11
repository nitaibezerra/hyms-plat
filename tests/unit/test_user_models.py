"""
Tests for User model.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests for custom User model."""

    def test_user_creation(self):
        """Test basic user creation."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="pass123")

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("pass123")

    def test_user_with_bio(self):
        """Test user with bio field."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="pass123")
        user.bio = "Test bio content"
        user.save()

        assert user.bio == "Test bio content"

    def test_user_without_bio(self):
        """Test user bio defaults to empty."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="pass123")

        assert user.bio == ""

    def test_user_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass123", first_name="John", last_name="Doe"
        )

        assert user.get_full_name() == "John Doe"

    def test_user_string_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(username="testuser", email="test@example.com", password="pass123")

        # Should have some string representation
        assert len(str(user)) > 0
