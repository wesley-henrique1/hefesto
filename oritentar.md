# Hefesto — Documentação do Projeto

## 🏗️ Arquitetura do Sistema (Back-end)
* **Estrutura de Diretórios:** Organização modular para separar interface, regras de negócio e persistência de dados.
* **Armazenamento:** **SQLite** (`hefesto_config.db`) para controle centralizado de pipelines, configurações, paths, módulos, bots e tarefas diárias.

---

## 🖥️ Front-End (Interface Gráfica)

### 1. Tela Principal
A interface principal está dividida nos seguintes blocos de controle e monitoramento:
* **Quadro de Botões:** Atalhos de ação rápida para o operador.
* **Quadro de Pipelines:** Listagem em tempo real dos pipelines ativos, controlada via SQLite e exibida com flags de status.
* **Quadro de Arquivos Usados:** Monitoramento dos arquivos manipulados pelos pipelines (`Nome` | `Data de Modificação`).
* **Progresso:** Indicador visual composto por contador e etapa atual.

#### 🎛️ Detalhes do Quadro de Botões
* `Iniciar Pipelines`: Executa os fluxos de trabalho ativos.
* `bt_bot`: Abre o painel de gerenciamento de bots.
* `Configuração`: Acessa o menu de parâmetros do sistema.
* `Demandas do Dia`: Visualização rápida das tarefas pendentes e concluídas.

---

### 2. Telas Secundárias (`Toplevel`)

* **Iniciar:** Executa as rotinas e pipelines ativos em background.
* **`bt_bot`:** Exibe uma janela dedicada com botões de referência interativos para cada bot ativo no sistema.
* **Configuração:** Painel de gerenciamento completo contendo as seguintes ações:
  * `Flags`: Ativação/desativação de parâmetros e estados.
  * `Cadastrar`: Inserção de novos *Paths*, *Módulos*, *Bots* ou *Tarefas*.
  * `Editar`: Atualização de registros existentes.
  * `Apagar`: Remoção de itens do banco de dados.
* **Demandas do Dia:** Painel de acompanhamento de tarefas para controle diário (pendentes vs. realizadas).
