# Status de Execução: Testes E2E com Playwright

**Projeto:** Portal de Hinários do Santo Daime (hyms-plat)
**Iniciado em:** 2026-01-11
**Última atualização:** 2026-01-11
**Status:** COMPLETO

---

## Resumo Executivo

Implementação de suite de testes E2E com Playwright para validar fluxos de usuário e prevenir regressões.

**Motivação:** Bug encontrado no upload de YAML que não foi detectado por testes unitários.

**Resultado:** 15 testes E2E implementados e passando. 291 testes unitários continuam passando.

---

## Checklist de Execução

### Parte 1: Correção do Bug (Pré-requisito)
- [x] Corrigir `apps/users/views.py` - aceitar YAML sem `hymn_book:` como raiz
- [x] Adicionar validação defensiva em `apps/hymns/disambiguation.py`
- [x] Testar correção manualmente

### Parte 2: Configuração Playwright
- [x] Criar `tests/e2e/__init__.py`
- [x] Criar `tests/e2e/conftest.py` com fixtures
- [x] Atualizar `pytest.ini` com marker e2e
- [x] Instalar browsers do Playwright (`playwright install chromium`)

### Parte 3: Testes de Navegação
- [x] Criar `tests/e2e/test_navigation.py`
- [x] Implementar `test_home_page_loads`
- [x] Implementar `test_hymnbook_list_shows_hymnbooks`
- [x] Implementar `test_hymnbook_detail_shows_hymns`
- [x] Implementar `test_hymn_detail_shows_lyrics`
- [x] Implementar `test_search_page_loads`

### Parte 4: Testes de Autenticação
- [x] Criar `tests/e2e/test_auth.py`
- [x] Implementar `test_signup_page_loads`
- [x] Implementar `test_login_page_loads`
- [x] Implementar `test_login_with_invalid_credentials_shows_error`
- [x] Implementar `test_protected_page_redirects_to_login`

### Parte 5: Testes de Upload
- [x] Criar `tests/e2e/test_upload.py`
- [x] Implementar `test_upload_page_requires_authentication`
- [x] Implementar `test_upload_page_loads_when_authenticated`
- [x] Implementar `test_upload_invalid_yaml_shows_error`

### Parte 6: Testes de Features Sociais
- [x] Criar `tests/e2e/test_social.py`
- [x] Implementar `test_hymn_detail_shows_social_buttons_when_authenticated`
- [x] Implementar `test_notifications_page_loads`
- [x] Implementar `test_profile_page_loads`

### Parte 7: Validação Final
- [x] Rodar todos os testes E2E (15 passed)
- [x] Verificar que testes unitários ainda passam (291 passed)
- [x] Documentar como executar testes

---

## Progresso Detalhado

### Sessão 1: 2026-01-11

**Status:** COMPLETO

**Contexto:**
- Fase 3 (Áudio & Social) foi completada
- 291 testes unitários passando (83.91% coverage)
- Bug encontrado no upload de YAML (erro: 'NoneType' object has no attribute 'lower')

**Ações realizadas:**
1. Investigação do bug - Root cause identificado:
   - Código espera `hymn_book:` como chave raiz no YAML
   - Arquivo do usuário tem campos diretamente na raiz
   - `name=None` é passado para `disambiguation.py` sem validação

2. Plano criado e salvo em `_plan/E2E_TESTS/PLANO.md`

3. Bug corrigido em `apps/users/views.py`:
   - Aceita ambos formatos YAML (com ou sem `hymn_book:` como raiz)
   - Valida que `name` é obrigatório

4. Validação defensiva adicionada em `apps/hymns/disambiguation.py`:
   - `calculate_string_similarity()` retorna 0.0 se alguma string for None
   - `normalize_hymnbook_name()` retorna "" se nome for None

5. Suite E2E completa implementada:
   - 5 testes de navegação pública
   - 4 testes de autenticação
   - 3 testes de upload
   - 3 testes de features sociais

---

## Arquivos Criados/Modificados

| Arquivo | Status | Descrição |
|---------|--------|-----------|
| `apps/users/views.py` | COMPLETO | Bug corrigido - aceita ambos formatos YAML |
| `apps/hymns/disambiguation.py` | COMPLETO | Validação defensiva para None |
| `tests/e2e/__init__.py` | COMPLETO | Init do módulo |
| `tests/e2e/conftest.py` | COMPLETO | Fixtures E2E (browser, page, authenticated_page) |
| `tests/e2e/test_navigation.py` | COMPLETO | 5 testes de navegação |
| `tests/e2e/test_auth.py` | COMPLETO | 4 testes de autenticação |
| `tests/e2e/test_upload.py` | COMPLETO | 3 testes de upload |
| `tests/e2e/test_social.py` | COMPLETO | 3 testes sociais |
| `pytest.ini` | COMPLETO | Marker e2e adicionado |

---

## Comandos Úteis

```bash
# Servidor Django (porta 9000 para evitar conflitos)
poetry run python manage.py runserver 9000

# Rodar testes E2E
poetry run pytest tests/e2e/ -v

# Rodar testes E2E com browser visível
poetry run pytest tests/e2e/ -v --headed

# Rodar teste específico
poetry run pytest tests/e2e/test_upload.py::TestHymnbookUpload::test_upload_invalid_yaml_shows_error -v

# Instalar browsers do Playwright
poetry run playwright install chromium

# Rodar todos os testes (unit + E2E)
poetry run pytest tests/ -v
```

---

## Pré-requisitos para Rodar Testes E2E

1. **Servidor Django rodando:**
   ```bash
   poetry run python manage.py runserver 9000
   ```

2. **Usuário de teste criado no banco:**
   ```bash
   poetry run python manage.py shell -c "
   from apps.users.models import User
   if not User.objects.filter(email='teste2e@example.com').exists():
       User.objects.create_user('teste2e', 'teste2e@example.com', 'testpass123')
   "
   ```

3. **Browsers do Playwright instalados:**
   ```bash
   poetry run playwright install chromium
   ```

---

## Contexto do Projeto

- **Fases 1-3 completas:** MVP, Upload, Social
- **291 testes unitários** passando
- **15 testes E2E** passando
- **Playwright v1.49** instalado via Poetry
- **Servidor roda na porta 9000** (8000, 8001, 8002 ocupadas)

---

## Referências

- Plano completo: `_plan/E2E_TESTS/PLANO.md`
- Fixture YAML válido: `tests/fixtures/test_hymnbook.yaml`
- Arquivo que causou erro original: `/Users/nitai/Dropbox/dev-mgi/tmp/hinario_rainha.yaml`
