"""
Tests for the reindex_typesense management command.
"""

import pytest
from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.core.management.base import CommandError


class TestReindexTypesenseCommand:
    """Test suite for reindex_typesense command."""

    @patch("apps.search.management.commands.reindex_typesense.reindex_all_hymns")
    def test_command_calls_reindex_function(self, mock_reindex, db):
        """Test that command calls reindex_all_hymns function."""
        mock_reindex.return_value = 10

        call_command("reindex_typesense")

        mock_reindex.assert_called_once()

    @patch("apps.search.management.commands.reindex_typesense.reindex_all_hymns")
    def test_outputs_success_message(self, mock_reindex, db, capsys):
        """Test that command outputs success message with count."""
        mock_reindex.return_value = 25

        call_command("reindex_typesense")

        captured = capsys.readouterr()
        assert "Reindexing hymns in TypeSense" in captured.out
        assert "Successfully reindexed 25 hymns" in captured.out

    @patch("apps.search.management.commands.reindex_typesense.reindex_all_hymns")
    def test_handles_exception_from_reindex_function(self, mock_reindex, db, capsys):
        """Test that command handles exceptions from reindex_all_hymns."""
        mock_reindex.side_effect = Exception("TypeSense connection error")

        with pytest.raises(Exception, match="TypeSense connection error"):
            call_command("reindex_typesense")

        captured = capsys.readouterr()
        assert "Error reindexing" in captured.out

    @patch("apps.search.management.commands.reindex_typesense.reindex_all_hymns")
    def test_outputs_reindexing_start_message(self, mock_reindex, db, capsys):
        """Test that command outputs message before starting reindex."""
        mock_reindex.return_value = 0

        call_command("reindex_typesense")

        captured = capsys.readouterr()
        assert "Reindexing hymns in TypeSense" in captured.out

    @patch("apps.search.management.commands.reindex_typesense.reindex_all_hymns")
    def test_handles_zero_hymns_reindexed(self, mock_reindex, db, capsys):
        """Test that command handles case when no hymns are reindexed."""
        mock_reindex.return_value = 0

        call_command("reindex_typesense")

        captured = capsys.readouterr()
        assert "Successfully reindexed 0 hymns" in captured.out
