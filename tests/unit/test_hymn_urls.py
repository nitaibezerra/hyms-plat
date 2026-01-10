"""
Unit tests for Hymn URL patterns.
"""

import uuid

import pytest
from django.urls import resolve, reverse

from apps.hymns import views


@pytest.mark.django_db
class TestHymnUrls:
    """Tests for hymn URL patterns."""

    def test_home_url_resolves(self):
        """Test that home URL resolves correctly."""
        url = reverse("hymns:home")
        assert url == "/"
        assert resolve(url).func == views.home_view

    def test_hymnbook_list_url_resolves(self):
        """Test that hymnbook list URL resolves."""
        url = reverse("hymns:hymnbook_list")
        assert url == "/hinarios/"
        assert resolve(url).func.view_class == views.HymnBookListView

    def test_hymnbook_detail_url_resolves(self):
        """Test that hymnbook detail URL resolves with slug."""
        test_slug = "o-cruzeiro"
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": test_slug})
        assert url == f"/hinarios/{test_slug}/"
        assert resolve(url).func.view_class == views.HymnBookDetailView

    def test_hymn_detail_url_resolves(self):
        """Test that hymn detail URL resolves with UUID."""
        test_uuid = uuid.uuid4()
        url = reverse("hymns:hymn_detail", kwargs={"pk": test_uuid})
        assert url == f"/hinos/{test_uuid}/"
        assert resolve(url).func.view_class == views.HymnDetailView

    def test_search_url_resolves(self):
        """Test that search URL resolves correctly."""
        url = reverse("hymns:search")
        assert url == "/busca/"
        assert resolve(url).func == views.search_view

    def test_url_namespace(self):
        """Test that URLs use the correct namespace."""
        # All these should not raise NoReverseMatch
        reverse("hymns:home")
        reverse("hymns:hymnbook_list")
        reverse("hymns:search")
        # This confirms the 'hymns' namespace is properly configured
        assert True
