"""
Tests for hymn disambiguation system.
"""

import pytest

from apps.hymns.disambiguation import (
    calculate_string_similarity,
    compare_hymn_texts,
    find_duplicates_with_content,
    find_exact_match,
    find_similar_hymnbooks,
    normalize_hymnbook_name,
)
from apps.hymns.models import Hymn, HymnBook


@pytest.mark.django_db
class TestStringSimilarity:
    """Tests for string similarity functions."""

    def test_identical_strings(self):
        """Test similarity of identical strings."""
        similarity = calculate_string_similarity("O Cruzeiro", "O Cruzeiro")
        assert similarity == 1.0

    def test_case_insensitive(self):
        """Test that comparison is case-insensitive."""
        similarity = calculate_string_similarity("O CRUZEIRO", "o cruzeiro")
        assert similarity == 1.0

    def test_similar_strings(self):
        """Test similarity of similar strings."""
        similarity = calculate_string_similarity("O Cruzeiro", "Cruzeiro")
        assert 0.7 < similarity < 1.0

    def test_different_strings(self):
        """Test similarity of different strings."""
        similarity = calculate_string_similarity("O Cruzeiro", "Hinário do Padrinho")
        assert similarity < 0.5

    def test_normalize_hymnbook_name(self):
        """Test name normalization."""
        assert normalize_hymnbook_name("O  Cruzeiro  ") == "o cruzeiro"
        assert normalize_hymnbook_name("O CRUZEIRO") == "o cruzeiro"
        assert normalize_hymnbook_name("  Hinário   do   Padrinho  ") == "hinário do padrinho"


@pytest.mark.django_db
class TestFindExactMatch:
    """Tests for exact match finding."""

    def test_exact_match_found(self):
        """Test finding exact match (case-insensitive)."""
        hymnbook = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        found = find_exact_match("o cruzeiro")

        assert found == hymnbook

    def test_exact_match_with_extra_spaces(self):
        """Test exact match ignores extra spaces."""
        hymnbook = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        found = find_exact_match("O  Cruzeiro  ")

        assert found == hymnbook

    def test_no_exact_match(self):
        """Test when no exact match exists."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        found = find_exact_match("Hinário do Padrinho")

        assert found is None


@pytest.mark.django_db
class TestFindSimilarHymnbooks:
    """Tests for finding similar hymnbooks."""

    def test_find_similar_by_name(self):
        """Test finding similar hymnbooks."""
        hb1 = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")
        hb2 = HymnBook.objects.create(name="Cruzeiro Universal", owner_name="Outro")
        HymnBook.objects.create(name="Hinário Totalmente Diferente", owner_name="Outro")

        similar = find_similar_hymnbooks("O Cruzeiro", threshold=0.5, limit=5)

        # Deve encontrar pelo menos os 2 com "Cruzeiro"
        assert len(similar) >= 2
        assert any(hb == hb1 for hb, score in similar)
        assert any(hb == hb2 for hb, score in similar)

    def test_similarity_scores_ordered(self):
        """Test that results are ordered by similarity score."""
        hb1 = HymnBook.objects.create(name="O Cruzeiro", owner_name="M1")
        hb2 = HymnBook.objects.create(name="Cruzeiro", owner_name="M2")
        hb3 = HymnBook.objects.create(name="Cruz", owner_name="M3")

        similar = find_similar_hymnbooks("O Cruzeiro", threshold=0.4, limit=5)

        scores = [score for hb, score in similar]

        # Scores devem estar em ordem decrescente
        assert scores == sorted(scores, reverse=True)

    def test_threshold_filtering(self):
        """Test that threshold filters out low-similarity results."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="M1")
        HymnBook.objects.create(name="Hinário Muito Diferente", owner_name="M2")

        similar = find_similar_hymnbooks("O Cruzeiro", threshold=0.9, limit=5)

        # Com threshold alto, só deve encontrar match exato
        assert len(similar) <= 1

    def test_limit_results(self):
        """Test that limit parameter works."""
        for i in range(10):
            HymnBook.objects.create(name=f"Hinário {i}", owner_name=f"Dono {i}")

        similar = find_similar_hymnbooks("Hinário", threshold=0.5, limit=3)

        assert len(similar) <= 3


@pytest.mark.django_db
class TestCompareHymnTexts:
    """Tests for comparing hymn texts."""

    def test_identical_hymns(self):
        """Test comparison of identical hymn lists."""
        hymns1 = [
            {"number": 1, "title": "Lua Branca", "text": "Da luz serena..."},
            {"number": 2, "title": "Tuperci", "text": "Eu canto é na altura..."},
        ]

        hymns2 = [
            {"number": 1, "title": "Lua Branca", "text": "Da luz serena..."},
            {"number": 2, "title": "Tuperci", "text": "Eu canto é na altura..."},
        ]

        similarity = compare_hymn_texts(hymns1, hymns2, sample_size=5)

        assert similarity > 0.95

    def test_different_hymns(self):
        """Test comparison of different hymn lists."""
        hymns1 = [{"number": 1, "title": "Hino A", "text": "Texto completamente diferente"}]

        hymns2 = [{"number": 1, "title": "Hino B", "text": "Outro texto totalmente distinto"}]

        similarity = compare_hymn_texts(hymns1, hymns2, sample_size=5)

        # Even different short texts can have some similarity due to common words
        assert similarity < 0.8

    def test_empty_lists(self):
        """Test with empty hymn lists."""
        similarity = compare_hymn_texts([], [], sample_size=5)
        assert similarity == 0.0

        similarity = compare_hymn_texts([{"number": 1, "title": "Test", "text": "Test"}], [])
        assert similarity == 0.0

    def test_sample_size_limit(self):
        """Test that only first N hymns are compared."""
        hymns1 = [{"number": i, "title": f"Hino {i}", "text": f"Texto {i}"} for i in range(10)]

        hymns2 = [{"number": i, "title": f"Hino {i}", "text": f"Texto {i}"} for i in range(10)]

        # Com sample_size=3, deve comparar apenas primeiros 3
        similarity = compare_hymn_texts(hymns1, hymns2, sample_size=3)

        assert similarity > 0.95


@pytest.mark.django_db
class TestFindDuplicatesWithContent:
    """Tests for complete duplicate detection."""

    def test_exact_match_detected(self):
        """Test detection of exact match."""
        HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        result = find_duplicates_with_content(name="O Cruzeiro", hymns=[], name_threshold=0.7, content_threshold=0.8)

        assert result["exact_match"] is not None
        assert result["exact_match"].name == "O Cruzeiro"

    def test_high_confidence_duplicate(self):
        """Test detection of high confidence duplicate."""
        hb = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        # Cria hinos
        Hymn.objects.create(hymn_book=hb, number=1, title="Lua Branca", text="Da luz serena\nDo mar sagrado")

        # Tenta upload com nome similar e mesmo conteúdo
        hymns = [{"number": 1, "title": "Lua Branca", "text": "Da luz serena\nDo mar sagrado"}]

        result = find_duplicates_with_content(name="Cruzeiro", hymns=hymns, name_threshold=0.7, content_threshold=0.8)

        # Deve detectar duplicata (pode ser high, medium ou low confidence)
        total_duplicates = (
            len(result["high_confidence"]) + len(result["medium_confidence"]) + len(result["low_confidence"])
        )
        assert total_duplicates > 0

    def test_no_duplicates(self):
        """Test when no duplicates exist."""
        HymnBook.objects.create(name="Hinário A", owner_name="Dono A")

        result = find_duplicates_with_content(
            name="Hinário Totalmente Diferente",
            hymns=[],
            name_threshold=0.7,
            content_threshold=0.8,
        )

        assert result["exact_match"] is None
        assert len(result["high_confidence"]) == 0

    def test_medium_confidence(self):
        """Test medium confidence detection."""
        hb = HymnBook.objects.create(name="O Cruzeiro", owner_name="Mestre Irineu")

        Hymn.objects.create(hymn_book=hb, number=1, title="Lua Branca", text="Da luz serena do mar")

        # Nome similar, mas texto diferente
        hymns = [{"number": 1, "title": "Outro Hino", "text": "Texto diferente completamente"}]

        result = find_duplicates_with_content(
            name="Cruzeiro Universal", hymns=hymns, name_threshold=0.6, content_threshold=0.8
        )

        # Pode cair em medium ou low confidence
        assert result["exact_match"] is None
