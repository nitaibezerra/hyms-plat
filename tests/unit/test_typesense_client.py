"""
Testes unitários para o cliente TypeSense.

Fase 2 do plano de testes - 32 testes para cobertura >= 85%
"""

import time
from datetime import date
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest
from django.conf import settings

from apps.search.typesense_client import (
    HYMNS_SCHEMA,
    create_hymns_collection,
    delete_hymn,
    get_typesense_client,
    index_hymn,
    reindex_all_hymns,
    search_hymns,
)


class TestGetTypesenseClient:
    """Testa a função get_typesense_client()."""

    @patch("apps.search.typesense_client.Client")
    def test_creates_client_with_settings(self, mock_client_class):
        """Testa se cria o cliente com as configurações corretas do Django settings."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        client = get_typesense_client()

        # Verifica se Client foi chamado com os parâmetros corretos
        mock_client_class.assert_called_once_with(
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
        assert client == mock_client

    @patch("apps.search.typesense_client.Client")
    def test_uses_environment_variables(self, mock_client_class):
        """Testa se usa as variáveis de ambiente do Django."""
        with patch.object(settings, "TYPESENSE_HOST", "custom-host"):
            with patch.object(settings, "TYPESENSE_PORT", "9999"):
                with patch.object(settings, "TYPESENSE_PROTOCOL", "https"):
                    with patch.object(settings, "TYPESENSE_API_KEY", "custom-key"):
                        get_typesense_client()

                        call_args = mock_client_class.call_args[0][0]
                        assert call_args["nodes"][0]["host"] == "custom-host"
                        assert call_args["nodes"][0]["port"] == "9999"
                        assert call_args["nodes"][0]["protocol"] == "https"
                        assert call_args["api_key"] == "custom-key"

    @patch("apps.search.typesense_client.Client")
    def test_connection_timeout_2_seconds(self, mock_client_class):
        """Testa se o timeout de conexão é 2 segundos."""
        get_typesense_client()

        call_args = mock_client_class.call_args[0][0]
        assert call_args["connection_timeout_seconds"] == 2


class TestCreateHymnsCollection:
    """Testa a função create_hymns_collection()."""

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_creates_collection_fresh(self, mock_get_client):
        """Testa criação de collection em banco vazio."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula que a collection não existe (levanta exceção no delete)
        mock_client.collections["hymns"].delete.side_effect = Exception("Not found")

        create_hymns_collection()

        # Verifica que criou a collection
        mock_client.collections.create.assert_called_once_with(HYMNS_SCHEMA)

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_drops_existing_collection(self, mock_get_client):
        """Testa que deleta collection existente antes de criar."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula que a collection existe (delete não levanta exceção)
        # O MagicMock já cria automaticamente o método delete quando acessado

        create_hymns_collection()

        # Verifica que deletou a collection existente
        mock_client.collections["hymns"].delete.assert_called_once()
        # Verifica que criou a nova collection
        mock_client.collections.create.assert_called_once_with(HYMNS_SCHEMA)

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_handles_non_existent_collection(self, mock_get_client):
        """Testa que ignora erro quando collection não existe."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula que o delete levanta exceção
        mock_client.collections["hymns"].delete.side_effect = Exception("Collection not found")

        # Não deve levantar exceção
        create_hymns_collection()

        # Deve criar a collection mesmo assim
        mock_client.collections.create.assert_called_once_with(HYMNS_SCHEMA)

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_schema_structure(self, mock_get_client):
        """Testa se o schema tem a estrutura correta."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].delete.side_effect = Exception()

        create_hymns_collection()

        # Captura o schema passado para create
        call_args = mock_client.collections.create.call_args[0][0]

        assert call_args["name"] == "hymns"
        assert call_args["default_sorting_field"] == "number"

        # Verifica campos obrigatórios
        field_names = [f["name"] for f in call_args["fields"]]
        assert "id" in field_names
        assert "hymn_book_id" in field_names
        assert "hymn_book_name" in field_names
        assert "number" in field_names
        assert "title" in field_names
        assert "text" in field_names

        # Verifica campos opcionais
        assert "style" in field_names
        assert "received_at" in field_names


class TestIndexHymn:
    """Testa a função index_hymn()."""

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_indexes_minimal_hymn(self, mock_get_client):
        """Testa indexação de hino com campos mínimos."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Cria hino mock
        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário Teste"
        hymn.hymn_book.slug = "hinario-teste"
        hymn.hymn_book.owner_name = "João Silva"
        hymn.number = 42
        hymn.title = "Canto de Alegria"
        hymn.text = "Letra do hino aqui"
        hymn.style = ""
        hymn.received_at = None

        index_hymn(hymn)

        # Verifica que upsert foi chamado
        upsert_call = mock_client.collections["hymns"].documents.upsert
        upsert_call.assert_called_once()

        # Verifica documento
        doc = upsert_call.call_args[0][0]
        assert doc["id"] == str(hymn.id)
        assert doc["number"] == 42
        assert doc["title"] == "Canto de Alegria"
        assert "style" not in doc
        assert "received_at" not in doc

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_indexes_hymn_with_all_fields(self, mock_get_client):
        """Testa indexação de hino com todos os campos preenchidos."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Cria hino mock com todos os campos
        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "O Cruzeiro"
        hymn.hymn_book.slug = "o-cruzeiro"
        hymn.hymn_book.owner_name = "Maria Santos"
        hymn.number = 123
        hymn.title = "Marcha Gloriosa"
        hymn.text = "Texto completo do hino"
        hymn.style = "Marcha"
        hymn.received_at = date(2023, 5, 15)

        index_hymn(hymn)

        # Verifica documento completo
        doc = mock_client.collections["hymns"].documents.upsert.call_args[0][0]
        assert doc["style"] == "Marcha"
        assert "received_at" in doc
        assert isinstance(doc["received_at"], int)  # Unix timestamp

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_indexes_hymn_with_optional_fields_null(self, mock_get_client):
        """Testa que campos opcionais nulos não são incluídos no documento."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário"
        hymn.hymn_book.slug = "hinario"
        hymn.hymn_book.owner_name = "Dono"
        hymn.number = 1
        hymn.title = "Título"
        hymn.text = "Texto"
        hymn.style = None
        hymn.received_at = None

        index_hymn(hymn)

        doc = mock_client.collections["hymns"].documents.upsert.call_args[0][0]
        assert "style" not in doc
        assert "received_at" not in doc

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_converts_received_at_to_timestamp(self, mock_get_client):
        """Testa conversão de data para timestamp Unix."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário"
        hymn.hymn_book.slug = "hinario"
        hymn.hymn_book.owner_name = "Dono"
        hymn.number = 1
        hymn.title = "Título"
        hymn.text = "Texto"
        hymn.style = ""
        test_date = date(2023, 6, 15)
        hymn.received_at = test_date

        index_hymn(hymn)

        doc = mock_client.collections["hymns"].documents.upsert.call_args[0][0]
        expected_timestamp = int(time.mktime(test_date.timetuple()))
        assert doc["received_at"] == expected_timestamp

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_serializes_uuid_to_string(self, mock_get_client):
        """Testa que UUIDs são convertidos para string."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn_id = uuid4()
        book_id = uuid4()

        hymn = Mock()
        hymn.id = hymn_id
        hymn.hymn_book.id = book_id
        hymn.hymn_book.name = "Hinário"
        hymn.hymn_book.slug = "hinario"
        hymn.hymn_book.owner_name = "Dono"
        hymn.number = 1
        hymn.title = "Título"
        hymn.text = "Texto"
        hymn.style = ""
        hymn.received_at = None

        index_hymn(hymn)

        doc = mock_client.collections["hymns"].documents.upsert.call_args[0][0]
        assert doc["id"] == str(hymn_id)
        assert doc["hymn_book_id"] == str(book_id)
        assert isinstance(doc["id"], str)
        assert isinstance(doc["hymn_book_id"], str)

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_handles_special_characters_in_text(self, mock_get_client):
        """Testa indexação de texto com caracteres especiais."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário Especial"
        hymn.hymn_book.slug = "hinario-especial"
        hymn.hymn_book.owner_name = "José & Maria"
        hymn.number = 1
        hymn.title = "Cântico de Ação de Graças"
        hymn.text = "Letra com acentuação: á é í ó ú ã õ ç\nE caracteres especiais: !@#$%"
        hymn.style = "Valsa"
        hymn.received_at = None

        index_hymn(hymn)

        doc = mock_client.collections["hymns"].documents.upsert.call_args[0][0]
        assert "á é í ó ú" in doc["text"]
        assert "!@#$%" in doc["text"]
        assert "&" in doc["owner_name"]

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_upsert_idempotency(self, mock_get_client):
        """Testa que upsert é usado (permite re-indexação)."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário"
        hymn.hymn_book.slug = "hinario"
        hymn.hymn_book.owner_name = "Dono"
        hymn.number = 1
        hymn.title = "Título"
        hymn.text = "Texto"
        hymn.style = ""
        hymn.received_at = None

        # Indexa duas vezes
        index_hymn(hymn)
        index_hymn(hymn)

        # Verifica que upsert foi chamado duas vezes
        upsert_calls = mock_client.collections["hymns"].documents.upsert.call_count
        assert upsert_calls == 2

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_handles_indexing_error(self, mock_get_client):
        """Testa que erros de indexação são propagados."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula erro no upsert
        mock_client.collections["hymns"].documents.upsert.side_effect = Exception("TypeSense error")

        hymn = Mock()
        hymn.id = uuid4()
        hymn.hymn_book.id = uuid4()
        hymn.hymn_book.name = "Hinário"
        hymn.hymn_book.slug = "hinario"
        hymn.hymn_book.owner_name = "Dono"
        hymn.number = 1
        hymn.title = "Título"
        hymn.text = "Texto"
        hymn.style = ""
        hymn.received_at = None

        # Deve propagar a exceção
        with pytest.raises(Exception, match="TypeSense error"):
            index_hymn(hymn)


class TestDeleteHymn:
    """Testa a função delete_hymn()."""

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_deletes_existing_hymn(self, mock_get_client):
        """Testa deleção de hino existente."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        hymn_id = uuid4()
        delete_hymn(hymn_id)

        # Verifica que tentou deletar o documento correto
        mock_client.collections["hymns"].documents[str(hymn_id)].delete.assert_called_once()

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_handles_non_existent_hymn(self, mock_get_client):
        """Testa que não levanta exceção se hino não existe."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula que o documento não existe
        mock_client.collections["hymns"].documents[Mock()].delete.side_effect = Exception("Not found")

        hymn_id = uuid4()

        # Não deve levantar exceção
        delete_hymn(hymn_id)

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_silently_fails_on_error(self, mock_get_client):
        """Testa que falhas de deleção são silenciosas."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Simula diversos tipos de erro
        mock_client.collections["hymns"].documents[Mock()].delete.side_effect = Exception("Connection timeout")

        hymn_id = uuid4()

        # Não deve levantar exceção
        delete_hymn(hymn_id)


class TestSearchHymns:
    """Testa a função search_hymns()."""

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_searches_with_simple_query(self, mock_get_client):
        """Testa busca com query simples."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_results = {"found": 5, "hits": []}
        mock_client.collections["hymns"].documents.search.return_value = mock_results

        results = search_hymns("alegria")

        # Verifica chamada de search
        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["q"] == "alegria"
        assert results == mock_results

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_searches_multiple_fields(self, mock_get_client):
        """Testa que busca em múltiplos campos."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("test")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        query_by = search_call["query_by"]
        assert "title" in query_by
        assert "text" in query_by
        assert "hymn_book_name" in query_by
        assert "owner_name" in query_by

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_with_pagination(self, mock_get_client):
        """Testa busca com paginação customizada."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("test", per_page=10, page=3)

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["per_page"] == 10
        assert search_call["page"] == 3

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_default_per_page_20(self, mock_get_client):
        """Testa que o padrão é 20 resultados por página."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("test")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["per_page"] == 20
        assert search_call["page"] == 1

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_with_filters(self, mock_get_client):
        """Testa busca com filtros."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("test", filters="hymn_book_name:O Cruzeiro")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["filter_by"] == "hymn_book_name:O Cruzeiro"

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_empty_query(self, mock_get_client):
        """Testa busca com query vazia."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["q"] == ""

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_special_characters(self, mock_get_client):
        """Testa busca com caracteres especiais."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("ação & graça!")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["q"] == "ação & graça!"

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_unicode_characters(self, mock_get_client):
        """Testa busca com caracteres Unicode."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.collections["hymns"].documents.search.return_value = {"found": 0}

        search_hymns("canção coração")

        search_call = mock_client.collections["hymns"].documents.search.call_args[0][0]
        assert search_call["q"] == "canção coração"

    @patch("apps.search.typesense_client.get_typesense_client")
    def test_search_returns_raw_response(self, mock_get_client):
        """Testa que retorna a resposta crua do TypeSense."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        expected_response = {
            "found": 3,
            "hits": [
                {"document": {"id": "1", "title": "Test"}},
                {"document": {"id": "2", "title": "Another"}},
            ],
            "page": 1,
        }
        mock_client.collections["hymns"].documents.search.return_value = expected_response

        results = search_hymns("test")

        assert results == expected_response
        assert results["found"] == 3
        assert len(results["hits"]) == 2


class TestReindexAllHymns:
    """Testa a função reindex_all_hymns()."""

    @patch("apps.hymns.models.Hymn")
    @patch("apps.search.typesense_client.index_hymn")
    @patch("apps.search.typesense_client.create_hymns_collection")
    def test_reindexes_all_hymns(self, mock_create_collection, mock_index_hymn, mock_hymn_model):
        """Testa re-indexação de todos os hinos."""
        # Cria 3 hinos mock
        hymn1 = Mock()
        hymn2 = Mock()
        hymn3 = Mock()

        mock_queryset = MagicMock()
        mock_queryset.__iter__ = Mock(return_value=iter([hymn1, hymn2, hymn3]))
        mock_hymn_model.objects.select_related.return_value.all.return_value = mock_queryset

        count = reindex_all_hymns()

        # Verifica que recriou a collection
        mock_create_collection.assert_called_once()

        # Verifica que indexou todos os hinos
        assert mock_index_hymn.call_count == 3
        mock_index_hymn.assert_any_call(hymn1)
        mock_index_hymn.assert_any_call(hymn2)
        mock_index_hymn.assert_any_call(hymn3)

        assert count == 3

    @patch("apps.hymns.models.Hymn")
    @patch("apps.search.typesense_client.index_hymn")
    @patch("apps.search.typesense_client.create_hymns_collection")
    def test_reindex_empty_table(self, mock_create_collection, mock_index_hymn, mock_hymn_model):
        """Testa re-indexação quando não há hinos."""
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = Mock(return_value=iter([]))
        mock_hymn_model.objects.select_related.return_value.all.return_value = mock_queryset

        count = reindex_all_hymns()

        # Verifica que recriou a collection mesmo sem hinos
        mock_create_collection.assert_called_once()

        # Verifica que não indexou nenhum hino
        mock_index_hymn.assert_not_called()

        assert count == 0

    @patch("apps.hymns.models.Hymn")
    @patch("apps.search.typesense_client.index_hymn")
    @patch("apps.search.typesense_client.create_hymns_collection")
    def test_reindex_returns_count(self, mock_create_collection, mock_index_hymn, mock_hymn_model):
        """Testa que retorna o número de hinos indexados."""
        hymns = [Mock() for _ in range(42)]
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = Mock(return_value=iter(hymns))
        mock_hymn_model.objects.select_related.return_value.all.return_value = mock_queryset

        count = reindex_all_hymns()

        assert count == 42
        assert mock_index_hymn.call_count == 42

    @patch("apps.hymns.models.Hymn")
    @patch("apps.search.typesense_client.index_hymn")
    @patch("apps.search.typesense_client.create_hymns_collection")
    def test_reindex_uses_select_related(self, mock_create_collection, mock_index_hymn, mock_hymn_model):
        """Testa que usa select_related para otimizar queries."""
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = Mock(return_value=iter([]))
        mock_hymn_model.objects.select_related.return_value.all.return_value = mock_queryset

        reindex_all_hymns()

        # Verifica que usou select_related("hymn_book")
        mock_hymn_model.objects.select_related.assert_called_once_with("hymn_book")

    @patch("apps.hymns.models.Hymn")
    @patch("apps.search.typesense_client.index_hymn")
    @patch("apps.search.typesense_client.create_hymns_collection")
    def test_reindex_recreates_collection(self, mock_create_collection, mock_index_hymn, mock_hymn_model):
        """Testa que recria a collection antes de indexar."""
        hymns = [Mock(), Mock()]
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = Mock(return_value=iter(hymns))
        mock_hymn_model.objects.select_related.return_value.all.return_value = mock_queryset

        reindex_all_hymns()

        # Verifica que create_collection foi chamada antes de index_hymn
        mock_create_collection.assert_called_once()
        assert mock_create_collection.call_count == 1
        assert mock_index_hymn.call_count == 2
