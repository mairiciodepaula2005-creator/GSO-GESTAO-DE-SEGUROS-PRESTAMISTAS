# Configuração de acesso protegido

Projeto Firebase: gsp---gerenciador-de-seg. Manter plano Spark, sem habilitar faturamento.

## Acesso

A conta proprietária confirmada é mairiciodepaula2005@gmail.com.
O aplicativo exige Google, e-mail verificado e igualdade com a conta configurada.
As regras em database.rules.json fazem a mesma verificação no servidor, sem
condição de data ou prazo de 30 dias. O bloqueio da interface não substitui regras.

## Publicação

Repositório: https://github.com/mairiciodepaula2005-creator/GSO-GESTAO-DE-SEGUROS-PRESTAMISTAS
Site confirmado pelo GitHub Pages:
https://mairiciodepaula2005-creator.github.io/GSO-GESTAO-DE-SEGUROS-PRESTAMISTAS/
Branch main, diretório raiz, HTTPS obrigatório.

Arquivos necessários juntos: index.html, gsp-access.js e gsp-sync.js.
O domínio mairiciodepaula2005-creator.github.io foi adicionado ao Authentication;
o provedor Google foi ativado. Não usar file:// para testar login.
As regras restritas precisam ser publicadas na mesma janela de manutenção da
nova versão do site. Não publicar as regras isoladamente com a versão antiga.

## Preservação dos dados

Foi preservado backup local validado de 2695 clientes na pasta backups,
excluída de publicações pelo .gitignore. Não enviar backups, contatos ou prévias
de importação a um repositório público. Remover o arquivo de dados do estado
atual do Git não apaga versões anteriores nem cópias já baixadas.

A abertura do site novo não envia cache legado à nuvem. A leitura inicial,
mesmo de banco vazio, não grava nada. A transação de salvamento compara o banco
com o estado carregado e aborta em caso de conflito com outra aba ou dispositivo.
Metadados e opções adicionais do banco são preservados. Renderizar filtros não
modifica datas antigas automaticamente.

O aplicativo bloqueia edição quando detecta desconexão. Uma gravação iniciada
pode aguardar reconexão; aguardar a confirmação antes de fechar a aba. Em erro,
a tentativa permanece em memória e pode ser baixada antes de recarregar. Não há
mesclagem automática de conflitos. O cache legado permanece intacto.

## Verificação

Executar node --test tests/sync.test.cjs. Os 13 testes isolados passaram, incluindo
negação de outra conta, e-mail não verificado e provedor diferente; prevenção de
sobrescrita e de envio automático de cache; preservação de datas e confirmação
real de salvamento pelo banco simulado.

Ainda é necessária verificação no ambiente publicado: login pessoal do
proprietário, leitura dos registros preservados, rejeição de usuário sem login
e gravação de um registro fictício isolado com posterior remoção. Os testes
simulados não comprovam OAuth ou regras publicadas.

## Referências oficiais

- https://firebase.google.com/docs/auth/web/google-signin
- https://firebase.google.com/docs/database/web/read-and-write
- https://firebase.google.com/docs/database/security/rules-conditions
- https://firebase.google.com/pricing
