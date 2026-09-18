# GSP — Gestão de Seguros Prestamista

Sistema web moderno, rápido e 100% responsivo para controle, gestão e acompanhamento de resgates de seguros prestamistas, comissões, parceiros e agendamento de retornos.

---

## 🌟 Principais Recursos

* **Dashboard Financeiro em Tempo Real**:
  * Total de clientes cadastrados;
  * Valor total de seguros administrados;
  * Pendências líquidas a receber (deduzindo valores já pagos);
  * Total já recebido.

* **Cadastro e Edição Completa de Clientes**:
  * **Dados do Cliente**: Nome completo, contato/WhatsApp com máscara automática, bairro e lotação de trabalho.
  * **Origem e Gestão**: Consultor, Secretaria, Empresa Responsável (todos com opção de adicionar novos via botão `+` diretamente na tela).
  * **Clientes Compartilhados**: Seletor Sim/Não com bloqueio inteligente de campos de parceiro e comissão caso o cliente não seja compartilhado.
  * **Seguro e Banco**: Seleção de tipo de seguro (+ cadastro dinâmico) e vínculo de banco individual com pesquisa rápida.
  * **Cálculo Automático**: Cálculo imediato do valor líquido a receber com base na porcentagem pactuada.

* **Acompanhamento de Status e Agendamentos de Retorno**:
  * Status: `AGUARDANDO RETORNO`, `FALARÁ COMIGO NA DATA`, `FECHADO` e `CARÊNCIA` (+ opção de novos).
  * **Destaques de Proximidade**: Alertas visuais coloridos para datas de contato (🔴 Atrasado, 🟠 LIGAR HOJE com efeito pulsante, 🟡 Próximo).
  * **Lembrete via WhatsApp**: Botão que abre o WhatsApp diretamente com mensagem profissional personalizada pronta para envio no dia do retorno.
  * **Fluxo de Fechamento**: Ao marcar como `FECHADO`, registra automaticamente a data e questiona se houve pagamento prévio.

* **Importação, Exportação e Limpeza de Dados**:
  * **Importação Inteligente (Excel e CSV)**: Reconhece a coluna `VALOR` e extrai a porcentagem de comissão diretamente da coluna `OBSERVAÇÃO`.
  * **Botão Desfazer Importação**: Caso você carregue uma planilha errada, permite reverter a ação imediatamente em 1 clique sem afetar os dados anteriores.
  * **Botão Limpar Todos os Dados**: Permite apagar rapidamente todos os registros do histórico com confirmação de segurança.
  * **Exportação**: Gera relatórios em `.xlsx` (Excel) ou `.csv`.
  * **Backup Completo em JSON**: Permite salvar e restaurar em 1 clique todos os clientes e listas personalizadas criadas pelo usuário.

---

## 🚀 Como Executar Localmente

Basta abrir o arquivo [`index.html`](index.html) em qualquer navegador moderno (Google Chrome, Microsoft Edge, Firefox, Brave, etc.). Não é necessário instalar Node.js, banco de dados ou servidores.

---

## 🌐 Como Publicar Gratuitamente no GitHub Pages

Para ter um link público na internet (ex.: `https://seu-usuario.github.io/seu-repositorio`):

1. Crie um repositório no seu [GitHub](https://github.com/new).
2. Envie os arquivos desta pasta (`index.html`, `README.md`, etc.).
3. No repositório, clique na aba **Settings** (Configurações).
4. No menu lateral esquerdo, clique em **Pages**.
5. Em **Branch**, selecione `main` (ou `master`) e a pasta `/(root)`.
6. Clique em **Save**.
7. Em cerca de 1 minuto, o GitHub fornecerá o link público do seu sistema!
