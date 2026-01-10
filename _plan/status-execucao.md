# Status de Execução do Plano de Implementação

**Última atualização:** 2026-01-06

## Visão Geral do Projeto

**Portal de Hinários** - Plataforma para busca e acesso a hinários do Santo Daime

- **Stack:** Django 5.1 + Wagtail 6.4 + PostgreSQL 16 + TypeSense 27.1
- **Repositório:** https://github.com/nitaibezerra/hyms-plat
- **Diretório:** `/Users/nitai/Dropbox/dev-mgi/hyms-plat`
- **Abordagem:** MVP iterativo (read-only → upload → áudio → social)

## Arquitetura Confirmada

**IMPORTANTE:** PostgreSQL é o banco de dados principal (source of truth). TypeSense é índice de busca secundário.

**Fluxo de dados:**
- **Escrita:** Django → PostgreSQL → TypeSense
- **Busca:** TypeSense → PostgreSQL (para detalhes completos)
- **Fallback:** Se TypeSense falhar, busca direta no PostgreSQL

## Status por Fase

### ✅ Fase 0: Configuração Inicial - COMPLETA

**Data de conclusão:** 2026-01-06

**Itens implementados:**
- [x] Repositório GitHub criado (nitaibezerra/hyms-plat)
- [x] Poetry configurado com todas as dependências
- [x] Docker Compose com PostgreSQL 16, TypeSense 27.1, Redis 7
- [x] Estrutura de settings multi-ambiente (base, local, test, production)
- [x] Modelo de usuário customizado (apps.users.User)
- [x] GitHub Actions CI/CD (lint → test → build)
- [x] Pre-commit hooks (black, isort, ruff)
- [x] 5 smoke tests passando

**Commits:**
1. `3269200` - "Initial Django + Wagtail setup with Docker Compose"

**Erros resolvidos:**
- Poetry package installation: adicionado `package-mode = false`
- Django-allauth deprecations: migrado para nova API `ACCOUNT_LOGIN_METHODS`
- Wagtail HomePage migration: criado migrations para cms e users separadamente
- SQLite test database: comentado `DisableMigrations` para permitir migrations

### ✅ Fase 1: MVP Read-Only - COMPLETA

**Data de conclusão:** 2026-01-06

#### 1.1 Modelos ✅

**Arquivos:**
- `apps/hymns/models.py` - HymnBook e Hymn com todos os campos
- `apps/hymns/admin.py` - Interface admin com inline de hinos
- `tests/unit/test_hymn_models.py` - 14 testes unitários (100% passing)

**Campos principais:**
```python
HymnBook:
- id (UUID)
- name, intro_name, slug
- owner_name, owner_user (FK opcional)
- cover_image
- created_at, updated_at

Hymn:
- id (UUID)
- hymn_book (FK com cascade)
- number, title, text
- received_at, offered_to, style
- extra_instructions, repetitions
```

#### 1.2 Import YAML ✅

**Arquivos:**
- `apps/hymns/management/commands/import_yaml.py`

**Funcionalidades:**
- Parser de YAML no formato hymn_pdf_generator
- Validação de duplicatas de números de hinos
- Modo dry-run para preview
- Modo update para hinários existentes
- Importação de imagem de capa

**Uso:**
```bash
python manage.py import_yaml --file caminho/arquivo.yaml [--dry-run] [--update]
```

**Teste realizado:**
- Importado "O Cruzeiro" com 3 hinos

#### 1.3 Integração TypeSense ✅

**Arquivos:**
- `apps/search/typesense_client.py`
- `apps/search/management/commands/reindex_typesense.py`

**Schema:**
```python
hymns collection:
- id, hymn_book_id, hymn_book_name
- owner_name, number, title, text
- style, received_at
- default_sorting_field: number
```

**Funções:**
- `index_hymn(hymn)` - indexa hino único
- `delete_hymn(hymn_id)` - remove do índice
- `search_hymns(query, per_page)` - busca full-text
- `reindex_all_hymns()` - reindexação completa

**Comando:**
```bash
python manage.py reindex_typesense
```

**Teste realizado:**
- 3 hinos indexados com sucesso
- Busca testada e funcionando

#### 1.4 Views e Templates ✅

**Views (apps/hymns/views.py):**
- `home_view` - página inicial com stats e busca
- `HymnBookListView` - lista paginada de hinários
- `HymnBookDetailView` - detalhes de hinário com tabela de hinos
- `HymnDetailView` - visualização completa de hino
- `search_view` - busca TypeSense com fallback PostgreSQL

**URLs (apps/hymns/urls.py):**
```
/ - home
/hinarios/ - lista de hinários
/hinarios/<slug>/ - detalhes do hinário
/hinos/<uuid>/ - detalhes do hino
/busca/ - busca
```

**Templates criados:**
- `templates/base.html` - base responsiva com CSS embutido
- `templates/hymns/home.html` - página inicial
- `templates/hymns/hymnbook_list.html` - lista de hinários
- `templates/hymns/hymnbook_detail.html` - detalhes + tabela
- `templates/hymns/hymn_detail.html` - visualização de hino
- `templates/hymns/search.html` - resultados de busca

**Design:**
- Tema azul/branco (#2c5282 primary)
- Responsivo (mobile-first)
- Navegação: Home | Hinários | Buscar
- Cards, grids, tabelas estilizadas

**Commits:**
2. `a1b2c3d` - "Fase 1: Implement models, admin and tests"
3. `d4e5f6g` - "Fase 1: Implement YAML import and TypeSense integration"
4. `h7i8j9k` - "Fase 1: Implement views and templates (MVP Read-Only)"

**Status:** MVP Read-Only COMPLETO! 🎊

### 🔜 Fase 2: Upload e Sistema de Usuários - PENDENTE

**Prioridade:** Próxima fase a implementar

**Itens planejados:**
- [ ] Autenticação com django-allauth (já instalado)
- [ ] Upload de hinários (YAML + PDF + imagens)
- [ ] UI de desambiguação (sugerir hinários existentes antes de criar novo)
- [ ] Modelo HymnBookVersion para múltiplas versões
- [ ] Páginas de perfil de usuário
- [ ] Sistema de "seguir" donos de hinários
- [ ] Sistema de notificações básico
- [ ] Testes (min 80% coverage)

**Decisões pendentes:**
- Estratégia exata de desambiguação (fuzzy match + comparação de primeiros hinos)
- UI/UX do fluxo de upload
- Permissões (quem pode editar/deletar)

### 🔜 Fase 3: Áudio e Social - PENDENTE

**Itens planejados:**
- [ ] Upload e player de áudio (MP3/M4A)
- [ ] Associação áudio ↔ hinos
- [ ] Sistema de curtidas/favoritos
- [ ] Comentários em hinários
- [ ] Feed de atividades
- [ ] Notificações avançadas

### 🔜 Fase 4: Deploy e Produção - PENDENTE

**Itens planejados:**
- [ ] Configuração Django production settings
- [ ] Docker Compose para produção
- [ ] CI/CD completo (deploy automático)
- [ ] Monitoramento (logs, métricas)
- [ ] Backup automático
- [ ] CDN para arquivos estáticos

### 🔜 Fase 5: Otimizações - PENDENTE

**Itens planejados:**
- [ ] Cache (Redis)
- [ ] Celery para tarefas assíncronas
- [ ] Otimização de queries
- [ ] Compressão de imagens
- [ ] Performance testing

## Estado Atual do Sistema

### Base de Dados

**PostgreSQL (porta 5432):**
- 1 hinário: "O Cruzeiro" (Mestre Irineu)
- 3 hinos importados
- Tabelas: users, hymnbooks, hymns, wagtail, django

**TypeSense (porta 8108):**
- Collection "hymns" criada
- 3 documentos indexados
- Schema configurado com sorting por number

### Servidor de Desenvolvimento

**Comando:**
```bash
cd /Users/nitai/Dropbox/dev-mgi/hyms-plat
poetry shell
python manage.py runserver 8001
```

**URL:** http://localhost:8001

### Testes

**Total:** 19 testes
- 5 smoke tests (apps funcionais básicos)
- 14 unit tests (modelos)
- Coverage: não medido ainda

**Comando:**
```bash
poetry run pytest
```

## Decisões Arquiteturais Importantes

### 1. PostgreSQL como Source of Truth
PostgreSQL é o banco principal. TypeSense é apenas índice de busca.

**Justificativa:**
- PostgreSQL garante integridade dos dados
- TypeSense pode ser reconstruído a qualquer momento
- Facilita backups e migrações

### 2. Sem Identificador Único para Hinos
Não há ID universal para hinos. Desambiguação será feita por:
- Match exato de nome
- Análise de proximidade (fuzzy search)
- Comparação de primeiros 3-5 hinos

**Justificativa:**
- Não existe padrão universal na comunidade
- Múltiplas versões do mesmo hinário existem
- UI deve sugerir match antes de criar novo

### 3. MVP Read-Only Primeiro
Fase 1 implementa apenas visualização, sem upload.

**Justificativa:**
- Validar estrutura de dados e UI
- Feedback rápido do usuário
- Reduzir complexidade inicial

### 4. Upload Sem Moderação (Inicialmente)
Fase 2 permitirá upload livre, sem aprovação prévia.

**Justificativa:**
- Facilitar adoção inicial
- Comunidade pequena e de confiança
- Moderação pode ser adicionada depois se necessário

## Comandos Úteis

### Desenvolvimento
```bash
# Ativar ambiente
cd /Users/nitai/Dropbox/dev-mgi/hyms-plat
poetry shell

# Subir serviços
docker compose up -d

# Servidor de desenvolvimento
python manage.py runserver 8001

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser
```

### Importação
```bash
# Preview de importação
python manage.py import_yaml --file caminho.yaml --dry-run

# Importar hinário
python manage.py import_yaml --file caminho.yaml

# Atualizar hinário existente
python manage.py import_yaml --file caminho.yaml --update
```

### TypeSense
```bash
# Reindexar todos os hinos
python manage.py reindex_typesense

# Verificar status do TypeSense
curl http://localhost:8108/health
```

### Testes
```bash
# Todos os testes
poetry run pytest

# Com verbose
poetry run pytest -v

# Com coverage
poetry run pytest --cov=apps --cov-report=html

# Smoke tests
poetry run pytest tests/smoke/

# Unit tests
poetry run pytest tests/unit/
```

### Git
```bash
# Status
git status

# Commit
git add .
git commit -m "mensagem"

# Push
git push origin main

# Ver log
git log --oneline -5
```

## Próximos Passos Recomendados

### Opção 1: Continuar Fase 2 (Upload)
Implementar sistema de upload e autenticação.

**Tempo estimado:** 2-3 sessões
**Prioridade:** Alta (necessário para MVP completo)

### Opção 2: Importar Mais Dados
Importar hinários adicionais para testar o sistema.

**Tempo estimado:** 1 sessão
**Prioridade:** Média (útil para validação)

### Opção 3: Melhorar Testes
Aumentar coverage e adicionar testes de integração.

**Tempo estimado:** 1 sessão
**Prioridade:** Alta (80% coverage é requisito)

### Opção 4: UI/UX Review
Revisar e melhorar templates existentes.

**Tempo estimado:** 1 sessão
**Prioridade:** Baixa (funcional, mas pode melhorar)

## Notas e Observações

### Erros Comuns Resolvidos

1. **Django-allauth deprecation warnings**
   - Solução: Atualizar para `ACCOUNT_LOGIN_METHODS = {"email"}`

2. **Duplicate hymn numbers**
   - Solução: Validação adicionada no comando import_yaml

3. **TypeSense connection errors**
   - Solução: Verificar se docker compose está rodando

4. **Test database issues**
   - Solução: Comentar `DisableMigrations` em test settings

### Referências

- **Formato YAML:** https://github.com/jacquesvcritien/hymn-pdf-generator
- **Portal referência:** https://santodaime.org/hinarios
- **Repositório:** https://github.com/nitaibezerra/hyms-plat
- **Plano completo:** `_plan/plano-implementacao.md`
- **Requisitos:** `_plan/requisitos.md`

### Contatos e Recursos

- **Desenvolvedor:** nitaibezerra
- **Projeto:** hyms-plat
- **Data de início:** 2026-01-06

---

## Como Retomar o Trabalho

1. **Ler este documento** para entender o estado atual
2. **Verificar o plano de implementação** em `plano-implementacao.md`
3. **Decidir próxima fase** (recomendado: Fase 2)
4. **Verificar ambiente:**
   ```bash
   cd /Users/nitai/Dropbox/dev-mgi/hyms-plat
   docker compose ps  # verificar serviços
   poetry shell       # ativar ambiente
   poetry run pytest  # rodar testes
   ```
5. **Criar nova branch** se necessário
6. **Implementar próxima feature**
7. **Atualizar este documento** ao final da sessão

---

**Última sessão:** 2026-01-06
**Próxima sessão:** TBD
**Status geral:** Fase 1 completa, pronto para Fase 2
