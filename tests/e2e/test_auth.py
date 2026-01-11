"""
E2E tests for authentication.

NOTE: These tests run against a live server on localhost:9000.
Start the server before running: poetry run python manage.py runserver 9000
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestAuthentication:
    """Tests for user authentication."""

    def test_signup_page_loads(self, page: Page, base_url: str):
        """Signup page loads correctly."""
        page.goto(f"{base_url}/accounts/signup/")

        expect(page.locator('input[name="email"]')).to_be_visible()
        expect(page.locator('input[name="password1"]')).to_be_visible()

    def test_login_page_loads(self, page: Page, base_url: str):
        """Login page loads correctly."""
        page.goto(f"{base_url}/accounts/login/")

        expect(page.locator('input[name="login"]')).to_be_visible()
        expect(page.locator('input[name="password"]')).to_be_visible()

    def test_login_with_invalid_credentials_shows_error(self, page: Page, base_url: str):
        """Login with invalid credentials shows error."""
        page.goto(f"{base_url}/accounts/login/")

        page.fill('input[name="login"]', "wrong@example.com")
        page.fill('input[name="password"]', "wrongpass")
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        # Should stay on login page with error message
        # allauth shows errors in various ways
        content = page.content().lower()
        has_error = (
            "errorlist" in content
            or "incorrect" in content
            or "inválid" in content
            or "invalid" in content
            or "erro" in content
            or page.url.endswith("/accounts/login/")  # Still on login = failed
        )
        assert has_error, "Expected to stay on login page or show error"

    def test_protected_page_redirects_to_login(self, page: Page, base_url: str):
        """Accessing protected page without login redirects to login."""
        page.goto(f"{base_url}/contribuir/")

        page.wait_for_load_state("networkidle")
        # Should redirect to login
        assert "/accounts/login/" in page.url
