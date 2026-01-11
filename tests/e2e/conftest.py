"""
Fixtures for E2E tests with Playwright.

NOTE: E2E tests run against a live server, NOT test database.
The server should be running on localhost:9000 before running tests.
"""

import pytest
from playwright.sync_api import Browser, Page, sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Browser instance for the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    """New page for each test."""
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture
def base_url():
    """Base URL of Django server."""
    return "http://localhost:9000"


@pytest.fixture
def authenticated_page(page: Page, base_url: str):
    """
    Page with authenticated user.
    Uses test credentials that should exist in the database.
    Create user with: poetry run python manage.py shell
    >>> from apps.users.models import User
    >>> User.objects.create_user('teste2e', 'teste2e@example.com', 'testpass123')
    """
    page.goto(f"{base_url}/accounts/login/")
    # Uses test user credentials - must exist in running server's database
    page.fill('input[name="login"]', "teste2e@example.com")
    page.fill('input[name="password"]', "testpass123")
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    return page
