# Plano de Documentação Completa - hyms-plat

**Projeto:** Portal de Hinários do Santo Daime
**Data:** 2026-01-10
**Objetivo:** Criar documentação completa para usuários e desenvolvedores usando MkDocs

---

## 📋 Executive Summary

### Contexto
O projeto **hyms-plat** é um portal Django/Wagtail para pesquisa e acesso a hinários do Santo Daime. Atualmente possui:
- ✅ **Fase 0-1 completa:** Models, Views, TypeSense, Import YAML
- ✅ **98.19% de cobertura de testes** (153 testes)
- ⏳ **Fases 2-4 pendentes:** Upload, Áudio, Social, Deploy

### Públicos-Alvo Definidos
1. **Usuários finais** - Comunidade Santo Daime usando o portal
2. **Equipe de desenvolvimento interna** - Mantém e evolui o projeto

### Escopo do Plano
Este plano documenta **TODAS AS FASES** (0-4), incluindo funcionalidades futuras, para ser executado após implementação completa das Fases 2-4.

### Formato Escolhido
**MkDocs** com tema Material Design - site estático com navegação, busca e responsivo

### Prioridade
**Documentação de Usuário** tem prioridade, mas ambas serão criadas em paralelo.

---

## 🎯 Objetivos do Plano

### Para Usuários
- Guia completo de como usar o portal (buscar, visualizar, contribuir)
- Guia visual com screenshots
- FAQ e troubleshooting
- Tutoriais passo-a-passo

### Para Desenvolvedores
- Arquitetura do sistema
- Guia de setup e contribuição
- Referência de APIs e models
- Padrões de código e testes
- Guia de deployment

---

## 📐 Arquitetura de Informação

### 1. Documentação de Usuário

```
docs/user-guide/
├── index.md                      # Introdução ao portal
├── getting-started.md            # Primeiros passos
├── searching-hymns.md            # Como buscar hinos
├── browsing-hymnbooks.md         # Navegar por hinários
├── viewing-hymns.md              # Visualizar letra de hinos
├── user-accounts.md              # Criar conta e login (Fase 2)
├── uploading-hymnbooks.md        # Upload de hinários (Fase 2)
├── contributing-content.md       # Como contribuir (Fase 2)
├── audio-features.md             # Áudio e player (Fase 3)
├── social-features.md            # Curtir, favoritar, comentar (Fase 3)
├── faq.md                        # Perguntas frequentes
└── troubleshooting.md            # Problemas comuns
```

**Princípios:**
- Linguagem simples e acessível
- Screenshots em todas as páginas
- Tutoriais passo-a-passo numerados
- Links para conceitos relacionados
- Exemplos práticos

### 2. Documentação de Desenvolvedor

```
docs/developer-guide/
├── index.md                      # Visão geral para devs
├── architecture/
│   ├── overview.md               # Arquitetura geral
│   ├── technology-stack.md       # Stack tecnológico
│   ├── data-models.md            # Models e ERD
│   ├── search-architecture.md    # TypeSense integration
│   └── decisions.md              # ADRs (Architecture Decision Records)
├── setup/
│   ├── local-development.md      # Setup local completo
│   ├── docker-services.md        # PostgreSQL, TypeSense, Redis
│   ├── environment-variables.md  # Variáveis de ambiente
│   └── common-issues.md          # Problemas comuns de setup
├── contributing/
│   ├── getting-started.md        # Como contribuir
│   ├── code-style.md             # Black, isort, ruff
│   ├── testing.md                # Escrevendo testes
│   ├── pull-requests.md          # Workflow de PR
│   └── commit-guidelines.md      # Conventional commits
├── api-reference/
│   ├── models.md                 # Referência completa de models
│   ├── views.md                  # Views e URLs
│   ├── management-commands.md    # Commands disponíveis
│   ├── typesense-client.md       # API TypeSense
│   └── utils.md                  # Utilities
├── guides/
│   ├── importing-yaml.md         # Importar hinários via YAML
│   ├── indexing-search.md        # Reindexar TypeSense
│   ├── adding-features.md        # Adicionar novas features
│   ├── working-with-wagtail.md   # CMS Wagtail
│   └── celery-tasks.md           # Background tasks (Fase 2+)
├── deployment/
│   ├── overview.md               # Visão geral de deploy
│   ├── production-setup.md       # Configuração produção
│   ├── ci-cd.md                  # GitHub Actions
│   ├── monitoring.md             # Logs e métricas
│   └── backup-restore.md         # Backup e restore
└── testing/
    ├── overview.md               # Estratégia de testes
    ├── unit-tests.md             # Testes unitários
    ├── integration-tests.md      # Testes de integração
    ├── e2e-tests.md              # Testes E2E (Playwright)
    └── coverage.md               # Coverage e CI
```

**Princípios:**
- Documentação técnica precisa
- Código comentado e exemplos
- Diagramas arquiteturais
- Links para código-fonte
- Comandos copiáveis

### 3. Documentação Geral (Raiz)

```
docs/
├── index.md                      # Landing page
├── about.md                      # Sobre o projeto
├── roadmap.md                    # Fases e roadmap
├── changelog.md                  # Histórico de mudanças
├── license.md                    # Licença do projeto
└── community.md                  # Como se envolver
```

---

## 📝 Conteúdo Detalhado por Documento

### SEÇÃO 1: Documentação de Usuário

#### `docs/user-guide/index.md`
```markdown
# Bem-vindo ao Portal de Hinários

O Portal de Hinários é uma plataforma para pesquisa, visualização e compartilhamento de hinários do Santo Daime.

## O que você pode fazer

- 🔍 **Buscar hinos** por título, letra ou hinário
- 📚 **Navegar hinários** completos com todos os hinos
- 📖 **Visualizar letras** formatadas e completas
- 👤 **Criar conta** e contribuir com conteúdo (em breve)
- 🎵 **Ouvir áudios** de hinos (em breve)
- ❤️ **Favoritar** seus hinos preferidos (em breve)

## Como começar

1. [Primeiros Passos](getting-started.md) - Navegue pela interface
2. [Buscar Hinos](searching-hymns.md) - Aprenda a buscar eficientemente
3. [Navegar Hinários](browsing-hymnbooks.md) - Explore hinários completos

## Screenshots

[Incluir screenshots da home, busca, hinário, hino]
```

#### `docs/user-guide/getting-started.md`
```markdown
# Primeiros Passos

## Interface Principal

### Página Inicial

[Screenshot da home com anotações]

A página inicial mostra:
1. **Barra de busca** - Digite para buscar hinos
2. **Estatísticas** - Total de hinários e hinos
3. **Hinários Recentes** - Últimos 6 hinários adicionados
4. **Menu de Navegação** - Home, Hinários, Buscar

### Navegação

#### Menu Principal
- **Home** - Volta para página inicial
- **Hinários** - Lista completa de hinários
- **Buscar** - Página de busca avançada

## Dicas de Uso

💡 Use a barra de busca em qualquer página
💡 Clique no hinário para ver todos os hinos
💡 Favoritos e conta exigem login (em breve)
```

#### `docs/user-guide/searching-hymns.md`
```markdown
# Como Buscar Hinos

## Busca Simples

1. Digite o termo na barra de busca
2. Pressione Enter ou clique na lupa
3. Veja os resultados ordenados por relevância

[Screenshot da busca]

## O que você pode buscar

- **Título do hino** - Ex: "Lua Branca"
- **Letra do hino** - Ex: "Da luz serena"
- **Nome do hinário** - Ex: "Cruzeiro"
- **Nome do dono** - Ex: "Mestre Irineu"

## Dicas de Busca

### Busca Exata
Use aspas para buscar frase exata:
```
"Lua Branca"
```

### Busca Parcial
Digite parte da palavra (mínimo 3 letras):
```
luz → encontra "Lua Branca da luz serena"
```

### Caracteres Especiais
O sistema lida automaticamente com acentos:
```
"jose" encontra "José"
"irineu" encontra "Irineu"
```

## Resultados da Busca

Cada resultado mostra:
- **Número e Título** do hino
- **Hinário** e dono
- **Preview da letra** (primeiras 40 palavras)
- **Estilo musical** (se disponível)

[Screenshot dos resultados]

## Sem Resultados?

Se não encontrou o que procura:
- ✓ Verifique a ortografia
- ✓ Use palavras-chave mais curtas
- ✓ Tente sinônimos
- ✓ Navegue pelos [Hinários](browsing-hymnbooks.md) manualmente
```

#### `docs/user-guide/browsing-hymnbooks.md`
```markdown
# Navegar por Hinários

## Lista de Hinários

Acesse **Hinários** no menu para ver todos os hinários disponíveis.

[Screenshot da lista]

### Informações Exibidas

Para cada hinário você vê:
- **Capa** (se disponível)
- **Nome** do hinário
- **Dono** (quem recebeu)
- **Quantidade** de hinos
- **Descrição** resumida

### Ordenação

Hinários são ordenados alfabeticamente por nome.

### Paginação

A lista mostra 20 hinários por página. Use os botões de paginação:
- **Primeira** - Vai para primeira página
- **Anterior** - Página anterior
- **Próxima** - Próxima página
- **Última** - Última página

## Detalhes do Hinário

Clique em **"Ver Hinário"** para ver todos os hinos.

[Screenshot de detalhes]

### Informações Completas

- **Capa grande** (300x400)
- **Nome completo** e nome curto
- **Dono** do hinário
- **Descrição** completa
- **Total de hinos**

### Tabela de Hinos

Todos os hinos são listados em tabela:

| Número | Título | Estilo | Ação |
|--------|--------|--------|------|
| 1 | Lua Branca | Valsa | Ver |
| 2 | Tuperci | Marcha | Ver |

Clique em qualquer linha para ver a letra completa.
```

#### `docs/user-guide/viewing-hymns.md`
```markdown
# Visualizar Letra de Hinos

## Página do Hino

Quando você clica em um hino, vê a letra completa formatada.

[Screenshot da página de hino]

## Informações do Hino

### Cabeçalho
- **Número** do hino no hinário
- **Título** em destaque
- **Hinário** e dono (breadcrumb clicável)

### Letra Completa
A letra é exibida preservando:
- ✓ Quebras de linha originais
- ✓ Estrofes separadas
- ✓ Formatação especial

### Metadados

Quando disponíveis:
- **Estilo** - Ex: Valsa, Marcha, Mazurca
- **Recebido em** - Data que o hino foi recebido
- **Oferecido para** - Pessoa dedicatária
- **Repetições** - Ex: "1-4, 5-8"
- **Instruções extras** - Instruções especiais de canto

## Navegação

- **Voltar** - Clica no hinário para voltar
- **Buscar outro** - Use a barra de busca
```

#### `docs/user-guide/user-accounts.md` (Fase 2)
```markdown
# Contas de Usuário

> ⚠️ **Em Desenvolvimento** - Esta funcionalidade será lançada na Fase 2

## Criando uma Conta

1. Clique em **"Entrar"** no menu
2. Selecione **"Criar Conta"**
3. Escolha o método:
   - 📧 Email e senha
   - 🔐 Google
   - 🔐 Facebook (opcional)
4. Preencha seus dados
5. Confirme o email
6. Pronto! Você já pode fazer login

[Screenshots do processo]

## Seu Perfil

Após criar conta, você pode:
- ✏️ Editar biografia
- 📷 Upload de avatar
- ❤️ Ver seus hinos favoritos
- 📚 Ver hinários que você subiu
- 👥 Ver usuários que você segue

## Login

1. Clique em **"Entrar"**
2. Digite email e senha OU use login social
3. Clique em **"Entrar"**

## Recuperar Senha

1. Na tela de login, clique **"Esqueci a senha"**
2. Digite seu email
3. Verifique sua caixa de entrada
4. Clique no link recebido
5. Crie nova senha

## Privacidade

Seus dados são protegidos. Ver [Política de Privacidade](../privacy.md).
```

#### `docs/user-guide/uploading-hymnbooks.md` (Fase 2)
```markdown
# Upload de Hinários

> ⚠️ **Em Desenvolvimento** - Esta funcionalidade será lançada na Fase 2

## Pré-requisitos

- ✓ Ter uma [conta criada](user-accounts.md)
- ✓ Estar logado
- ✓ Ter o arquivo YAML do hinário OU PDF

## Upload via YAML

### 1. Preparar o Arquivo YAML

Crie um arquivo `.yaml` com esta estrutura:

```yaml
hymn_book:
  name: "Nome do Hinário"
  owner: "Nome do Dono"
  intro_name: "Nome Curto (opcional)"
  description: "Descrição completa do hinário"
  hymns:
    - number: 1
      title: "Título do Hino"
      text: |
        Letra do hino
        Com quebras de linha
        Preservadas
      received_at: "1930-07-15"  # opcional
      style: "Valsa"              # opcional
      offered_to: "Nome"          # opcional
      extra_instructions: "..."   # opcional
      repetitions: "1-4, 5-8"     # opcional
    - number: 2
      title: "Segundo Hino"
      text: "Letra..."
```

### 2. Fazer Upload

1. Clique em **"Contribuir"** no menu
2. Selecione **"Novo Hinário"**
3. Escolha **"Upload YAML"**
4. Arraste o arquivo ou clique para selecionar
5. Clique **"Enviar"**

[Screenshot do formulário]

### 3. Revisão

Após upload:
- ✓ Sistema valida o YAML
- ✓ Detecta duplicatas
- ✓ Mostra preview
- ✓ Você confirma ou corrige

### 4. Publicação

Após confirmação:
- ✓ Hinário é salvo no banco
- ✓ Hinos são indexados na busca
- ✓ Você é creditado como contribuidor

## Upload via PDF

### 1. Preparar PDF

Certifique-se que o PDF:
- ✓ É legível e texto selecionável (não imagem)
- ✓ Tem estrutura clara (título, número, letra)
- ✓ Está completo

### 2. Fazer Upload

1. Selecione **"Upload PDF"**
2. Arraste o PDF
3. O sistema usa OCR para extrair texto
4. Revise e corrija os dados extraídos
5. Confirme

[Screenshot do processo]

## Atualizar Hinário Existente

### Desambiguação

Se o hinário já existe, o sistema:
1. Detecta possível duplicata
2. Mostra hinários similares
3. Pergunta se você quer:
   - **Atualizar existente** - Substitui dados
   - **Criar nova versão** - Mantém ambos
   - **Cancelar** - Não faz upload

### Versionamento

Hinários podem ter múltiplas versões:
- **Versão oficial** - Mais recente aprovada
- **Versões anteriores** - Histórico preservado
- **Diferenças** - Comparar versões lado-a-lado

## Diretrizes de Qualidade

### ✅ Fazer
- Use ortografia correta
- Preserve formatação original
- Inclua metadados quando possível
- Verifique números duplicados

### ❌ Evitar
- Copiar de fontes protegidas sem permissão
- Upload de conteúdo ofensivo
- Informações falsas ou incorretas

## Moderação

Todos os uploads passam por:
1. **Validação automática** - Verifica estrutura
2. **Revisão comunitária** (opcional) - Outros usuários podem sugerir melhorias
3. **Aprovação moderador** (para novos usuários)

## Limites

- **Tamanho YAML:** Até 10 MB
- **Tamanho PDF:** Até 50 MB
- **Uploads por dia:** 10 hinários (aumenta com reputação)
```

#### `docs/user-guide/audio-features.md` (Fase 3)
```markdown
# Recursos de Áudio

> ⚠️ **Em Desenvolvimento** - Esta funcionalidade será lançada na Fase 3

## Player de Áudio

Alguns hinos têm áudio disponível. Quando disponível, você verá um player na página do hino.

[Screenshot do player]

### Controles

- ▶️ **Play/Pause** - Tocar ou pausar
- ⏮️ **Anterior** - Hino anterior no hinário
- ⏭️ **Próximo** - Próximo hino
- 🔊 **Volume** - Ajustar volume
- 🔄 **Repetir** - Repetir hino atual
- 📥 **Download** - Baixar áudio (se permitido)

### Formatos Suportados

- MP3 (até 320kbps)
- OGG Vorbis
- FLAC (lossless)

## Contribuir com Áudio

### 1. Preparar Arquivo

Requisitos:
- ✓ Qualidade mínima: 128kbps
- ✓ Formato: MP3, OGG ou FLAC
- ✓ Tamanho máximo: 25 MB por arquivo
- ✓ Você tem direitos para compartilhar

### 2. Upload

1. Vá para página do hino
2. Clique **"Adicionar Áudio"**
3. Arraste o arquivo ou selecione
4. Adicione informações:
   - **Fonte** - Onde foi gravado
   - **Data** - Quando foi gravado
   - **Créditos** - Quem cantou/gravou
5. Clique **"Enviar"**

### 3. Moderação

Áudios passam por:
- ✓ Validação de formato e qualidade
- ✓ Verificação de direitos autorais
- ✓ Aprovação de moderador

## Playlist

Crie playlists personalizadas:
1. Navegue pelos hinos
2. Clique no **"+"** ao lado do hino
3. Selecione playlist ou crie nova
4. Acesse suas playlists no perfil

## Download

Alguns áudios permitem download:
- 📥 **Download individual** - Um hino por vez
- 📦 **Download do hinário** - ZIP com todos os áudios
```

#### `docs/user-guide/social-features.md` (Fase 3)
```markdown
# Recursos Sociais

> ⚠️ **Em Desenvolvimento** - Esta funcionalidade será lançada na Fase 3

## Curtir Hinos

Curta seus hinos favoritos:
1. Vá para página do hino
2. Clique no ❤️ **"Curtir"**
3. Hino é adicionado aos seus favoritos

Ver todos os favoritos:
- Acesse seu **Perfil**
- Clique em **"Favoritos"**
- Veja lista completa

## Comentários

Deixe comentários nos hinos:
1. Role até seção de comentários
2. Digite seu comentário
3. Clique **"Enviar"**

[Screenshot de comentários]

### Regras

- ✓ Seja respeitoso
- ✓ Contribua construtivamente
- ✓ Não spam
- ✗ Sem conteúdo ofensivo

### Moderação

Comentários são moderados:
- 🚫 **Reportar** - Clique para reportar abuso
- 👤 **Editar** - Edite seus próprios comentários (15 min)
- 🗑️ **Deletar** - Delete seus comentários

## Seguir Usuários

Siga outros contribuidores:
1. Vá para perfil do usuário
2. Clique **"Seguir"**
3. Receba notificações de novos uploads

Ver quem você segue:
- **Perfil** → **Seguindo**

## Notificações

Receba notificações de:
- 💬 Resposta ao seu comentário
- ❤️ Alguém curtiu seu upload
- 📚 Usuário que você segue fez upload
- ✅ Seu upload foi aprovado

[Screenshot de notificações]

Gerenciar notificações:
- **Perfil** → **Configurações** → **Notificações**
```

#### `docs/user-guide/faq.md`
```markdown
# Perguntas Frequentes

## Geral

### O que é o Portal de Hinários?
É uma plataforma para pesquisa, visualização e compartilhamento de hinários do Santo Daime.

### O portal é gratuito?
Sim, 100% gratuito e sem anúncios.

### Preciso de conta para buscar hinos?
Não, busca e visualização são públicas. Conta é necessária apenas para contribuir.

## Busca

### Não encontrei o hino que procuro
- Verifique ortografia
- Tente palavras-chave mais curtas
- Navegue manualmente pelo hinário
- [Contribua](uploading-hymnbooks.md) com o hino!

### A busca considera acentos?
Sim, a busca é inteligente e encontra resultados mesmo com diferenças de acentuação.

## Conteúdo

### Posso baixar os hinários?
Sim, você pode visualizar e copiar as letras. Áudios podem ser baixados quando disponível.

### Posso imprimir os hinos?
Sim, use a função de impressão do navegador na página do hino.

### Como sei se o conteúdo é oficial?
Hinários têm badge de "✓ Verificado" quando validados por moderadores.

## Contribuição

### Como envio um hinário?
Ver guia completo em [Upload de Hinários](uploading-hymnbooks.md).

### Meu upload foi rejeitado, por quê?
Possíveis razões:
- Duplicata de hinário existente
- Qualidade insuficiente
- Violação de direitos autorais
- Conteúdo incompleto

### Posso editar um hinário existente?
Sim, você pode sugerir edições que passarão por revisão.

## Técnico

### Quais navegadores são suportados?
- Chrome/Edge (recomendado)
- Firefox
- Safari
- Mobile: Chrome, Safari iOS

### O site funciona em celular?
Sim, totalmente responsivo e otimizado para mobile.

### Há um app?
Ainda não, mas o site mobile oferece ótima experiência.

## Privacidade

### Meus dados são compartilhados?
Não, ver [Política de Privacidade](../privacy.md).

### Posso deletar minha conta?
Sim, em **Perfil** → **Configurações** → **Deletar Conta**.
```

#### `docs/user-guide/troubleshooting.md`
```markdown
# Solução de Problemas

## Problemas Comuns

### Busca não retorna resultados

**Sintoma:** Busca vazia ou "Nenhum resultado encontrado"

**Soluções:**
1. ✓ Verifique ortografia
2. ✓ Use 3+ caracteres
3. ✓ Tente palavra-chave diferente
4. ✓ Limpe o cache do navegador
5. ✓ Recarregue a página

Se persistir, pode ser problema temporário de indexação. Aguarde alguns minutos.

### Página não carrega

**Sintoma:** Tela branca ou erro 500

**Soluções:**
1. ✓ Recarregue a página (Ctrl+R ou Cmd+R)
2. ✓ Limpe cache: Ctrl+Shift+Del
3. ✓ Tente outro navegador
4. ✓ Desative extensões (modo anônimo)
5. ✓ Verifique sua conexão de internet

### Imagens não aparecem

**Sintoma:** Capas de hinários não carregam

**Soluções:**
1. ✓ Aguarde carregamento completo
2. ✓ Recarregue a página
3. ✓ Verifique se as imagens estão bloqueadas (AdBlock)

### Login não funciona

**Sintoma:** "Email ou senha incorretos"

**Soluções:**
1. ✓ Verifique caps lock
2. ✓ Tente recuperar senha
3. ✓ Use login social (Google/Facebook)
4. ✓ Limpe cookies do site

### Upload falha

**Sintoma:** Erro ao fazer upload de YAML/PDF

**Soluções:**
1. ✓ Verifique tamanho do arquivo (limites: YAML 10MB, PDF 50MB)
2. ✓ Valide estrutura do YAML
3. ✓ Verifique formato do PDF (texto selecionável)
4. ✓ Tente navegador diferente
5. ✓ Verifique sua conexão de internet

### Áudio não toca

**Sintoma:** Player não reproduz áudio

**Soluções:**
1. ✓ Verifique volume do sistema e do player
2. ✓ Tente outro navegador
3. ✓ Verifique se há bloqueador de áudio
4. ✓ Recarregue a página
5. ✓ Limpe cache

## Reportar Problema

Se nenhuma solução funcionou:
1. Acesse [GitHub Issues](https://github.com/seu-repo/hyms-plat/issues)
2. Verifique se já foi reportado
3. Crie novo issue com:
   - Descrição do problema
   - Passos para reproduzir
   - Screenshots
   - Navegador e versão
   - Sistema operacional

## Contato

Precisa de ajuda?
- 📧 Email: suporte@portal-hinarios.com.br
- 💬 Fórum: [forum.portal-hinarios.com.br]
- 🐛 Bugs: [GitHub Issues]
```

---

### SEÇÃO 2: Documentação de Desenvolvedor

#### `docs/developer-guide/index.md`
```markdown
# Guia do Desenvolvedor

Bem-vindo à documentação técnica do **hyms-plat**!

## Visão Geral

O hyms-plat é um portal Django/Wagtail para hinários do Santo Daime com:
- 🔍 Busca avançada via TypeSense
- 📚 CMS Wagtail para páginas
- 🎵 Upload de áudio (Fase 3)
- 👥 Features sociais (Fase 3)
- 🐳 Docker para serviços externos

## Stack Tecnológico

- **Backend:** Django 5.1 + Python 3.11+
- **CMS:** Wagtail 6.4
- **Banco:** PostgreSQL 16
- **Search:** TypeSense 27.1
- **Task Queue:** Celery + Redis
- **Testes:** pytest + 98.19% coverage

Ver [Technology Stack](architecture/technology-stack.md) completo.

## Começando

1. [Setup Local](setup/local-development.md) - Configure ambiente
2. [Arquitetura](architecture/overview.md) - Entenda o sistema
3. [Contribuindo](contributing/getting-started.md) - Faça sua primeira contribuição
4. [Testes](testing/overview.md) - Escreva testes

## Links Rápidos

- [Models Reference](api-reference/models.md)
- [Management Commands](api-reference/management-commands.md)
- [Code Style](contributing/code-style.md)
- [Deploy Guide](deployment/overview.md)

## Status do Projeto

| Fase | Status | Cobertura de Testes |
|------|--------|---------------------|
| Fase 0: Setup | ✅ Completa | N/A |
| Fase 1: MVP Read-Only | ✅ Completa | 98.19% |
| Fase 2: Upload & Users | ⏳ Planejada | - |
| Fase 3: Áudio & Social | ⏳ Planejada | - |
| Fase 4: Deploy & Prod | ⏳ Planejada | - |

Ver [Roadmap](../roadmap.md) completo.
```

#### `docs/developer-guide/architecture/overview.md`
```markdown
# Arquitetura do Sistema

## Visão Geral

O hyms-plat usa arquitetura monolítica Django com separação de apps por domínio.

```
┌─────────────────────────────────────────────┐
│             Usuário / Browser               │
└──────────────────┬──────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────┐
│          gunicorn + whitenoise              │
│         (application server)                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              Django 5.1                     │
│  ┌───────────────────────────────────────┐  │
│  │  apps/                                │  │
│  │  ├── hymns/    (Core)                │  │
│  │  ├── search/   (TypeSense)           │  │
│  │  ├── cms/      (Wagtail)             │  │
│  │  ├── users/    (Auth)                │  │
│  │  └── core/     (Base)                │  │
│  └───────────────────────────────────────┘  │
└────┬─────────────────────────┬──────────────┘
     │                         │
     │                         │
┌────▼────────┐    ┌───────────▼─────────────┐
│ PostgreSQL  │    │   TypeSense 27.1        │
│   16.x      │    │   (Search Engine)       │
│  (primary)  │    └─────────────────────────┘
└─────────────┘
     │
┌────▼────────┐    ┌─────────────────────────┐
│   Redis 7   │    │  Celery Workers         │
│ (cache +    │◄───┤  (background tasks)     │
│  broker)    │    └─────────────────────────┘
└─────────────┘
```

## Apps Django

### `apps/hymns/` (Core)
**Responsabilidades:**
- Models: HymnBook, Hymn
- Views: Home, List, Detail, Search
- Admin: Interface de gerenciamento
- Commands: import_yaml

**Dependencies:**
- apps.search (TypeSense integration)
- apps.users (FK owner_user)

### `apps/search/`
**Responsabilidades:**
- TypeSense client wrapper
- Index/reindex functions
- Search queries
- Commands: reindex_typesense

**Dependencies:**
- apps.hymns (Hymn model)

### `apps/cms/`
**Responsabilidades:**
- Wagtail HomePage model
- CMS pages editáveis

**Dependencies:**
- Wagtail

### `apps/users/`
**Responsabilidades:**
- Custom User model (bio, avatar)
- django-allauth integration

**Dependencies:**
- django-allauth

### `apps/core/`
**Responsabilidades:**
- Base mixins
- Common utilities
- Shared models (futuro)

## Fluxo de Dados

### 1. Importação YAML → DB

```
1. Admin roda: python manage.py import_yaml hinario.yaml
2. Command lê e valida YAML
3. Cria HymnBook + Hymns em transaction
4. Auto-indexa no TypeSense via signal
```

### 2. Busca de Usuário

```
1. User digita query em /busca/
2. search_view chama search_hymns()
3. TypeSense retorna IDs ordenados por relevância
4. Django busca Hymns no PostgreSQL preservando ordem
5. Template renderiza resultados
```

### 3. Upload de Hinário (Fase 2)

```
1. User faz upload via form
2. Celery task processa arquivo assíncrono
3. Valida e extrai dados
4. Detecta duplicatas (fuzzy match)
5. Cria HymnBookVersion
6. Indexa no TypeSense
7. Notifica user
```

## Patterns e Decisões

Ver [Architecture Decision Records](decisions.md) para decisões detalhadas.

### UUID como Primary Key
- **Por quê:** Melhor para distributed systems, privacy
- **Trade-off:** Índices maiores que auto-increment

### TypeSense vs ElasticSearch
- **Por quê:** TypeSense mais simples, menor overhead, typo-tolerance nativo
- **Trade-off:** Menos features avançadas

### Celery para Background Tasks
- **Por quê:** Upload, OCR, reindexação são lentos
- **Trade-off:** Mais complexidade operacional

### Wagtail CMS
- **Por quê:** CMS Django-native para páginas editáveis
- **Trade-off:** Overhead para features simples
```

#### `docs/developer-guide/architecture/data-models.md`
```markdown
# Models e Schema

## ERD (Entity Relationship Diagram)

```
┌──────────────────────────┐
│       User               │
│  (apps.users.User)       │
├──────────────────────────┤
│ id: UUID (PK)            │
│ email: str (unique)      │
│ username: str (unique)   │
│ bio: text                │
│ avatar: image            │
└────────────┬─────────────┘
             │ 1
             │ owner_user (nullable)
             │
             │ *
┌────────────▼─────────────┐        ┌─────────────────────────┐
│     HymnBook             │  1   * │        Hymn             │
│  (apps.hymns.HymnBook)   ├────────┤  (apps.hymns.Hymn)      │
├──────────────────────────┤        ├─────────────────────────┤
│ id: UUID (PK)            │        │ id: UUID (PK)           │
│ name: str (unique idx)   │        │ hymn_book_id: FK        │
│ slug: str (unique)       │        │ number: int             │
│ intro_name: str          │        │ title: str (idx)        │
│ owner_name: str (idx)    │        │ text: text              │
│ owner_user_id: FK (null) │        │ received_at: date (idx) │
│ cover_image: image       │        │ offered_to: str         │
│ description: text        │        │ style: str              │
│ created_at: datetime     │        │ extra_instructions: txt │
│ updated_at: datetime     │        │ repetitions: str        │
└──────────────────────────┘        │ created_at: datetime    │
                                    │ updated_at: datetime    │
                                    └─────────────────────────┘
                                    unique_together: (hymn_book, number)
```

## Models Detalhados

### `apps.hymns.models.HymnBook`

```python
class HymnBook(models.Model):
    """Hinário - coleção de hinos."""

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identificação
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Nome do hinário"
    )
    intro_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nome de exibição curto"
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        help_text="Auto-gerado de 'name'"
    )

    # Proprietário
    owner_name = models.CharField(
        max_length=255,
        help_text="Pessoa que recebeu o hinário (texto livre)"
    )
    owner_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_hymnbooks',
        help_text="Usuário cadastrado como dono"
    )

    # Mídia e descrição
    cover_image = models.ImageField(
        upload_to='hymn_covers/',
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hinário"
        verbose_name_plural = "Hinários"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner_name']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        """Auto-gera slug se não existir."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def hymn_count(self):
        """Retorna número de hinos."""
        return self.hymns.count()
```

**Indexes:**
- `name` - Busca rápida por nome
- `owner_name` - Filtrar por dono
- `created_at` - Ordenar por recentes

**Constraints:**
- `name` UNIQUE - Evita duplicatas
- `slug` UNIQUE - URLs únicas

### `apps.hymns.models.Hymn`

```python
class Hymn(models.Model):
    """Hino individual dentro de um hinário."""

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relacionamento
    hymn_book = models.ForeignKey(
        HymnBook,
        on_delete=models.CASCADE,
        related_name='hymns',
        verbose_name="Hinário"
    )

    # Identificação
    number = models.PositiveIntegerField(
        help_text="Número sequencial no hinário"
    )
    title = models.CharField(
        max_length=255,
        db_index=True
    )

    # Conteúdo
    text = models.TextField(
        help_text="Letra completa do hino"
    )

    # Metadados (opcionais)
    received_at = models.DateField(
        null=True,
        blank=True,
        help_text="Data em que o hino foi recebido"
    )
    offered_to = models.CharField(
        max_length=255,
        blank=True,
        help_text="Pessoa dedicatária"
    )
    style = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ex: Valsa, Marcha, Mazurca"
    )
    extra_instructions = models.TextField(
        blank=True,
        help_text="Instruções especiais de canto"
    )
    repetitions = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ex: 1-4, 5-8 (estrofes a repetir)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hino"
        verbose_name_plural = "Hinos"
        ordering = ['hymn_book', 'number']
        unique_together = [['hymn_book', 'number']]
        indexes = [
            models.Index(fields=['hymn_book', 'number']),
            models.Index(fields=['title']),
            models.Index(fields=['received_at']),
        ]

    @property
    def full_title(self):
        """Título completo: Hinário - Nº. Título"""
        return f"{self.hymn_book.name} - {self.number}. {self.title}"
```

**Indexes:**
- `(hymn_book, number)` - Lookup rápido
- `title` - Busca por título
- `received_at` - Ordenar por data

**Constraints:**
- `unique_together(hymn_book, number)` - Número único por hinário
- `CASCADE delete` - Deleta hinos quando hinário é deletado

## TypeSense Schema

```python
HYMNS_SCHEMA = {
    'name': 'hymns',
    'fields': [
        {'name': 'id', 'type': 'string'},
        {'name': 'hymn_book_id', 'type': 'string'},
        {'name': 'hymn_book_name', 'type': 'string', 'facet': True},
        {'name': 'hymn_book_slug', 'type': 'string'},
        {'name': 'owner_name', 'type': 'string', 'facet': True},
        {'name': 'number', 'type': 'int32', 'sort': True},
        {'name': 'title', 'type': 'string'},
        {'name': 'text', 'type': 'string'},
        {'name': 'style', 'type': 'string', 'facet': True, 'optional': True},
        {'name': 'received_at', 'type': 'int64', 'optional': True},  # Unix timestamp
    ],
    'default_sorting_field': 'number'
}
```

**Facets:** hymn_book_name, owner_name, style - Para filtros
**Sortable:** number - Ordenação numérica
**Searchable:** title, text - Full-text search com typo-tolerance

## Migrations

Ver histórico em `apps/hymns/migrations/` e `apps/users/migrations/`.

**Principais migrations:**
- `0001_initial.py` - Cria HymnBook e Hymn
- `0002_add_indexes.py` - Adiciona índices de performance
- `0003_add_cover_image.py` - Adiciona campo cover_image
```

*(Continuando na próxima parte devido ao tamanho...)*

---

## 🛠️ Implementação

### Fase 1: Setup MkDocs (1 hora)

**Tarefas:**
1. Instalar MkDocs e tema Material
2. Criar estrutura de diretórios `docs/`
3. Configurar `mkdocs.yml`
4. Adicionar ao `.gitignore`: `site/`
5. Testar build local

**Arquivos criados:**
- `mkdocs.yml` (configuração)
- `docs/index.md` (landing page)
- `.gitignore` (atualizado)

**Comandos:**
```bash
pip install mkdocs-material
mkdocs new .
mkdocs serve  # Testa em http://127.0.0.1:8000
mkdocs build  # Gera site/
```

### Fase 2: Documentação de Usuário (8-12 horas)

**Prioridade Alta:**
1. `getting-started.md` - Screenshots e guia visual
2. `searching-hymns.md` - Como buscar eficientemente
3. `browsing-hymnbooks.md` - Navegação por hinários
4. `viewing-hymns.md` - Visualizar letras
5. `faq.md` - Perguntas frequentes
6. `troubleshooting.md` - Problemas comuns

**Prioridade Média (Fase 2-3):**
7. `user-accounts.md` - Criar conta
8. `uploading-hymnbooks.md` - Upload YAML/PDF
9. `contributing-content.md` - Diretrizes
10. `audio-features.md` - Player e upload áudio
11. `social-features.md` - Curtir, comentar, seguir

### Fase 3: Documentação de Desenvolvedor (16-24 horas)

**Prioridade Alta:**
1. `architecture/overview.md` - Arquitetura geral + diagrama
2. `architecture/data-models.md` - ERD e models
3. `setup/local-development.md` - Setup completo
4. `api-reference/models.md` - Referência models
5. `api-reference/management-commands.md` - Commands
6. `contributing/getting-started.md` - Como contribuir
7. `contributing/code-style.md` - Black, isort, ruff
8. `testing/overview.md` - Estratégia de testes

**Prioridade Média:**
9. `architecture/technology-stack.md` - Stack completo
10. `architecture/search-architecture.md` - TypeSense
11. `architecture/decisions.md` - ADRs
12. `setup/docker-services.md` - Docker Compose
13. `setup/environment-variables.md` - Env vars
14. `api-reference/views.md` - Views e URLs
15. `api-reference/typesense-client.md` - Search API
16. `guides/importing-yaml.md` - Importar YAML
17. `guides/indexing-search.md` - Reindexar
18. `testing/unit-tests.md` - Testes unitários

**Prioridade Baixa:**
19. `deployment/overview.md` - Deploy
20. `deployment/production-setup.md` - Produção
21. `deployment/ci-cd.md` - GitHub Actions
22. `deployment/monitoring.md` - Logs
23. `guides/adding-features.md` - Adicionar features
24. `guides/celery-tasks.md` - Background tasks

### Fase 4: Screenshots e Diagramas (4-6 horas)

**Screenshots necessários (mínimo 15):**
1. Home page
2. Busca vazia (dicas)
3. Resultados de busca
4. Lista de hinários
5. Detalhes de hinário + tabela de hinos
6. Página de hino (letra completa)
7. Login/signup
8. Upload YAML (form)
9. Upload PDF (processo)
10. Player de áudio
11. Comentários
12. Perfil de usuário
13. Notificações
14. Admin Django
15. Admin Wagtail

**Diagramas técnicos:**
1. Arquitetura geral (ASCII + Mermaid)
2. ERD (Entity Relationship Diagram)
3. Fluxo de importação YAML
4. Fluxo de busca TypeSense
5. Fluxo de upload (Fase 2)

**Ferramentas:**
- Screenshots: Navegador + DevTools
- Diagramas: Mermaid.js (renderizados pelo MkDocs)
- ERD: dbdiagram.io ou draw.io

### Fase 5: Revisão e Deploy (2-3 horas)

**Tarefas:**
1. Revisar todos os documentos
2. Verificar links internos
3. Testar navegação completa
4. Gerar site estático (`mkdocs build`)
5. Deploy no GitHub Pages ou Netlify
6. Atualizar README.md com link para docs

**Validação:**
- [ ] Todos os links funcionam
- [ ] Todas as imagens carregam
- [ ] Navegação intuitiva
- [ ] Busca funciona
- [ ] Mobile responsivo
- [ ] Sem erros no build

---

## 📦 Entregáveis

### Estrutura Final

```
hyms-plat/
├── docs/                                    # Toda documentação
│   ├── index.md                            # Landing page
│   ├── user-guide/                         # 12 arquivos
│   ├── developer-guide/                    # 25+ arquivos
│   ├── about.md
│   ├── roadmap.md
│   ├── changelog.md
│   └── images/                             # Screenshots e diagramas
├── mkdocs.yml                              # Configuração MkDocs
├── site/                                   # Site gerado (gitignored)
└── README.md                               # Link para docs
```

### `mkdocs.yml` Exemplo

```yaml
site_name: Portal de Hinários - Documentação
site_description: Documentação completa do Portal de Hinários do Santo Daime
site_url: https://portal-hinarios.com.br/docs/
repo_url: https://github.com/seu-usuario/hyms-plat
repo_name: hyms-plat

theme:
  name: material
  language: pt-BR
  palette:
    - scheme: default
      primary: blue
      accent: light-blue
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

nav:
  - Início: index.md
  - Sobre: about.md
  - Roadmap: roadmap.md

  - Guia do Usuário:
    - user-guide/index.md
    - Primeiros Passos: user-guide/getting-started.md
    - Buscar Hinos: user-guide/searching-hymns.md
    - Navegar Hinários: user-guide/browsing-hymnbooks.md
    - Visualizar Hinos: user-guide/viewing-hymns.md
    - Contas de Usuário: user-guide/user-accounts.md
    - Upload de Hinários: user-guide/uploading-hymnbooks.md
    - Recursos de Áudio: user-guide/audio-features.md
    - Recursos Sociais: user-guide/social-features.md
    - FAQ: user-guide/faq.md
    - Problemas: user-guide/troubleshooting.md

  - Guia do Desenvolvedor:
    - developer-guide/index.md
    - Arquitetura:
      - Visão Geral: developer-guide/architecture/overview.md
      - Stack Tecnológico: developer-guide/architecture/technology-stack.md
      - Models e Schema: developer-guide/architecture/data-models.md
      - Busca TypeSense: developer-guide/architecture/search-architecture.md
      - Decisões (ADRs): developer-guide/architecture/decisions.md
    - Setup:
      - Dev Local: developer-guide/setup/local-development.md
      - Docker Services: developer-guide/setup/docker-services.md
      - Variáveis de Ambiente: developer-guide/setup/environment-variables.md
      - Problemas Comuns: developer-guide/setup/common-issues.md
    - Contribuindo:
      - Como Contribuir: developer-guide/contributing/getting-started.md
      - Code Style: developer-guide/contributing/code-style.md
      - Escrevendo Testes: developer-guide/contributing/testing.md
      - Pull Requests: developer-guide/contributing/pull-requests.md
    - API Reference:
      - Models: developer-guide/api-reference/models.md
      - Views: developer-guide/api-reference/views.md
      - Commands: developer-guide/api-reference/management-commands.md
      - TypeSense Client: developer-guide/api-reference/typesense-client.md
    - Guias:
      - Importar YAML: developer-guide/guides/importing-yaml.md
      - Reindexar Busca: developer-guide/guides/indexing-search.md
      - Adicionar Features: developer-guide/guides/adding-features.md
      - Wagtail CMS: developer-guide/guides/working-with-wagtail.md
    - Deploy:
      - Visão Geral: developer-guide/deployment/overview.md
      - Setup Produção: developer-guide/deployment/production-setup.md
      - CI/CD: developer-guide/deployment/ci-cd.md
      - Monitoramento: developer-guide/deployment/monitoring.md
    - Testes:
      - Visão Geral: developer-guide/testing/overview.md
      - Testes Unitários: developer-guide/testing/unit-tests.md
      - Coverage: developer-guide/testing/coverage.md

  - Changelog: changelog.md

plugins:
  - search:
      lang: pt
  - mermaid2  # Para diagramas

markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:mermaid2.fence_mermaid
  - pymdownx.tabbed
  - pymdownx.details
  - pymdownx.emoji
  - toc:
      permalink: true

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/seu-usuario/hyms-plat
```

---

## ✅ Critérios de Sucesso

### Métricas

| Critério | Meta |
|----------|------|
| **Documentos criados** | 40+ arquivos markdown |
| **Screenshots** | 15+ imagens |
| **Diagramas** | 5+ diagramas técnicos |
| **Cobertura funcional** | 100% das features documentadas |
| **Links internos** | 0 links quebrados |
| **Mobile** | 100% responsivo |
| **Busca** | Funcional e rápida |

### Validação com Usuários

**Teste com 3 personas:**

1. **Usuário final (não-técnico)**
   - Consegue entender como buscar hinos? ✓
   - Consegue visualizar e imprimir letra? ✓
   - Entende como criar conta e contribuir? ✓

2. **Desenvolvedor júnior**
   - Consegue fazer setup local? ✓
   - Entende arquitetura do sistema? ✓
   - Sabe como contribuir com código? ✓

3. **Desenvolvedor sênior**
   - Documentação técnica é precisa? ✓
   - ADRs justificam decisões? ✓
   - Pode fazer deploy em produção? ✓

---

## 🎯 Próximas Ações

### Após Implementação das Fases 2-4

Quando as fases futuras forem implementadas:

1. **Atualizar docs existentes** - Remover avisos "⚠️ Em Desenvolvimento"
2. **Adicionar screenshots reais** - Substituir placeholders
3. **Documentar novas APIs** - Endpoints de upload, áudio, social
4. **Atualizar diagramas** - Incluir novos fluxos
5. **Testar todos os guias** - Validar tutoriais passo-a-passo

### Deploy da Documentação

**Opção 1: GitHub Pages (Recomendado)**
```bash
mkdocs gh-deploy
```
- URL: `https://seu-usuario.github.io/hyms-plat/`
- Automático via GitHub Actions

**Opção 2: Netlify**
- Build command: `mkdocs build`
- Publish directory: `site/`
- Custom domain possível

**Opção 3: ReadTheDocs**
- Integração com GitHub
- Versionamento automático
- Tema próprio

---

## 📚 Referências

### Documentações Inspiradoras

- [Django Docs](https://docs.djangoproject.com/) - Clareza e estrutura
- [FastAPI Docs](https://fastapi.tiangolo.com/) - Exemplos práticos
- [Wagtail Docs](https://docs.wagtail.org/) - Guias e tutoriais
- [Stripe Docs](https://stripe.com/docs) - UX e navegação

### Ferramentas

- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid.js](https://mermaid.js.org/) - Diagramas
- [dbdiagram.io](https://dbdiagram.io/) - ERD

---

**FIM DO PLANO**

Este plano será salvo em `/Users/nitai/Dropbox/dev-mgi/hyms-plat/_plan/plano-documentacao.md` para execução após implementação das Fases 2-4.
