# Portal de Hinários - Requisitos

## Visão Geral
Portal para pesquisa e acesso a hinários do Santo Daime.

**Stack Tecnológico:** Django + Wagtail
**Abordagem:** MVP incremental (leitura primeiro, upload depois)

---

## Requisitos Funcionais

### RF01 - Gerenciamento de Hinários

#### RF01.1 - Upload de Hinários [Fase 2]
- Usuários devem poder fazer upload de hinários em formato PDF e/ou YAML
- O sistema deve extrair e indexar o conteúdo
- **Desambiguação de hinários:**
  - Se nome igual: alta probabilidade de ser o mesmo hinário
  - Se nome diferente: análise de proximidade semântica (TypeSense com/sem embeddings)
  - Comparação de textos dos hinos para identificar duplicidades
  - **UI deve sugerir fortemente selecionar nome existente antes de criar novo**
  - Fluxo: busca → sugestões → confirmação → upload

#### RF01.2 - Download de Hinários [Fase 1]
- Usuários devem poder baixar hinários em PDF
- Suporte para uso offline (celular, impressão)

#### RF01.3 - Múltiplas Versões [Fase 2]
- O sistema deve suportar múltiplas versões do mesmo hinário
- Manter vinculação entre versões diferentes do mesmo hinário
- Visualização de todas as versões de um mesmo hinário

### RF02 - Gerenciamento de Áudio [Fase 3]

#### RF02.1 - Upload de Áudio
- Usuários devem poder fazer upload de versões de áudio dos hinos
- Identificar variações de como um mesmo hino é cantado

#### RF02.2 - Vinculação Áudio-Texto
- Vincular áudio a uma versão específica do texto (PDF)
- Um áudio pode referenciar qualquer versão do hinário/texto

### RF03 - Sistema de Usuários

#### RF03.1 - Tipos de Usuário
- **Usuário Anônimo**: acesso público de leitura [Fase 1]
- **Usuário Autenticado**: download, upload, recursos avançados [Fase 2]
- **Dono de Hinário**: usuário vinculado como proprietário de hinários [Fase 2]

#### RF03.2 - Perfil de Dono de Hinário [Fase 2]
- Metadado do hinário deve incluir o "dono" (quem recebeu o hinário)
- Se o dono tiver cadastro, deve estar vinculado ao perfil
- Página do usuário mostrando todos os seus hinários
- Navegação entre hinários do mesmo dono

#### RF03.3 - Sistema de Seguir [Fase 3]
- Usuários podem seguir donos de hinários
- Notificações quando o dono publica novos hinos (texto ou áudio)

### RF04 - Busca e Navegação

#### RF04.1 - Barra de Busca [Fase 1]
- Busca full-text em todos os hinos
- Usar TypeSense para indexação
- Sugestões de autocompletar

#### RF04.2 - Navegação por Categorias [Fase 1]
- Página listando todos os hinários
- Categorização por autor/dono
- Categorização por época
- Menu lateral com hinários (referência: santodaime.org)

#### RF04.3 - Visualização de Hinário [Fase 1]
- Visualização do conteúdo no navegador
- Sequência de hinos com navegação
- Download do PDF

### RF05 - Moderação [Fase Futura]
- Upload inicialmente livre (sem moderação)
- Sistema de moderação a ser definido posteriormente

---

## Requisitos Não-Funcionais

### RNF01 - Acesso Aberto
- Maximizar conteúdo público (sem autenticação)
- Autenticação apenas onde estritamente necessário
- Todos os dados e informações devem ser abertos para qualquer pessoa

### RNF02 - Plataformas
- Versão web (navegador)
- Suporte a dispositivos móveis (responsive)
- Suporte multi-idioma (referência: PT, EN, ES, DE, FR, IT, NL, JP)

### RNF03 - Qualidade de Código
- **Cobertura de testes automatizados abrangente**
- Testes unitários para models e services
- Testes de integração para APIs
- Testes end-to-end para fluxos críticos
- CI/CD com execução automática de testes

### RNF04 - Performance
- Indexação eficiente com TypeSense
- Carregamento rápido de PDFs
- Cache de buscas frequentes

---

## Estrutura de Dados

### Formato YAML (Referência)
Baseado em: https://github.com/nitaibezerra/hymn_pdf_generator/blob/main/example/selecao_aniversario_ingrid.yaml

```yaml
hymn_book:
  intro_name: "Nome curto"           # Nome de exibição
  name: |                            # Título completo (multi-linha)
    Título do Hinário
  owner: "Nome do Dono"              # Pessoa que recebeu
  cover_image_path: "capa.jpg"       # Imagem de capa
  hymns:                             # Lista de hinos
    - number: 1                      # Número sequencial
      title: "Título do Hino"        # Nome do hino
      text: |                        # Letra (multi-linha)
        Verso 1
        Verso 2
      received_at: 2024-01-15        # Data de recebimento
      offered_to: "Pessoa"           # Dedicatória (opcional)
      style: "Valsa"                 # Estilo musical (opcional)
      extra_instructions: "..."      # Instruções (opcional)
      repetitions: "1-4, 5-8"        # Repetições (opcional)
```

### Entidades Django

#### HymnBook (Hinário)
- `id`: UUID
- `name`: CharField (único para desambiguação)
- `intro_name`: CharField
- `owner_name`: CharField (texto livre)
- `owner_user`: ForeignKey(User, nullable)
- `cover_image`: ImageField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

#### Hymn (Hino)
- `id`: UUID
- `hymn_book`: ForeignKey(HymnBook)
- `number`: IntegerField
- `title`: CharField
- `text`: TextField
- `received_at`: DateField (nullable)
- `offered_to`: CharField (nullable)
- `style`: CharField (nullable)
- `extra_instructions`: TextField (nullable)
- `repetitions`: CharField (nullable)

#### HymnBookVersion (Versão de Hinário)
- `id`: UUID
- `hymn_book`: ForeignKey(HymnBook)
- `version_name`: CharField
- `pdf_file`: FileField
- `uploaded_by`: ForeignKey(User)
- `created_at`: DateTimeField

#### HymnAudio (Áudio de Hino) [Fase 3]
- `id`: UUID
- `hymn`: ForeignKey(Hymn)
- `audio_file`: FileField
- `hymn_book_version`: ForeignKey(HymnBookVersion, nullable)
- `uploaded_by`: ForeignKey(User)
- `created_at`: DateTimeField

---

## Referências Externas

1. **Estrutura YAML**: https://github.com/nitaibezerra/hymn_pdf_generator/blob/main/example/selecao_aniversario_ingrid.yaml
2. **Portal de Referência**: https://hinos.santodaime.org/acervo/introducao
   - Menu lateral com 28+ hinários
   - Organização por compositor/dono
   - Suporte multi-idioma
   - Links para áudio (Soundcloud)

---

## Decisões Técnicas

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Framework | Django + Wagtail | CMS robusto, admin poderoso |
| Busca | TypeSense | Full-text + embeddings para desambiguação |
| Storage | A definir | GCS ou S3 para PDFs/áudios |
| Deploy | A definir | - |
| Auth | Django Auth | Integrado ao Wagtail |
