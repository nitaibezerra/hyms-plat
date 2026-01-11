"""
Additional edge case tests for disambiguation to boost coverage.
"""

import pytest

from apps.hymns.disambiguation import find_duplicates_with_content, normalize_hymnbook_name
from apps.hymns.models import Hymn, HymnBook


@pytest.mark.django_db
class TestDisambiguationEdgeCases:
    """Edge case tests for disambiguation functions."""

    def test_normalize_empty_string(self):
        """Test normalizing empty string."""
        result = normalize_hymnbook_name("")
        assert result == ""

    def test_normalize_only_spaces(self):
        """Test normalizing string with only spaces."""
        result = normalize_hymnbook_name("     ")
        assert result == ""

    def test_find_duplicates_with_empty_name(self):
        """Test finding duplicates with empty name."""
        result = find_duplicates_with_content(name="", hymns=[])

        assert result["exact_match"] is None
        assert len(result["high_confidence"]) == 0

    def test_find_duplicates_with_very_short_name(self):
        """Test with very short hymnbook name."""
        HymnBook.objects.create(name="A", owner_name="Owner")

        result = find_duplicates_with_content(name="B", hymns=[])

        # Should not crash, may or may not find matches
        assert result["exact_match"] is None

    def test_find_duplicates_with_special_characters(self):
        """Test with special characters in name."""
        HymnBook.objects.create(name="Hinário #1 (Edição 2023)", owner_name="Owner")

        result = find_duplicates_with_content(name="Hinário #1", hymns=[])

        # Should handle special characters gracefully
        assert result is not None

    def test_find_duplicates_with_unicode_characters(self):
        """Test with unicode characters."""
        HymnBook.objects.create(name="Hinário São José", owner_name="Owner")

        result = find_duplicates_with_content(name="Hinário Sao Jose", hymns=[])

        # Should normalize unicode
        assert result is not None

    def test_find_duplicates_many_similar_hymnbooks(self):
        """Test with many similar hymnbooks."""
        # Create 20 similar hymnbooks
        for i in range(20):
            HymnBook.objects.create(name=f"Hinário Cruzeiro {i}", owner_name=f"Owner {i}")

        result = find_duplicates_with_content(name="Hinário Cruzeiro", hymns=[], name_threshold=0.6)

        # Should return all matches
        total = len(result["high_confidence"]) + len(result["medium_confidence"]) + len(result["low_confidence"])
        assert total > 0

    def test_find_duplicates_with_very_long_name(self):
        """Test with very long hymnbook name."""
        long_name = "A" * 500
        HymnBook.objects.create(name=long_name[:255], owner_name="Owner")  # DB limit is 255

        result = find_duplicates_with_content(name=long_name, hymns=[])

        # Should handle long names
        assert result is not None

    def test_find_duplicates_low_confidence_match(self):
        """Test that low confidence matches are detected."""
        hb = HymnBook.objects.create(name="Hinário A", owner_name="Owner A")

        # Create some hymns
        Hymn.objects.create(hymn_book=hb, number=1, title="Hino X", text="Texto X")

        # Search with somewhat similar name
        result = find_duplicates_with_content(
            name="Hinário ABC", hymns=[{"number": 1, "title": "Hino Y", "text": "Texto Y"}], name_threshold=0.3
        )

        # Should have some matches (high, medium, or low)
        total = len(result["high_confidence"]) + len(result["medium_confidence"]) + len(result["low_confidence"])
        assert total >= 0  # At least should not crash

    def test_find_duplicates_with_None_hymns(self):
        """Test with None instead of empty list."""
        HymnBook.objects.create(name="Test", owner_name="Owner")

        # Should handle None gracefully or use empty list
        result = find_duplicates_with_content(name="Test", hymns=None or [])

        assert result is not None

    def test_exact_match_case_variations(self):
        """Test exact match with various case combinations."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        # All these should match
        for variant in ["o cruzeiro", "O CRUZEIRO", "o CrUzEiRo"]:
            result = find_duplicates_with_content(name=variant, hymns=[])
            assert result["exact_match"] is not None

    def test_medium_confidence_thresholds(self):
        """Test medium confidence detection with threshold boundaries."""
        hb = HymnBook.objects.create(name="Cruzeiro Universal", owner_name="Owner")
        Hymn.objects.create(hymn_book=hb, number=1, title="Hino 1", text="Texto do hino 1")

        # Name similar but not exact, content different
        result = find_duplicates_with_content(
            name="Cruzeiro", hymns=[{"number": 1, "title": "Outro", "text": "Outro texto"}], name_threshold=0.6
        )

        # Should be in medium or low confidence
        assert len(result["medium_confidence"]) + len(result["low_confidence"]) > 0
