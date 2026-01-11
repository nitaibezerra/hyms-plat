"""
Tests for HymnBookVersion model.
"""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.hymns.models import HymnBook, HymnBookVersion
from apps.users.models import User


@pytest.mark.django_db
class TestHymnBookVersionModel:
    """Tests for HymnBookVersion model."""

    def test_create_version(self, hymn_book, django_user_model):
        """Test creating a hymnbook version."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        version = HymnBookVersion.objects.create(
            hymn_book=hymn_book,
            version_name="Edição 2020",
            description="Versão revisada com correções",
            uploaded_by=user,
            is_primary=False,
        )

        assert version.id is not None
        assert version.hymn_book == hymn_book
        assert version.version_name == "Edição 2020"
        assert version.uploaded_by == user
        assert version.is_primary is False

    def test_version_string_representation(self, hymn_book):
        """Test __str__ method."""
        version = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Edição 2020"
        )

        assert str(version) == f"{hymn_book.name} - Edição 2020"

    def test_is_primary_removes_other_primaries(self, hymn_book):
        """Test that setting is_primary=True removes flag from other versions."""
        # Cria primeira versão primária
        version1 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Versão 1", is_primary=True
        )

        assert version1.is_primary is True

        # Cria segunda versão primária
        version2 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Versão 2", is_primary=True
        )

        # Recarrega primeira versão
        version1.refresh_from_db()

        assert version2.is_primary is True
        assert version1.is_primary is False

    def test_multiple_non_primary_versions(self, hymn_book):
        """Test creating multiple non-primary versions."""
        version1 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Versão 1", is_primary=False
        )

        version2 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Versão 2", is_primary=False
        )

        assert version1.is_primary is False
        assert version2.is_primary is False

    def test_version_with_files(self, hymn_book):
        """Test version with PDF and YAML files."""
        pdf_file = SimpleUploadedFile("test.pdf", b"PDF content", content_type="application/pdf")
        yaml_file = SimpleUploadedFile("test.yaml", b"yaml: content", content_type="text/yaml")

        version = HymnBookVersion.objects.create(
            hymn_book=hymn_book,
            version_name="Com Arquivos",
            pdf_file=pdf_file,
            yaml_file=yaml_file,
        )

        assert version.pdf_file.name.endswith(".pdf")
        assert version.yaml_file.name.endswith(".yaml")

    def test_version_ordering(self, hymn_book):
        """Test that versions are ordered by is_primary desc, then created_at desc."""
        version1 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Antiga", is_primary=False
        )

        version2 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Primária", is_primary=True
        )

        version3 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Recente", is_primary=False
        )

        versions = list(HymnBookVersion.objects.filter(hymn_book=hymn_book))

        # Primária deve vir primeiro
        assert versions[0] == version2
        # Depois as mais recentes
        assert versions[1] == version3
        assert versions[2] == version1

    def test_version_cascade_delete(self, hymn_book):
        """Test that versions are deleted when hymnbook is deleted."""
        version = HymnBookVersion.objects.create(hymn_book=hymn_book, version_name="Test")

        hymn_book.delete()

        assert not HymnBookVersion.objects.filter(id=version.id).exists()

    def test_version_without_uploaded_by(self, hymn_book):
        """Test creating version without uploaded_by (nullable)."""
        version = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Sem Usuário", uploaded_by=None
        )

        assert version.uploaded_by is None

    def test_version_blank_description(self, hymn_book):
        """Test creating version with blank description."""
        version = HymnBookVersion.objects.create(hymn_book=hymn_book, version_name="Test")

        assert version.description == ""


@pytest.mark.django_db
class TestHymnBookVersionRelationships:
    """Tests for HymnBookVersion relationships."""

    def test_hymnbook_versions_relationship(self, hymn_book):
        """Test reverse relationship from HymnBook to versions."""
        version1 = HymnBookVersion.objects.create(hymn_book=hymn_book, version_name="V1")
        version2 = HymnBookVersion.objects.create(hymn_book=hymn_book, version_name="V2")

        versions = hymn_book.versions.all()

        assert versions.count() == 2
        assert version1 in versions
        assert version2 in versions

    def test_user_uploaded_versions_relationship(self, hymn_book, django_user_model):
        """Test reverse relationship from User to uploaded_versions."""
        user = django_user_model.objects.create_user(
            username="uploader", email="uploader@example.com", password="pass123"
        )

        version1 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="V1", uploaded_by=user
        )

        version2 = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="V2", uploaded_by=user
        )

        uploaded = user.uploaded_versions.all()

        assert uploaded.count() == 2
        assert version1 in uploaded
        assert version2 in uploaded

    def test_set_null_on_user_delete(self, hymn_book, django_user_model):
        """Test that uploaded_by is set to null when user is deleted."""
        user = django_user_model.objects.create_user(
            username="temp", email="temp@example.com", password="pass123"
        )

        version = HymnBookVersion.objects.create(
            hymn_book=hymn_book, version_name="Test", uploaded_by=user
        )

        user.delete()
        version.refresh_from_db()

        assert version.uploaded_by is None
