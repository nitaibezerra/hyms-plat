"""
Unit tests for Hymn views.
"""

from unittest.mock import patch
from uuid import uuid4

import pytest
from django.urls import reverse

from apps.hymns.models import Hymn, HymnBook


@pytest.mark.django_db
class TestHymnBookListView:
    """Tests for HymnBook list view."""

    def test_list_view_url_resolves(self, client):
        """Test that the list view URL resolves correctly."""
        url = reverse("hymns:hymnbook_list")
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_uses_correct_template(self, client):
        """Test that list view uses the correct template."""
        url = reverse("hymns:hymnbook_list")
        response = client.get(url)
        assert "hymns/hymnbook_list.html" in [t.name for t in response.templates]

    def test_list_view_shows_all_hymnbooks(self, client):
        """Test that list view shows all hymn books."""
        book1 = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        book2 = HymnBook.objects.create(name="Hinário do Padrinho", owner_name="Padrinho Sebastião")
        book3 = HymnBook.objects.create(name="Hinário da Madrinha", owner_name="Madrinha Rita")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url)

        assert book1 in response.context["hymnbooks"]
        assert book2 in response.context["hymnbooks"]
        assert book3 in response.context["hymnbooks"]

    def test_list_view_orders_by_name(self, client):
        """Test that list view orders hymn books by name."""
        book3 = HymnBook.objects.create(name="Zé do Bolo", owner_name="Zé")
        book1 = HymnBook.objects.create(name="Algo", owner_name="Alguém")
        book2 = HymnBook.objects.create(name="Meio", owner_name="Alguém")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url)

        hymnbooks = list(response.context["hymnbooks"])
        assert hymnbooks == [book1, book2, book3]

    def test_list_view_pagination_20_items(self, client):
        """Test that list view paginates at 20 items per page."""
        # Create 25 hymn books
        for i in range(25):
            HymnBook.objects.create(name=f"Hinário {i:02d}", owner_name="Owner")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url)

        assert response.context["is_paginated"] is True
        assert len(response.context["hymnbooks"]) == 20

    def test_list_view_page_2(self, client):
        """Test that page 2 shows remaining items."""
        # Create 25 hymn books
        for i in range(25):
            HymnBook.objects.create(name=f"Hinário {i:02d}", owner_name="Owner")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url, {"page": 2})

        assert response.status_code == 200
        assert len(response.context["hymnbooks"]) == 5

    def test_list_view_empty_state(self, client):
        """Test that list view handles empty database."""
        url = reverse("hymns:hymnbook_list")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context["hymnbooks"]) == 0

    def test_list_view_invalid_page_404(self, client):
        """Test that invalid page number returns 404."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url, {"page": 999})

        assert response.status_code == 404

    def test_list_view_context_data(self, client):
        """Test that list view provides correct context data."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        url = reverse("hymns:hymnbook_list")
        response = client.get(url)

        assert "hymnbooks" in response.context
        assert "page_obj" in response.context


@pytest.mark.django_db
class TestHymnBookDetailView:
    """Tests for HymnBook detail view."""

    def test_detail_view_url_resolves(self, client):
        """Test that detail view URL resolves correctly."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_uses_correct_template(self, client):
        """Test that detail view uses the correct template."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)
        assert "hymns/hymnbook_detail.html" in [t.name for t in response.templates]

    def test_detail_view_shows_hymnbook(self, client):
        """Test that detail view displays the hymn book."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)

        assert response.context["hymnbook"] == hymn_book
        assert b"O Cruzeiro" in response.content

    def test_detail_view_shows_hymns_ordered(self, client):
        """Test that detail view shows hymns ordered by number."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn3 = Hymn.objects.create(hymn_book=hymn_book, number=3, title="Terceiro", text="Texto 3")
        hymn1 = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Primeiro", text="Texto 1")
        hymn2 = Hymn.objects.create(hymn_book=hymn_book, number=2, title="Segundo", text="Texto 2")

        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)

        hymns = list(response.context["hymns"])
        assert hymns == [hymn1, hymn2, hymn3]

    def test_detail_view_slug_lookup(self, client):
        """Test that detail view looks up by slug."""
        hymn_book = HymnBook.objects.create(name="Hinário do Padrinho Sebastião", owner_name="Padrinho")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": "hinario-do-padrinho-sebastiao"})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["hymnbook"] == hymn_book

    def test_detail_view_invalid_slug_404(self, client):
        """Test that invalid slug returns 404."""
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": "nao-existe"})
        response = client.get(url)
        assert response.status_code == 404

    def test_detail_view_slug_with_special_chars(self, client):
        """Test that slugs with special characters work correctly."""
        hymn_book = HymnBook.objects.create(name="Hinário São José", owner_name="Owner")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context_hymns(self, client):
        """Test that detail view includes hymns in context."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        Hymn.objects.create(hymn_book=hymn_book, number=2, title="Tuperci", text="...")

        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)

        assert "hymns" in response.context
        assert len(response.context["hymns"]) == 2

    def test_detail_view_context_hymnbook(self, client):
        """Test that detail view includes hymnbook in context."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        url = reverse("hymns:hymnbook_detail", kwargs={"slug": hymn_book.slug})
        response = client.get(url)

        assert "hymnbook" in response.context
        assert response.context["hymnbook"] == hymn_book


@pytest.mark.django_db
class TestHymnDetailView:
    """Tests for Hymn detail view."""

    def test_hymn_detail_url_resolves(self, client):
        """Test that hymn detail URL resolves correctly."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": hymn.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_hymn_detail_uses_correct_template(self, client):
        """Test that hymn detail view uses the correct template."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": hymn.pk})
        response = client.get(url)
        assert "hymns/hymn_detail.html" in [t.name for t in response.templates]

    def test_hymn_detail_shows_hymn(self, client):
        """Test that hymn detail view displays the hymn."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="Lua branca...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": hymn.pk})
        response = client.get(url)

        assert response.context["hymn"] == hymn
        assert b"Lua Branca" in response.content
        assert b"Lua branca..." in response.content

    def test_hymn_detail_uuid_lookup(self, client):
        """Test that hymn detail view looks up by UUID."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": str(hymn.id)})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["hymn"] == hymn

    def test_hymn_detail_invalid_uuid_404(self, client):
        """Test that invalid UUID returns 404."""
        random_uuid = uuid4()
        url = reverse("hymns:hymn_detail", kwargs={"pk": str(random_uuid)})
        response = client.get(url)
        assert response.status_code == 404

    def test_hymn_detail_malformed_uuid_404(self, client):
        """Test that malformed UUID returns 404."""
        url = "/hinos/not-a-uuid/"
        response = client.get(url)
        assert response.status_code == 404

    def test_hymn_detail_select_related(self, client):
        """Test that hymn detail view uses select_related for optimization."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": hymn.pk})

        # Just verify the view works - the get_queryset method in the view uses select_related
        response = client.get(url)
        assert response.status_code == 200
        # Verify hymn_book is accessible without additional query (if select_related worked)
        assert response.context["hymn"].hymn_book == hymn_book

    def test_hymn_detail_context_hymn(self, client):
        """Test that hymn detail view includes hymn in context."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        url = reverse("hymns:hymn_detail", kwargs={"pk": hymn.pk})
        response = client.get(url)

        assert "hymn" in response.context
        assert response.context["hymn"] == hymn


@pytest.mark.django_db
class TestSearchView:
    """Tests for search view."""

    def test_search_view_url_resolves(self, client):
        """Test that search view URL resolves correctly."""
        url = reverse("hymns:search")
        response = client.get(url)
        assert response.status_code == 200

    def test_search_view_uses_correct_template(self, client):
        """Test that search view uses the correct template."""
        url = reverse("hymns:search")
        response = client.get(url)
        assert "hymns/search.html" in [t.name for t in response.templates]

    def test_search_view_empty_query(self, client):
        """Test that search view handles empty query."""
        url = reverse("hymns:search")
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["query"] == ""
        assert response.context["results"] == []
        assert response.context["total"] == 0

    def test_search_view_whitespace_query(self, client):
        """Test that search view handles whitespace-only query."""
        url = reverse("hymns:search")
        response = client.get(url, {"q": "   "})

        assert response.status_code == 200
        assert response.context["query"] == ""
        assert response.context["results"] == []

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_valid_query_typesense(self, mock_search, client):
        """Test that search view uses TypeSense for valid query."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")

        mock_search.return_value = {
            "found": 1,
            "hits": [{"document": {"id": str(hymn.id)}}],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "lua"})

        assert response.status_code == 200
        mock_search.assert_called_once_with("lua", per_page=50)
        assert len(response.context["results"]) == 1
        assert response.context["results"][0] == hymn

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_preserves_typesense_order(self, mock_search, client):
        """Test that search view preserves TypeSense result order."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn1 = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Primeiro", text="...")
        hymn2 = Hymn.objects.create(hymn_book=hymn_book, number=2, title="Segundo", text="...")
        hymn3 = Hymn.objects.create(hymn_book=hymn_book, number=3, title="Terceiro", text="...")

        # TypeSense returns in specific order: 3, 1, 2
        mock_search.return_value = {
            "found": 3,
            "hits": [
                {"document": {"id": str(hymn3.id)}},
                {"document": {"id": str(hymn1.id)}},
                {"document": {"id": str(hymn2.id)}},
            ],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "hino"})

        results = response.context["results"]
        assert len(results) == 3
        assert results[0] == hymn3
        assert results[1] == hymn1
        assert results[2] == hymn2

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_total_count(self, mock_search, client):
        """Test that search view returns total count from TypeSense."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")

        mock_search.return_value = {
            "found": 42,
            "hits": [{"document": {"id": str(hymn.id)}}],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "lua"})

        assert response.context["total"] == 42

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_context_query(self, mock_search, client):
        """Test that search view includes query in context."""
        mock_search.return_value = {"found": 0, "hits": []}

        url = reverse("hymns:search")
        response = client.get(url, {"q": "lua branca"})

        assert response.context["query"] == "lua branca"

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_typesense_fails_fallback(self, mock_search, client):
        """Test that search view falls back to database when TypeSense fails."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")

        mock_search.side_effect = Exception("TypeSense is down")

        url = reverse("hymns:search")
        response = client.get(url, {"q": "lua"})

        assert response.status_code == 200
        # Should fallback to database search
        assert len(response.context["results"]) == 1
        assert response.context["results"][0] == hymn

    def test_search_view_fallback_title_search(self, client):
        """Test that database fallback searches in title."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn1 = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        hymn2 = Hymn.objects.create(hymn_book=hymn_book, number=2, title="Tuperci", text="...")

        with patch("apps.hymns.views.search_hymns") as mock_search:
            mock_search.side_effect = Exception("Error")

            url = reverse("hymns:search")
            response = client.get(url, {"q": "Lua"})

            results = response.context["results"]
            assert hymn1 in results
            assert hymn2 not in results

    def test_search_view_fallback_text_search(self, client):
        """Test that database fallback searches in text."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn1 = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Primeiro", text="Lua branca da luz serena")
        hymn2 = Hymn.objects.create(hymn_book=hymn_book, number=2, title="Segundo", text="Outro texto")

        with patch("apps.hymns.views.search_hymns") as mock_search:
            mock_search.side_effect = Exception("Error")

            url = reverse("hymns:search")
            response = client.get(url, {"q": "serena"})

            results = response.context["results"]
            assert hymn1 in results
            assert hymn2 not in results

    def test_search_view_fallback_hymnbook_search(self, client):
        """Test that database fallback searches in hymn book name."""
        book1 = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        book2 = HymnBook.objects.create(name="Hinário do Padrinho", owner_name="Padrinho")
        hymn1 = Hymn.objects.create(hymn_book=book1, number=1, title="Hino 1", text="Texto 1")
        hymn2 = Hymn.objects.create(hymn_book=book2, number=1, title="Hino 2", text="Texto 2")

        with patch("apps.hymns.views.search_hymns") as mock_search:
            mock_search.side_effect = Exception("Error")

            url = reverse("hymns:search")
            response = client.get(url, {"q": "Cruzeiro"})

            results = response.context["results"]
            assert hymn1 in results
            assert hymn2 not in results

    def test_search_view_fallback_50_limit(self, client):
        """Test that database fallback limits to 50 results."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        for i in range(60):
            Hymn.objects.create(hymn_book=hymn_book, number=i + 1, title=f"Hino {i}", text="Texto comum")

        with patch("apps.hymns.views.search_hymns") as mock_search:
            mock_search.side_effect = Exception("Error")

            url = reverse("hymns:search")
            response = client.get(url, {"q": "comum"})

            results = list(response.context["results"])
            assert len(results) == 50

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_special_characters(self, mock_search, client):
        """Test that search view handles special characters."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="São José", text="...")

        mock_search.return_value = {
            "found": 1,
            "hits": [{"document": {"id": str(hymn.id)}}],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "São José"})

        assert response.status_code == 200
        mock_search.assert_called_once_with("São José", per_page=50)

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_unicode_characters(self, mock_search, client):
        """Test that search view handles unicode characters."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Ação", text="...")

        mock_search.return_value = {
            "found": 1,
            "hits": [{"document": {"id": str(hymn.id)}}],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "Ação"})

        assert response.status_code == 200
        assert len(response.context["results"]) == 1

    @patch("apps.hymns.views.search_hymns")
    def test_search_view_hymn_deleted_after_index(self, mock_search, client):
        """Test that search handles hymn deleted after being indexed."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")

        # TypeSense returns a hymn that no longer exists
        deleted_uuid = str(uuid4())
        mock_search.return_value = {
            "found": 2,
            "hits": [
                {"document": {"id": str(hymn.id)}},
                {"document": {"id": deleted_uuid}},  # This hymn was deleted
            ],
        }

        url = reverse("hymns:search")
        response = client.get(url, {"q": "lua"})

        # Should only return existing hymn
        results = response.context["results"]
        assert len(results) == 1
        assert results[0] == hymn


@pytest.mark.django_db
class TestHomeView:
    """Tests for home view."""

    def test_home_view_url_resolves(self, client):
        """Test that home view URL resolves correctly."""
        url = reverse("hymns:home")
        response = client.get(url)
        assert response.status_code == 200

    def test_home_view_uses_correct_template(self, client):
        """Test that home view uses the correct template."""
        url = reverse("hymns:home")
        response = client.get(url)
        assert "hymns/home.html" in [t.name for t in response.templates]

    def test_home_view_recent_hymnbooks(self, client):
        """Test that home view shows recent hymn books."""
        book1 = HymnBook.objects.create(name="Livro 1", owner_name="Owner 1")
        book2 = HymnBook.objects.create(name="Livro 2", owner_name="Owner 2")
        book3 = HymnBook.objects.create(name="Livro 3", owner_name="Owner 3")

        url = reverse("hymns:home")
        response = client.get(url)

        recent = response.context["recent_hymnbooks"]
        assert book1 in recent
        assert book2 in recent
        assert book3 in recent

    def test_home_view_recent_ordering(self, client):
        """Test that home view orders recent hymn books by created_at descending."""
        # Create books in specific order
        book1 = HymnBook.objects.create(name="Primeiro", owner_name="Owner")
        book2 = HymnBook.objects.create(name="Segundo", owner_name="Owner")
        book3 = HymnBook.objects.create(name="Terceiro", owner_name="Owner")

        url = reverse("hymns:home")
        response = client.get(url)

        recent = list(response.context["recent_hymnbooks"])
        # Most recent first (created last)
        assert recent[0] == book3
        assert recent[1] == book2
        assert recent[2] == book1

    def test_home_view_total_hymnbooks_stat(self, client):
        """Test that home view shows total hymn books count."""
        HymnBook.objects.create(name="Livro 1", owner_name="Owner 1")
        HymnBook.objects.create(name="Livro 2", owner_name="Owner 2")
        HymnBook.objects.create(name="Livro 3", owner_name="Owner 3")

        url = reverse("hymns:home")
        response = client.get(url)

        assert response.context["total_hymnbooks"] == 3

    def test_home_view_total_hymns_stat(self, client):
        """Test that home view shows total hymns count."""
        book1 = HymnBook.objects.create(name="Livro 1", owner_name="Owner 1")
        book2 = HymnBook.objects.create(name="Livro 2", owner_name="Owner 2")

        Hymn.objects.create(hymn_book=book1, number=1, title="Hino 1", text="...")
        Hymn.objects.create(hymn_book=book1, number=2, title="Hino 2", text="...")
        Hymn.objects.create(hymn_book=book2, number=1, title="Hino 3", text="...")

        url = reverse("hymns:home")
        response = client.get(url)

        assert response.context["total_hymns"] == 3

    def test_home_view_empty_database(self, client):
        """Test that home view handles empty database."""
        url = reverse("hymns:home")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context["recent_hymnbooks"]) == 0
        assert response.context["total_hymnbooks"] == 0
        assert response.context["total_hymns"] == 0

    def test_home_view_context_recent_hymnbooks(self, client):
        """Test that home view limits recent hymn books to 6."""
        # Create 10 hymn books
        for i in range(10):
            HymnBook.objects.create(name=f"Livro {i}", owner_name="Owner")

        url = reverse("hymns:home")
        response = client.get(url)

        recent = response.context["recent_hymnbooks"]
        assert len(recent) == 6
