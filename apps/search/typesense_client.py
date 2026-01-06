"""
TypeSense client configuration and utilities.
"""

from django.conf import settings
from typesense import Client


def get_typesense_client():
    """Get TypeSense client instance."""
    return Client(
        {
            "nodes": [
                {
                    "host": settings.TYPESENSE_HOST,
                    "port": settings.TYPESENSE_PORT,
                    "protocol": settings.TYPESENSE_PROTOCOL,
                }
            ],
            "api_key": settings.TYPESENSE_API_KEY,
            "connection_timeout_seconds": 2,
        }
    )


# Schema for hymns collection
HYMNS_SCHEMA = {
    "name": "hymns",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "hymn_book_id", "type": "string"},
        {"name": "hymn_book_name", "type": "string", "facet": True},
        {"name": "hymn_book_slug", "type": "string"},
        {"name": "owner_name", "type": "string", "facet": True},
        {"name": "number", "type": "int32", "sort": True},
        {"name": "title", "type": "string"},
        {"name": "text", "type": "string"},
        {"name": "style", "type": "string", "facet": True, "optional": True},
        {"name": "received_at", "type": "int64", "optional": True},  # Unix timestamp
    ],
    "default_sorting_field": "number",
}


def create_hymns_collection():
    """Create or recreate the hymns collection in TypeSense."""
    client = get_typesense_client()

    # Drop collection if it exists
    try:
        client.collections["hymns"].delete()
    except Exception:
        pass

    # Create collection
    return client.collections.create(HYMNS_SCHEMA)


def index_hymn(hymn):
    """Index a single hymn in TypeSense."""
    client = get_typesense_client()

    # Prepare document
    doc = {
        "id": str(hymn.id),
        "hymn_book_id": str(hymn.hymn_book.id),
        "hymn_book_name": hymn.hymn_book.name,
        "hymn_book_slug": hymn.hymn_book.slug,
        "owner_name": hymn.hymn_book.owner_name,
        "number": hymn.number,
        "title": hymn.title,
        "text": hymn.text,
    }

    # Add optional fields
    if hymn.style:
        doc["style"] = hymn.style

    if hymn.received_at:
        # Convert to Unix timestamp
        import time

        doc["received_at"] = int(time.mktime(hymn.received_at.timetuple()))

    # Upsert document
    return client.collections["hymns"].documents.upsert(doc)


def delete_hymn(hymn_id):
    """Delete a hymn from TypeSense index."""
    client = get_typesense_client()
    try:
        client.collections["hymns"].documents[str(hymn_id)].delete()
    except Exception:
        pass


def search_hymns(query, filters=None, per_page=20, page=1):
    """
    Search hymns in TypeSense.

    Args:
        query: Search query string
        filters: Optional filter string (e.g., "hymn_book_name:O Cruzeiro")
        per_page: Results per page
        page: Page number

    Returns:
        TypeSense search results
    """
    client = get_typesense_client()

    search_parameters = {
        "q": query,
        "query_by": "title,text,hymn_book_name,owner_name",
        "per_page": per_page,
        "page": page,
    }

    if filters:
        search_parameters["filter_by"] = filters

    return client.collections["hymns"].documents.search(search_parameters)


def reindex_all_hymns():
    """Reindex all hymns in TypeSense."""
    from apps.hymns.models import Hymn

    # Recreate collection
    create_hymns_collection()

    # Index all hymns
    hymns = Hymn.objects.select_related("hymn_book").all()
    count = 0

    for hymn in hymns:
        index_hymn(hymn)
        count += 1

    return count
