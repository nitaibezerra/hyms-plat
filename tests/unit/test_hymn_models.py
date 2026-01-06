"""
Unit tests for Hymn models.
"""

import pytest
from django.db import IntegrityError

from apps.hymns.models import Hymn, HymnBook


@pytest.mark.django_db
class TestHymnBookModel:
    """Tests for HymnBook model."""

    def test_create_hymnbook(self):
        """Test creating a hymn book."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu", intro_name="Cruzeiro")
        assert hymn_book.id is not None
        assert hymn_book.name == "O Cruzeiro"
        assert hymn_book.owner_name == "Mestre Irineu"
        assert hymn_book.intro_name == "Cruzeiro"
        assert hymn_book.slug == "o-cruzeiro"

    def test_hymnbook_auto_slug(self):
        """Test that slug is auto-generated from name."""
        hymn_book = HymnBook.objects.create(name="Hinário do Padrinho Sebastião", owner_name="Padrinho Sebastião")
        assert hymn_book.slug == "hinario-do-padrinho-sebastiao"

    def test_hymnbook_unique_name(self):
        """Test that hymn book name must be unique."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        with pytest.raises(IntegrityError):
            HymnBook.objects.create(name="O Cruzeiro", owner_name="Outro")

    def test_hymnbook_str(self):
        """Test string representation."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        assert str(hymn_book) == "O Cruzeiro"

    def test_hymnbook_hymn_count(self):
        """Test hymn count property."""
        hymn_book = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        assert hymn_book.hymn_count == 0

        # Add hymns
        Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="Lua branca...")
        Hymn.objects.create(hymn_book=hymn_book, number=2, title="Tuperci", text="Tuperci...")
        assert hymn_book.hymn_count == 2

    def test_hymnbook_with_owner_user(self, user_factory):
        """Test hymn book with owner user link."""
        user = user_factory(email="mestre@example.com")
        hymn_book = HymnBook.objects.create(
            name="O Cruzeiro", owner_name="Mestre Irineu", owner_user=user
        )
        assert hymn_book.owner_user == user
        assert hymn_book in user.owned_hymnbooks.all()


@pytest.mark.django_db
class TestHymnModel:
    """Tests for Hymn model."""

    @pytest.fixture
    def hymn_book(self):
        """Create a hymn book for tests."""
        return HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

    def test_create_hymn(self, hymn_book):
        """Test creating a hymn."""
        hymn = Hymn.objects.create(
            hymn_book=hymn_book, number=1, title="Lua Branca", text="Lua branca...\nDa luz serena"
        )
        assert hymn.id is not None
        assert hymn.hymn_book == hymn_book
        assert hymn.number == 1
        assert hymn.title == "Lua Branca"
        assert hymn.text == "Lua branca...\nDa luz serena"

    def test_hymn_with_optional_fields(self, hymn_book):
        """Test hymn with all optional fields."""
        from datetime import date

        hymn = Hymn.objects.create(
            hymn_book=hymn_book,
            number=1,
            title="Lua Branca",
            text="Lua branca...",
            received_at=date(1930, 7, 15),
            offered_to="Padrinho Sebastião",
            style="Valsa",
            extra_instructions="Cantar devagar",
            repetitions="1-4, 5-8",
        )
        assert hymn.received_at == date(1930, 7, 15)
        assert hymn.offered_to == "Padrinho Sebastião"
        assert hymn.style == "Valsa"
        assert hymn.extra_instructions == "Cantar devagar"
        assert hymn.repetitions == "1-4, 5-8"

    def test_hymn_unique_number_per_book(self, hymn_book):
        """Test that hymn number must be unique within a hymn book."""
        Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        with pytest.raises(IntegrityError):
            Hymn.objects.create(hymn_book=hymn_book, number=1, title="Outro Hino", text="...")

    def test_hymn_same_number_different_books(self):
        """Test that same number can exist in different hymn books."""
        book1 = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        book2 = HymnBook.objects.create(name="Hinário do Padrinho Sebastião", owner_name="Padrinho Sebastião")

        hymn1 = Hymn.objects.create(hymn_book=book1, number=1, title="Lua Branca", text="...")
        hymn2 = Hymn.objects.create(hymn_book=book2, number=1, title="Outro Hino", text="...")

        assert hymn1.number == hymn2.number
        assert hymn1.hymn_book != hymn2.hymn_book

    def test_hymn_str(self, hymn_book):
        """Test string representation."""
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        assert str(hymn) == "O Cruzeiro - 1. Lua Branca"

    def test_hymn_full_title(self, hymn_book):
        """Test full_title property."""
        hymn = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        assert hymn.full_title == "O Cruzeiro - 1. Lua Branca"

    def test_hymn_ordering(self, hymn_book):
        """Test that hymns are ordered by hymn_book and number."""
        hymn3 = Hymn.objects.create(hymn_book=hymn_book, number=3, title="Terceiro", text="...")
        hymn1 = Hymn.objects.create(hymn_book=hymn_book, number=1, title="Primeiro", text="...")
        hymn2 = Hymn.objects.create(hymn_book=hymn_book, number=2, title="Segundo", text="...")

        hymns = list(Hymn.objects.all())
        assert hymns == [hymn1, hymn2, hymn3]

    def test_hymn_cascade_delete(self, hymn_book):
        """Test that hymns are deleted when hymn book is deleted."""
        Hymn.objects.create(hymn_book=hymn_book, number=1, title="Lua Branca", text="...")
        Hymn.objects.create(hymn_book=hymn_book, number=2, title="Tuperci", text="...")

        assert Hymn.objects.count() == 2
        hymn_book.delete()
        assert Hymn.objects.count() == 0
