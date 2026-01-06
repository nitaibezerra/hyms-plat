# Portal de Hinários - Plano de Implementação

## Visão Geral do Projeto

**Objetivo:** Criar um portal para pesquisa e acesso a hinários do Santo Daime
**Stack:** Django 5.x + Wagtail 6.x + TypeSense + PostgreSQL
**Abordagem:** Desenvolvimento incremental em fases com MVP funcional

---

## Fase 0: Setup e Infraestrutura Base

### 0.1 Configuração do Projeto
- [ ] Criar repositório Git
- [ ] Configurar projeto Django com Poetry
- [ ] Configurar Wagtail CMS
- [ ] Configurar PostgreSQL (local via Docker)
- [ ] Configurar TypeSense (local via Docker)
- [ ] Configurar pre-commit hooks (black, isort, flake8)
- [ ] Criar docker-compose.yml para ambiente de desenvolvimento

### 0.2 Estrutura do Projeto
```
hyms-plat/
├── docker-compose.yml
├── pyproject.toml
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/              # Configurações base, mixins
│   ├── hymns/             # Models de hinários e hinos
│   ├── search/            # Integração TypeSense
│   ├── users/             # Autenticação e perfis
│   └── cms/               # Páginas Wagtail
├── templates/
├── static/
├── media/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

### 0.3 CI/CD Base
- [ ] Configurar GitHub Actions
- [ ] Pipeline: lint → test → build
- [ ] Configurar pytest com coverage mínimo de 80%

### 0.4 Testes da Fase 0
- [ ] Teste de smoke: aplicação inicia corretamente
- [ ] Teste de conexão com PostgreSQL
- [ ] Teste de conexão com TypeSense

**Critério de Conclusão:** Aplicação Django/Wagtail rodando localmente com Docker

---

## Fase 1: MVP Leitura (Core Read-Only)

### 1.1 Models Base

#### 1.1.1 HymnBook (Hinário)
```python
class HymnBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    intro_name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    owner_name = models.CharField(max_length=255)  # Texto livre
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
```

#### 1.1.2 Hymn (Hino)
```python
class Hymn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hymn_book = models.ForeignKey(HymnBook, on_delete=models.CASCADE, related_name='hymns')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, db_index=True)
    text = models.TextField()
    received_at = models.DateField(null=True, blank=True)
    offered_to = models.CharField(max_length=255, blank=True)
    style = models.CharField(max_length=50, blank=True)  # Valsa, Marcha, etc.
    extra_instructions = models.TextField(blank=True)
    repetitions = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['hymn_book', 'number']
        unique_together = ['hymn_book', 'number']
```

### 1.2 Import de Dados YAML
- [ ] Criar management command `import_yaml`
- [ ] Parser para formato YAML do hymn_pdf_generator
- [ ] Validação de dados obrigatórios
- [ ] Importar hinários de exemplo para testes

### 1.3 Integração TypeSense
- [ ] Configurar cliente TypeSense
- [ ] Criar schema de coleção para hinos
- [ ] Indexar todos os hinos (título + texto)
- [ ] Criar signal para reindexar ao salvar hino
- [ ] Implementar busca full-text

**Schema TypeSense:**
```json
{
  "name": "hymns",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "hymn_book_id", "type": "string"},
    {"name": "hymn_book_name", "type": "string", "facet": true},
    {"name": "owner_name", "type": "string", "facet": true},
    {"name": "number", "type": "int32"},
    {"name": "title", "type": "string"},
    {"name": "text", "type": "string"},
    {"name": "style", "type": "string", "facet": true, "optional": true}
  ],
  "default_sorting_field": "number"
}
```

### 1.4 Views e Templates

#### 1.4.1 Páginas
- [ ] **Home**: Barra de busca + hinários em destaque
- [ ] **Lista de Hinários**: Grid/lista de todos os hinários
- [ ] **Detalhe do Hinário**: Info + lista de hinos
- [ ] **Detalhe do Hino**: Texto completo + metadados
- [ ] **Resultados de Busca**: Lista com snippets

#### 1.4.2 Componentes
- [ ] Barra de busca com autocomplete (TypeSense)
- [ ] Menu lateral com hinários (estilo santodaime.org)
- [ ] Breadcrumbs de navegação
- [ ] Paginação

### 1.5 Wagtail CMS
- [ ] Configurar HomePage
- [ ] Configurar páginas estáticas (Sobre, Contato)
- [ ] Configurar Snippets para hinários em destaque

### 1.6 Download de PDF
- [ ] Gerar PDF de hinário on-demand (usando WeasyPrint ou similar)
- [ ] Cache de PDFs gerados
- [ ] Botão de download em cada hinário

### 1.7 Testes da Fase 1
- [ ] **Unit Tests:**
  - Models: validações, métodos
  - Import YAML: parsing, validações
  - TypeSense: indexação, busca
- [ ] **Integration Tests:**
  - API de busca
  - Views (status codes, contexto)
- [ ] **E2E Tests (Playwright):**
  - Navegação home → hinário → hino
  - Busca e resultados
  - Download de PDF

**Critério de Conclusão:**
- Usuário pode navegar e buscar hinários
- Download de PDF funciona
- Cobertura de testes ≥ 80%

---

## Fase 2: Sistema de Upload e Usuários

### 2.1 Autenticação
- [ ] Configurar django-allauth
- [ ] Login com email/senha
- [ ] Login social (Google) - opcional
- [ ] Páginas de registro, login, recuperação de senha
- [ ] Perfil do usuário básico

### 2.2 Model de Versões
```python
class HymnBookVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hymn_book = models.ForeignKey(HymnBook, on_delete=models.CASCADE, related_name='versions')
    version_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    yaml_file = models.FileField(upload_to='yaml/', blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
```

### 2.3 Sistema de Desambiguação

#### 2.3.1 Fluxo de Upload
```
1. Usuário inicia upload
2. Insere nome do hinário
3. Sistema busca no TypeSense por:
   a. Nome exato (match direto)
   b. Nomes similares (fuzzy search)
   c. Textos similares (se YAML fornecido)
4. Exibe sugestões:
   - "Este hinário já existe. Adicionar como nova versão?"
   - "Hinários similares encontrados: [lista]"
   - "Criar novo hinário"
5. Usuário confirma escolha
6. Upload processado
```

#### 2.3.2 Algoritmo de Similaridade
- [ ] Busca fuzzy por nome (TypeSense typo tolerance)
- [ ] Se YAML: comparar primeiros 3-5 hinos
- [ ] Score de similaridade (Levenshtein ou embeddings)
- [ ] Threshold configurável para sugestões

### 2.4 Upload de Hinários
- [ ] Formulário de upload (PDF e/ou YAML)
- [ ] Preview antes de confirmar
- [ ] Processamento assíncrono (Celery) para arquivos grandes
- [ ] Extração de texto de PDF (OCR se necessário)

### 2.5 Perfil de Dono de Hinário
- [ ] Vincular HymnBook.owner_user a User
- [ ] Página pública do perfil com lista de hinários
- [ ] Edição do perfil pelo usuário

### 2.6 Testes da Fase 2
- [ ] **Unit Tests:**
  - Autenticação (registro, login)
  - Desambiguação (algoritmo de similaridade)
  - Upload (validações, processamento)
- [ ] **Integration Tests:**
  - Fluxo completo de upload
  - Vinculação de versões
- [ ] **E2E Tests:**
  - Registro → login → upload → visualização
  - Fluxo de desambiguação

**Critério de Conclusão:**
- Sistema de autenticação funcional
- Upload com desambiguação funcionando
- Múltiplas versões de hinário
- Cobertura de testes ≥ 80%

---

## Fase 3: Áudio e Social

### 3.1 Model de Áudio
```python
class HymnAudio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hymn = models.ForeignKey(Hymn, on_delete=models.CASCADE, related_name='audios')
    hymn_book_version = models.ForeignKey(HymnBookVersion, on_delete=models.SET_NULL, null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/')
    duration = models.DurationField(null=True)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3.2 Upload e Player de Áudio
- [ ] Upload de arquivos de áudio (MP3, M4A, WAV)
- [ ] Conversão para formato web (MP3)
- [ ] Player de áudio integrado na página do hino
- [ ] Vinculação com versão específica do hinário

### 3.3 Sistema de Seguir
```python
class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'followed']
```

### 3.4 Notificações
- [ ] Model de Notification
- [ ] Notificação ao seguir
- [ ] Notificação de novo hino/áudio
- [ ] Centro de notificações na UI
- [ ] Opção de email (opcional)

### 3.5 Testes da Fase 3
- [ ] **Unit Tests:**
  - Upload de áudio
  - Sistema de seguir
  - Notificações
- [ ] **Integration Tests:**
  - Fluxo de upload de áudio
  - Geração de notificações
- [ ] **E2E Tests:**
  - Player de áudio
  - Seguir usuário e receber notificação

**Critério de Conclusão:**
- Upload e reprodução de áudio
- Sistema de seguir funcional
- Notificações in-app
- Cobertura de testes ≥ 80%

---

## Fase 4: Refinamentos e Deploy

### 4.1 Multi-idioma
- [ ] Configurar django i18n
- [ ] Tradução da interface (PT, EN, ES)
- [ ] Seletor de idioma

### 4.2 SEO e Performance
- [ ] Meta tags dinâmicas
- [ ] Sitemap XML
- [ ] robots.txt
- [ ] Cache de páginas (Redis)
- [ ] Otimização de queries (select_related, prefetch_related)
- [ ] Lazy loading de imagens

### 4.3 PWA (Progressive Web App)
- [ ] Service Worker para cache offline
- [ ] Manifest.json
- [ ] Instalação em dispositivos móveis

### 4.4 Deploy
- [ ] Configurar ambiente de produção
- [ ] Docker para produção
- [ ] Configurar storage (GCS/S3) para mídia
- [ ] Configurar CDN
- [ ] SSL/HTTPS
- [ ] Monitoramento (Sentry)

### 4.5 Documentação
- [ ] README completo
- [ ] Documentação de API
- [ ] Guia de contribuição

**Critério de Conclusão:**
- Aplicação em produção
- Performance otimizada
- Documentação completa

---

## Fase Futura: Moderação e Melhorias

### Moderação
- [ ] Flags de conteúdo
- [ ] Fila de moderação
- [ ] Roles de moderador
- [ ] Histórico de ações

### Melhorias
- [ ] Comentários em hinos
- [ ] Ratings/favoritos
- [ ] Playlists de hinos
- [ ] API REST pública
- [ ] App mobile nativo

---

## Cronograma Sugerido

| Fase | Descrição | Dependências |
|------|-----------|--------------|
| 0 | Setup e Infraestrutura | - |
| 1 | MVP Leitura | Fase 0 |
| 2 | Upload e Usuários | Fase 1 |
| 3 | Áudio e Social | Fase 2 |
| 4 | Refinamentos e Deploy | Fase 3 |

---

## Métricas de Qualidade

### Cobertura de Testes
- **Mínimo:** 80% de cobertura
- **Ideal:** 90%+ para código crítico

### Tipos de Teste por Fase
| Fase | Unit | Integration | E2E |
|------|------|-------------|-----|
| 0 | 5+ | 3+ | 1 |
| 1 | 20+ | 10+ | 5+ |
| 2 | 15+ | 8+ | 3+ |
| 3 | 10+ | 5+ | 3+ |
| 4 | 5+ | 3+ | 2+ |

### Ferramentas de Teste
- **pytest** + pytest-django
- **factory_boy** para fixtures
- **Playwright** para E2E
- **coverage.py** para métricas

---

## Dependências Python (pyproject.toml)

```toml
[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
wagtail = "^6.0"
psycopg2-binary = "^2.9"
typesense = "^0.21"
django-allauth = "^0.61"
celery = "^5.3"
redis = "^5.0"
weasyprint = "^61"
pillow = "^10.2"
python-magic = "^0.4"
pyyaml = "^6.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-django = "^4.7"
pytest-cov = "^4.1"
factory-boy = "^3.3"
playwright = "^1.41"
black = "^24.1"
isort = "^5.13"
flake8 = "^7.0"
pre-commit = "^3.6"
```
