# Plano: Testes E2E com Playwright - hyms-plat

**Projeto:** Portal de Hinários do Santo Daime
**Data:** 2026-01-11
**Objetivo:** Implementar suite de testes E2E com Playwright para validar fluxos de usuário

---

## 📋 Contexto

### Problema Encontrado
Ao tentar fazer upload de um hinário YAML, ocorreu o erro:
```
Erro ao processar YAML: 'NoneType' object has no attribute 'lower'
```

**Root Cause:** O código espera estrutura YAML com `hymn_book:` como chave raiz, mas aceita arquivos sem essa estrutura, resultando em `name=None` sendo passado para funções de desambiguação.

### Necessidade
Testes E2E que simulem usuários reais para:
1. Detectar bugs de integração como esse
2. Validar fluxos completos (login → ação → resultado)
3. Garantir que a UI funciona corretamente
4. Prevenir regressões

### Estado Atual
- ✅ **Playwright instalado** (v1.49 no pyproject.toml)
- ✅ **Diretório `tests/e2e/`** existe (vazio)
- ✅ **291 testes unitários** passando (83.91% coverage)
- ❌ **Nenhum teste E2E** implementado
- ❌ **Nenhum `playwright.config.py`** configurado

---

## 🎯 Escopo do Plano

### Fluxos a Testar

1. **Navegação Pública** (sem login)
   - Home page carrega com estatísticas
   - Lista de hinários funciona
   - Detalhes de hinário mostram hinos
   - Detalhes de hino mostram letra
   - Busca retorna resultados

2. **Autenticação**
   - Criar conta (signup)
   - Login com email/senha
   - Logout
   - Acesso a áreas protegidas

3. **Upload de Hinário** (autenticado)
   - Upload de YAML válido
   - Validação de YAML inválido
   - Fluxo de desambiguação
   - Preview e confirmação

4. **Features Sociais** (autenticado)
   - Favoritar/desfavoritar hino
   - Adicionar comentário
   - Seguir/deixar de seguir usuário
   - Ver notificações

---

## 📁 Arquivos a Criar/Modificar

### Novos Arquivos

```
tests/
├── e2e/
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures E2E (browser, page, auth)
│   ├── test_navigation.py             # Testes de navegação pública
│   ├── test_auth.py                   # Testes de autenticação
│   ├── test_upload.py                 # Testes de upload de hinário
│   ├── test_social.py                 # Testes de features sociais
│   └── fixtures/
│       ├── valid_hymnbook.yaml        # YAML válido para upload
│       └── invalid_hymnbook.yaml      # YAML inválido para teste de erro
├── playwright.config.py               # Configuração do Playwright
```

### Arquivos a Modificar

```
pyproject.toml                         # Adicionar scripts de teste E2E
pytest.ini                             # Configurar markers para E2E
apps/users/views.py                    # Corrigir bug do upload (validação None)
apps/hymns/disambiguation.py           # Adicionar validação defensiva
```

---

## 🔧 Implementação

### Parte 1: Correção do Bug (Pré-requisito)

**Arquivo:** `apps/users/views.py` (linhas ~115-120)

```python
# ANTES (bugado)
hymn_book_data = data.get("hymn_book", {})
name = hymn_book_data.get("name")

# DEPOIS (corrigido)
hymn_book_data = data.get("hymn_book") or data  # Aceita ambos formatos
name = hymn_book_data.get("name")
if not name:
    form.add_error("yaml_file", "O arquivo YAML deve conter o campo 'name'.")
    return render(request, "users/upload.html", {"form": form})
```

**Arquivo:** `apps/hymns/disambiguation.py` (funções de validação)

```python
def normalize_hymnbook_name(name: str) -> str:
    if not name:
        return ""
    return " ".join(name.lower().split())

def calculate_string_similarity(str1: str, str2: str) -> float:
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
```

### Parte 2: Configuração Playwright

**Arquivo:** `playwright.config.py`

```python
from playwright.sync_api import Playwright

PLAYWRIGHT_CONFIG = {
    "base_url": "http://localhost:8000",
    "headless": True,
    "slow_mo": 0,
    "viewport": {"width": 1280, "height": 720},
    "screenshot": "only-on-failure",
    "video": "retain-on-failure",
    "trace": "retain-on-failure",
    "timeout": 30000,
}

# Configuração para pytest-playwright
def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
```

**Arquivo:** `pytest.ini` (adicionar)

```ini
[pytest]
markers =
    e2e: mark test as end-to-end (requires running server)
```

### Parte 3: Fixtures E2E

**Arquivo:** `tests/e2e/conftest.py`

```python
import pytest
from playwright.sync_api import sync_playwright, Page, Browser
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture(scope="session")
def browser():
    """Browser instance para toda a sessão de testes."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser: Browser):
    """Nova página para cada teste."""
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    yield page
    page.close()
    context.close()

@pytest.fixture
def base_url():
    """URL base do servidor Django."""
    return "http://localhost:9000"

@pytest.fixture
def test_user(db):
    """Cria usuário de teste."""
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    return user

@pytest.fixture
def authenticated_page(page: Page, base_url: str, test_user):
    """Página com usuário autenticado."""
    page.goto(f"{base_url}/accounts/login/")
    page.fill('input[name="login"]', test_user.email)
    page.fill('input[name="password"]', "testpass123")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{base_url}/**")
    return page
```

### Parte 4: Testes de Navegação

**Arquivo:** `tests/e2e/test_navigation.py`

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.django_db
class TestPublicNavigation:
    """Testes de navegação pública (sem login)."""

    def test_home_page_loads(self, page: Page, base_url: str):
        """Home page carrega com título e estatísticas."""
        page.goto(base_url)

        expect(page).to_have_title("Portal de Hinários do Santo Daime")
        expect(page.locator("h1")).to_contain_text("Portal de Hinários")

        # Verifica estatísticas
        stats = page.locator(".stat-item")
        expect(stats).to_have_count(2)  # Hinários e Hinos

    def test_hymnbook_list_shows_hymnbooks(self, page: Page, base_url: str):
        """Lista de hinários mostra hinários cadastrados."""
        page.goto(f"{base_url}/hinarios/")

        expect(page.locator("h1")).to_contain_text("Hinários")
        # Deve ter pelo menos o hinário de exemplo
        expect(page.locator(".card")).to_have_count_greater_than(0)

    def test_hymnbook_detail_shows_hymns(self, page: Page, base_url: str):
        """Detalhes do hinário mostram lista de hinos."""
        page.goto(f"{base_url}/hinarios/")
        page.click("text=Ver Hinário")

        # Deve mostrar tabela de hinos
        expect(page.locator("table")).to_be_visible()
        expect(page.locator("tr")).to_have_count_greater_than(1)

    def test_hymn_detail_shows_lyrics(self, page: Page, base_url: str):
        """Detalhes do hino mostram letra completa."""
        page.goto(f"{base_url}/hinarios/")
        page.click("text=Ver Hinário")
        page.click("tr >> nth=1")  # Primeiro hino

        # Deve mostrar letra
        expect(page.locator(".hymn-text")).to_be_visible()
        expect(page.locator(".hymn-text")).not_to_be_empty()

    def test_search_returns_results(self, page: Page, base_url: str):
        """Busca retorna resultados para termo válido."""
        page.goto(f"{base_url}/busca/")
        page.fill('input[name="q"]', "lua")
        page.click('button[type="submit"]')

        # Deve ter resultados
        page.wait_for_selector(".card")
        expect(page.locator(".card")).to_have_count_greater_than(0)
```

### Parte 5: Testes de Autenticação

**Arquivo:** `tests/e2e/test_auth.py`

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.django_db
class TestAuthentication:
    """Testes de autenticação de usuários."""

    def test_signup_creates_account(self, page: Page, base_url: str):
        """Criar conta com email/senha funciona."""
        page.goto(f"{base_url}/accounts/signup/")

        page.fill('input[name="email"]', "newuser@example.com")
        page.fill('input[name="username"]', "newuser")
        page.fill('input[name="password1"]', "SecurePass123!")
        page.fill('input[name="password2"]', "SecurePass123!")
        page.click('button[type="submit"]')

        # Deve redirecionar para home ou confirmação
        expect(page).not_to_have_url(f"{base_url}/accounts/signup/")

    def test_login_with_valid_credentials(self, page: Page, base_url: str, test_user):
        """Login com credenciais válidas funciona."""
        page.goto(f"{base_url}/accounts/login/")

        page.fill('input[name="login"]', test_user.email)
        page.fill('input[name="password"]', "testpass123")
        page.click('button[type="submit"]')

        # Deve mostrar menu de usuário logado
        expect(page.locator("text=Perfil")).to_be_visible()
        expect(page.locator("text=Sair")).to_be_visible()

    def test_login_with_invalid_credentials_shows_error(self, page: Page, base_url: str):
        """Login com credenciais inválidas mostra erro."""
        page.goto(f"{base_url}/accounts/login/")

        page.fill('input[name="login"]', "wrong@example.com")
        page.fill('input[name="password"]', "wrongpass")
        page.click('button[type="submit"]')

        # Deve mostrar erro
        expect(page.locator(".errorlist, .alert-danger, .error")).to_be_visible()

    def test_logout_redirects_to_home(self, authenticated_page: Page, base_url: str):
        """Logout redireciona para home."""
        authenticated_page.click("text=Sair")

        # Deve mostrar menu de não-logado
        expect(authenticated_page.locator("text=Entrar")).to_be_visible()
```

### Parte 6: Testes de Upload

**Arquivo:** `tests/e2e/test_upload.py`

```python
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.django_db
class TestHymnbookUpload:
    """Testes de upload de hinários."""

    def test_upload_valid_yaml_succeeds(self, authenticated_page: Page, base_url: str, tmp_path):
        """Upload de YAML válido cria hinário."""
        # Criar arquivo YAML temporário
        yaml_content = """
name: Hinário de Teste E2E
owner_name: Teste Automatizado
intro_name: Teste
description: Hinário criado por teste E2E

hymns:
  - number: 1
    title: Primeiro Hino de Teste
    text: |
      Esta é a letra
      Do primeiro hino de teste
    style: Valsa
"""
        yaml_file = tmp_path / "test_hymnbook.yaml"
        yaml_file.write_text(yaml_content)

        # Navegar para upload
        authenticated_page.goto(f"{base_url}/contribuir/")

        # Upload do arquivo
        authenticated_page.set_input_files('input[type="file"][name="yaml_file"]', str(yaml_file))
        authenticated_page.click('button:has-text("Enviar")')

        # Deve ir para preview ou confirmar
        authenticated_page.wait_for_url(f"{base_url}/**")
        # Não deve ter erro
        expect(authenticated_page.locator(".errorlist, .alert-danger")).not_to_be_visible()

    def test_upload_invalid_yaml_shows_error(self, authenticated_page: Page, base_url: str, tmp_path):
        """Upload de YAML inválido mostra erro amigável."""
        # YAML sem campos obrigatórios
        yaml_content = """
invalid: true
no_name: here
"""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text(yaml_content)

        authenticated_page.goto(f"{base_url}/contribuir/")
        authenticated_page.set_input_files('input[type="file"][name="yaml_file"]', str(yaml_file))
        authenticated_page.click('button:has-text("Enviar")')

        # Deve mostrar erro
        expect(authenticated_page.locator(".errorlist, .alert-danger, .error")).to_be_visible()

    def test_upload_requires_authentication(self, page: Page, base_url: str):
        """Upload sem login redireciona para login."""
        page.goto(f"{base_url}/contribuir/")

        # Deve redirecionar para login
        expect(page).to_have_url_matching(r".*/accounts/login/.*")
```

### Parte 7: Testes de Features Sociais

**Arquivo:** `tests/e2e/test_social.py`

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.django_db
class TestSocialFeatures:
    """Testes de features sociais."""

    def test_favorite_hymn_toggle(self, authenticated_page: Page, base_url: str):
        """Favoritar e desfavoritar hino funciona."""
        # Ir para um hino
        authenticated_page.goto(f"{base_url}/hinarios/")
        authenticated_page.click("text=Ver Hinário")
        authenticated_page.click("tr >> nth=1")

        # Clicar em favoritar
        fav_button = authenticated_page.locator('[data-action="toggle-favorite"]')
        expect(fav_button).to_be_visible()

        initial_text = fav_button.inner_text()
        fav_button.click()

        # Texto deve mudar
        authenticated_page.wait_for_timeout(500)  # Aguarda AJAX
        expect(fav_button).not_to_have_text(initial_text)

    def test_add_comment_to_hymn(self, authenticated_page: Page, base_url: str):
        """Adicionar comentário em hino funciona."""
        # Ir para um hino
        authenticated_page.goto(f"{base_url}/hinarios/")
        authenticated_page.click("text=Ver Hinário")
        authenticated_page.click("tr >> nth=1")

        # Clicar em comentar
        authenticated_page.click("text=Comentar")

        # Preencher formulário
        authenticated_page.fill('textarea[name="text"]', "Este é um comentário de teste E2E!")
        authenticated_page.click('button:has-text("Enviar")')

        # Deve voltar para página do hino com comentário
        expect(authenticated_page.locator("text=comentário de teste E2E")).to_be_visible()

    def test_notifications_page_loads(self, authenticated_page: Page, base_url: str):
        """Página de notificações carrega."""
        authenticated_page.goto(f"{base_url}/notificacoes/")

        expect(authenticated_page.locator("h1")).to_contain_text("Notificações")
```

---

## 🚀 Execução

### Comandos

```bash
# Instalar browsers do Playwright
poetry run playwright install chromium

# Rodar servidor Django (em outro terminal)
poetry run python manage.py runserver 9000

# Rodar todos os testes E2E
poetry run pytest tests/e2e/ -v --headed  # Com browser visível
poetry run pytest tests/e2e/ -v           # Headless (CI)

# Rodar teste específico
poetry run pytest tests/e2e/test_upload.py -v

# Rodar com screenshots de falhas
poetry run pytest tests/e2e/ -v --screenshot=on
```

### Scripts no pyproject.toml

```toml
[tool.poetry.scripts]
test-e2e = "pytest tests/e2e/ -v"
test-e2e-headed = "pytest tests/e2e/ -v --headed"
```

---

## ✅ Verificação

### Checklist de Sucesso

- [ ] Bug de upload corrigido (aceita YAML sem `hymn_book:`)
- [ ] Validação defensiva em `disambiguation.py`
- [ ] `playwright.config.py` criado
- [ ] `tests/e2e/conftest.py` com fixtures
- [ ] `test_navigation.py` - 5 testes passando
- [ ] `test_auth.py` - 4 testes passando
- [ ] `test_upload.py` - 3 testes passando
- [ ] `test_social.py` - 3 testes passando
- [ ] Todos os 15+ testes E2E passando
- [ ] CI configurado para rodar testes E2E

### Como Testar Manualmente

```bash
# 1. Iniciar servidor
poetry run python manage.py runserver 9000

# 2. Em outro terminal, rodar testes
poetry run pytest tests/e2e/ -v --headed

# 3. Verificar screenshots de falhas em:
#    tests/e2e/screenshots/
```

---

## 📊 Estimativa

| Tarefa | Tempo |
|--------|-------|
| Correção do bug de upload | 15 min |
| Configuração Playwright | 15 min |
| Fixtures E2E | 20 min |
| test_navigation.py | 20 min |
| test_auth.py | 20 min |
| test_upload.py | 25 min |
| test_social.py | 20 min |
| Testes e ajustes | 25 min |
| **Total** | **~2.5 horas** |

---

## 🔗 Arquivos Críticos

1. **Bug a corrigir:** [apps/users/views.py](apps/users/views.py) (linhas 115-135)
2. **Validação defensiva:** [apps/hymns/disambiguation.py](apps/hymns/disambiguation.py) (linhas 25-78)
3. **Fixtures existentes:** [tests/conftest.py](tests/conftest.py)
4. **YAML de exemplo:** [tests/fixtures/test_hymnbook.yaml](tests/fixtures/test_hymnbook.yaml)
