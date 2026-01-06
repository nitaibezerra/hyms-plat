"""
Management command to reindex all hymns in TypeSense.

Usage:
    python manage.py reindex_typesense
"""

from django.core.management.base import BaseCommand

from apps.search.typesense_client import reindex_all_hymns


class Command(BaseCommand):
    help = "Reindex all hymns in TypeSense"

    def handle(self, *args, **options):
        self.stdout.write("Reindexing hymns in TypeSense...")

        try:
            count = reindex_all_hymns()
            self.stdout.write(self.style.SUCCESS(f"✓ Successfully reindexed {count} hymns"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reindexing: {e}"))
            raise
