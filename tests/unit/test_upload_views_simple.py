"""
Simple smoke tests for upload views to boost coverage.
"""

import pytest
import yaml
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def user(django_user_model):
    """Create test user."""
    return django_user_model.objects.create_user(
        username="uploader", email="uploader@example.com", password="pass123"
    )


@pytest.mark.django_db
class TestUploadViewsSimple:
    """Simple smoke tests for upload views."""

    def test_upload_view_post_invalid_yaml(self, client, user):
        """Test upload with invalid YAML content."""
        client.force_login(user)

        invalid_yaml = SimpleUploadedFile("bad.yaml", b"invalid: yaml: content: [[[", content_type="application/x-yaml")

        url = reverse("users:upload")
        response = client.post(url, {"yaml_file": invalid_yaml})

        # Should not crash, should show error
        assert response.status_code in [200, 302]

    def test_upload_view_post_valid_yaml_minimal(self, client, user):
        """Test upload with minimal valid YAML."""
        client.force_login(user)

        yaml_content = yaml.dump(
            {"hymn_book": {"name": "Minimal Test", "owner": "Owner", "hymns": []}}, allow_unicode=True
        )
        yaml_file = SimpleUploadedFile("minimal.yaml", yaml_content.encode("utf-8"))

        url = reverse("users:upload")
        response = client.post(url, {"yaml_file": yaml_file})

        # Should process successfully
        assert response.status_code in [200, 302]

    def test_disambiguate_view_get_without_session(self, client, user):
        """Test accessing disambiguate without session data."""
        client.force_login(user)

        url = reverse("users:upload_disambiguate")
        response = client.get(url)

        # Should redirect back to upload
        assert response.status_code == 302

    def test_preview_view_get_without_session(self, client, user):
        """Test accessing preview without session data."""
        client.force_login(user)

        url = reverse("users:upload_preview")
        response = client.get(url)

        # Should redirect back to upload
        assert response.status_code == 302

    def test_confirm_view_get_without_session(self, client, user):
        """Test accessing confirm without session data."""
        client.force_login(user)

        url = reverse("users:upload_confirm")
        response = client.get(url)

        # Should redirect back to upload
        assert response.status_code == 302

    def test_disambiguate_view_cancel_choice(self, client, user):
        """Test cancel choice in disambiguation."""
        client.force_login(user)

        # Set minimal session data
        session = client.session
        session["upload_data"] = {"name": "Test", "owner": "Owner", "hymns": []}
        session.save()

        url = reverse("users:upload_disambiguate")
        response = client.post(url, {"choice": "cancel"})

        # Should redirect to upload
        assert response.status_code == 302
        assert "contribuir" in response.url

    def test_upload_view_missing_file(self, client, user):
        """Test upload without providing file."""
        client.force_login(user)

        url = reverse("users:upload")
        response = client.post(url, {})

        # Should show form with error
        assert response.status_code == 200
        assert b"yaml_file" in response.content or b"arquivo" in response.content.lower()

    def test_upload_view_file_too_large(self, client, user):
        """Test upload with file exceeding size limit."""
        client.force_login(user)

        # Create a file larger than 10MB
        large_content = b"x" * (11 * 1024 * 1024)
        large_file = SimpleUploadedFile("large.yaml", large_content)

        url = reverse("users:upload")
        response = client.post(url, {"yaml_file": large_file})

        # Should show error
        assert response.status_code == 200

    def test_upload_view_wrong_file_type(self, client, user):
        """Test upload with wrong file extension."""
        client.force_login(user)

        txt_file = SimpleUploadedFile("test.txt", b"not yaml")

        url = reverse("users:upload")
        response = client.post(url, {"yaml_file": txt_file})

        # Should show error
        assert response.status_code == 200
