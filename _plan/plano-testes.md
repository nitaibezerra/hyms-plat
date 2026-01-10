# Plano de Testes Abrangente - hyms-plat

**Projeto:** Portal de Hinários
**Data:** 2026-01-06
**Objetivo:** Criar cobertura de testes de 80%+ para toda funcionalidade implementada

---

## 1. Executive Summary

### Estado Atual
- **Testes existentes:** 19 (5 smoke tests + 14 model tests)
- **Cobertura estimada:** ~20-30%
- **Linhas de código sem testes:** ~400+ linhas
- **Componentes sem testes:** Views (5), Admin (2), Commands (2), TypeSense (6 funções)

### Objetivo do Plano
Criar **100+ testes unitários** para cobrir:
- ✅ Modelos (já 70% coberto, completar)
- ⚠️ Views (0% coberto)
- ⚠️ TypeSense Integration (0% coberto)
- ⚠️ Management Commands (0% coberto)
- ⚠️ Admin (0% coberto)
- ⚠️ URL Routing (0% coberto)

### Estratégia Definida
- **Prioridade:** Testes unitários primeiro
- **TypeSense:** Usar mocks (unittest.mock)
- **Escopo:** Plano detalhado + Implementação completa
- **Foco:** Testes funcionais apenas (sem performance)

---

## 2. Resumo de Testes

| Componente | Testes Existentes | Testes Novos | Total | Linhas de Teste |
|------------|-------------------|--------------|-------|-----------------|
| Smoke Tests | 5 | 0 | 5 | 56 |
| Modelos | 21 | 21 | 42 | 300 |
| Views | 0 | 50 | 50 | 500 |
| TypeSense | 0 | 32 | 32 | 350 |
| Commands | 0 | 25 | 25 | 310 |
| Admin | 0 | 16 | 16 | 150 |
| URLs | 0 | 6 | 6 | 60 |
| Integration | 0 | 10 | 10 | 200 |
| **TOTAL** | **26** | **160** | **186** | **~1.926 linhas** |

---

## 3. Fases de Implementação

### Fase 1: Setup e Modelos (Prioridade: Alta)
**Meta:** Completar cobertura de modelos e configurar coverage

**Tarefas:**
1. Atualizar `pyproject.toml` com configuração de coverage
2. Expandir `tests/conftest.py` com fixtures
3. Criar fixtures YAML em `tests/fixtures/`
4. Adicionar 21 testes em `test_hymn_models.py`
5. Rodar coverage e validar >= 90% em models.py

**Arquivos:**
- `pyproject.toml`
- `tests/conftest.py`
- `tests/unit/test_hymn_models.py`
- `tests/fixtures/test_hymnbook.yaml` (novo)
- `tests/fixtures/test_hymnbook_invalid.yaml` (novo)
- `tests/fixtures/test_hymnbook_duplicates.yaml` (novo)

**Meta de cobertura:** Models >= 90%

---

### Fase 2: TypeSense Client (Prioridade: Alta)
**Meta:** Cobertura completa do cliente TypeSense

**Tarefas:**
1. Criar `tests/unit/test_typesense_client.py`
2. Implementar 32 testes do TypeSense
3. Configurar mocks para TypeSense Client
4. Testar edge cases (erros, timeouts, dados inválidos)
5. Validar coverage >= 85%

**Arquivos:**
- `tests/unit/test_typesense_client.py` (novo, ~350 linhas)

**Meta de cobertura:** TypeSense client >= 85%

---

### Fase 3: Views (Prioridade: Alta)
**Meta:** Cobertura completa das views

**Tarefas:**
1. Criar `tests/unit/test_hymn_views.py`
2. Implementar 50 testes de views
3. Mockar TypeSense nas views de busca
4. Testar paginação, ordenação, 404s
5. Testar fallback de busca
6. Validar coverage >= 85%

**Arquivos:**
- `tests/unit/test_hymn_views.py` (novo, ~500 linhas)

**Meta de cobertura:** Views >= 85%

---

### Fase 4: Management Commands (Prioridade: Média)
**Meta:** Cobertura dos comandos de management

**Tarefas:**
1. Criar `tests/unit/test_import_yaml_command.py`
2. Criar `tests/unit/test_reindex_command.py`
3. Implementar 20 testes de import_yaml
4. Implementar 5 testes de reindex_typesense
5. Testar YAML válido/inválido
6. Testar dry-run e update mode
7. Validar coverage >= 80%

**Arquivos:**
- `tests/unit/test_import_yaml_command.py` (novo, ~250 linhas)
- `tests/unit/test_reindex_command.py` (novo, ~60 linhas)

**Meta de cobertura:** Commands >= 80%

---

### Fase 5: Admin e URLs (Prioridade: Baixa)
**Meta:** Cobertura de admin e URLs

**Tarefas:**
1. Criar `tests/unit/test_hymn_admin.py`
2. Criar `tests/unit/test_hymn_urls.py`
3. Implementar 16 testes de admin
4. Implementar 6 testes de URLs
5. Validar coverage >= 70% (admin é difícil)

**Arquivos:**
- `tests/unit/test_hymn_admin.py` (novo, ~150 linhas)
- `tests/unit/test_hymn_urls.py` (novo, ~60 linhas)

**Meta de cobertura:** Admin >= 70%, URLs >= 90%

---

## 4. Critérios de Sucesso

### Cobertura Mínima por Componente

| Componente | Meta de Coverage |
|------------|------------------|
| `apps/hymns/models.py` | >= 90% |
| `apps/hymns/views.py` | >= 85% |
| `apps/hymns/admin.py` | >= 70% |
| `apps/hymns/urls.py` | >= 90% |
| `apps/hymns/management/` | >= 80% |
| `apps/search/typesense_client.py` | >= 85% |
| `apps/search/management/` | >= 80% |
| **Total do projeto** | **>= 80%** |

### Validação Final

```bash
# Rodar todos os testes
pytest

# Gerar relatório de coverage
pytest --cov=apps --cov-report=html --cov-report=term-missing

# Verificar se >= 80%
pytest --cov=apps --cov-fail-under=80

# Ver relatório HTML
open htmlcov/index.html
```

### Checklist de Conclusão

- [ ] Todos os 186 testes passando
- [ ] Coverage total >= 80%
- [ ] Coverage de cada componente >= meta individual
- [ ] Relatório HTML gerado
- [ ] Sem warnings de pytest
- [ ] Testes rodam em < 30 segundos
- [ ] Documentação de testes atualizada em `_plan/status-execucao.md`

---

## 5. Comandos Úteis

### Desenvolvimento

```bash
# Rodar todos os testes
pytest

# Rodar testes de um arquivo
pytest tests/unit/test_hymn_views.py

# Rodar teste específico
pytest tests/unit/test_hymn_views.py::TestSearchView::test_search_view_valid_query_typesense

# Rodar com verbose
pytest -v

# Rodar com print output
pytest -s

# Rodar testes que falharam na última execução
pytest --lf
```

### Coverage

```bash
# Coverage de tudo
pytest --cov=apps

# Coverage de módulo específico
pytest --cov=apps.hymns.views tests/unit/test_hymn_views.py

# Coverage com HTML
pytest --cov=apps --cov-report=html

# Coverage com linhas faltantes
pytest --cov=apps --cov-report=term-missing

# Falha se < 80%
pytest --cov=apps --cov-fail-under=80
```

### Debug

```bash
# Parar no primeiro erro
pytest -x

# Mostrar locals no traceback
pytest -l

# Entrar no debugger no erro
pytest --pdb

# Mostrar 10 testes mais lentos
pytest --durations=10
```

---

**FIM DO PLANO**

Este plano detalha **186 testes** totalizando **~1.926 linhas de código de teste** para atingir **>= 80% de cobertura** em todo o projeto hyms-plat.

Para detalhes completos de cada teste, consulte o documento completo em `/Users/nitai/.claude/plans/woolly-wibbling-wren.md`
