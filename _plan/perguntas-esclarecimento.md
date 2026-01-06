# Perguntas de Esclarecimento - Portal de Hinários

## Estrutura de Dados

1. **Formato YAML**: Qual é a estrutura exata do arquivo YAML? Quais campos são obrigatórios vs opcionais para hinário e hino?

2. **Identificador único de hino**: Como identificar univocamente um hino entre diferentes versões? Existe um código/número tradicional, ou usa-se o título?

3. **Versionamento**: Como determinar se dois PDFs são "versões do mesmo hinário" vs "hinários diferentes"? Qual critério de desambiguação?

## Sistema de Áudio

4. **Formatos de áudio**: Quais formatos serão aceitos (MP3, M4A, WAV, etc.)?

5. **Áudio por hino ou por hinário**: O áudio será por hino individual ou por hinário completo (ou ambos)?

6. **Sincronização**: Haverá sincronização entre áudio e texto (tipo karaokê), ou apenas vinculação simples?

## Usuários e Permissões

7. **Autenticação**: Qual provider de autenticação usar (Google, email/senha, etc.)?

8. **Moderação**: Quem pode aprovar/rejeitar uploads? Haverá moderação ou é livre?

9. **Edição**: O dono de um hinário pode editar/remover versões que outros subiram?

10. **Notificações**: Como serão enviadas as notificações (email, push, in-app)?

## Upload e Processamento

11. **Limites**: Qual tamanho máximo de arquivo PDF/áudio?

12. **Processamento de PDF**: O sistema deve extrair o texto do PDF automaticamente (OCR) ou usuário cola o texto?

13. **Metadados obrigatórios**: Quais metadados são obrigatórios no upload (título, autor, data, igreja, etc.)?

## Navegação e Busca

14. **Categorias fixas**: Quais categorias de organização além de época e autor?

15. **Favoritos**: Usuários podem marcar hinários/hinos como favoritos?

16. **Listas personalizadas**: Usuários podem criar listas/playlists de hinos?

## Técnico

17. **Stack tecnológico**: Há preferência por linguagem/framework (Python, Node, etc.)?

18. **Hospedagem**: Onde será hospedado (GCP, AWS, Vercel, etc.)?

19. **Storage**: Onde armazenar os PDFs e áudios (GCS, S3, etc.)?

20. **MVP**: Quais funcionalidades são essenciais para a primeira versão vs futuras?
