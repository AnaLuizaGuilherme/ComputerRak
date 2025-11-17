# 🧠🎲 ComputerRak — Jogo de Tabuleiro Digital (Computabilidade)

> Plataforma gamificada para apoiar o estudo de **Computabilidade** e **Complexidade de Algoritmos**, utilizando um **tabuleiro digital**, quizzes e provas guiadas.  
> Backend em **FastAPI**, Banco **SQLite**, Frontend em **Streamlit** (planejado) e empacotamento final em **Docker** (planejado).

**Status do Projeto:** Até a **Fase 5** concluída no contexto da disciplina  
- **Fase 1** → Estruturação do repositório + `/health`  
- **Fase 2** → Rotas `/launch` e `/score` com lógica básica de jogo  
- **Fase 3** → Modelo relacional + persistência em **SQLite** + fluxo ponta a ponta (vídeo + mapa mental)  
- **Fase 4** → Ajustes de objetivos, testes funcionais e autenticação simples  
- **Fase 5** → Documentação: README completo, pronto para execução pelo usuário

---

# 🎯 Objetivo Geral do Projeto

Criar um **jogo de tabuleiro digital educacional**, onde o jogador avança casas ao resolver desafios teóricos de computabilidade.  
O projeto tem como foco:

- Transformar conteúdos abstratos (máquinas de Turing, decidibilidade, reduções) em **desafios interativos**.  
- Aproximar teoria e prática por meio de **gamificação**, **feedback imediato** e **organização visual**.  
- Proporcionar ao aluno uma experiência ativa, guiada e motivadora de aprendizagem.

---

# 🎓 Conexão com a Teoria (Fundamentos Aplicados)

A aplicação representa diretamente conceitos centrais da disciplina:

### ✔ Funções computáveis & entrada/saída  
Cada endpoint simula o modelo formal “entrada → processamento → saída”, essencial em Computabilidade.

### ✔ Decidibilidade & verificação  
O backend avalia respostas como *decidíveis* (correto/errado), analogamente a funções de decisão.

### ✔ Reduções e lógica de provas  
Os desafios (fases futuras) terão provas guiadas em passos, espelhando reduções ≤m e demonstrações formais.

### ✔ Modelagem de estados  
Cada sessão (partida) representa um **estado computacional**, evoluindo conforme as ações do usuário.

---

# 🧩 Como o jogo favorece o aprendizado

- Estimula **resolução de problemas**, compreensão de *por que* a resposta está correta.  
- Conecta o aluno à teoria por meio de **exemplos contextualizados** e feedback imediato.  
- Incentiva **aprendizagem ativa**, substituindo leitura passiva por prática guiada.  
- Ajuda a fixar conceitos difíceis com **repetição espaçada** e desafios progressivos.

---

# 🧰 Stack Tecnológica

- **Python 3.11+**  
- **FastAPI + Uvicorn** (backend)  
- **SQLite** (persistência de sessões e tentativas) — **Fase 3**  
- **Streamlit** (frontend/tabuleiro digital) — **planejado para fases seguintes**  
- **Docker** (empacotamento) — **planejado para fase final**  
- **Git/GitHub** (controle de versão)  

---

# 🗂️ Estrutura Atual do Projeto

```text
ComputerRak/
│
├── app/
│   ├── main.py            # Lógica principal da API (health, launch, score, auth, SQLite)
│   ├── __init__.py
│
├── computerrak.db         # Banco SQLite (gerado automaticamente na Fase 3)
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ▶️ Como Rodar o Projeto Localmente

## 1) Clonar o repositório

```bash
git clone https://github.com/AnaLuizaGuilherme/ComputerRak.git
cd ComputerRak
```

## 2) Criar ambiente virtual

```bash
python -m venv venv
```

## 3) Ativar o ambiente virtual

**PowerShell**
```powershell
venv\Scripts\Activate.ps1
```

**Git Bash / Linux**
```bash
source venv/Scripts/activate
# ou
source venv/bin/activate
```

## 4) Instalar dependências

```bash
pip install -r requirements.txt
```

## 5) Rodar o backend

```bash
uvicorn app.main:app --reload
```

API disponível em:

- **http://127.0.0.1:8000**
- Documentação: **http://127.0.0.1:8000/docs**

---

# 🔐 Autenticação (Fase 4)

A partir da fase de consolidação, as rotas de jogo usam um header fixo:

```text
x-api-key: computerrak-dev
```

Sem o token → **401 Unauthorized**

> A rota `/health` é pública para facilitar testes rápidos.

---

# 🌐 Endpoints Implementados

## 🩺 GET `/health`

Verifica se o serviço está no ar.

Exemplo de resposta:

```json
{ "status": "ok", "service": "computerrak-api" }
```

---

## 🎮 POST `/launch`

Inicia uma nova sessão (partida) e registra no SQLite.

### Exemplo de request:

```json
{ "user": "ana" }
```

### Exemplo de response:

```json
{
  "session_id": "uuid",
  "position": 0,
  "score": 0,
  "message": "partida iniciada"
}
```

---

## 🧠 POST `/score`

Registra uma resposta do jogador, calcula pontos e atualiza o score da sessão.

### Exemplo de request:

```json
{
  "session_id": "uuid",
  "payload_id": "q_001",
  "answer": 1
}
```

### Exemplo de response:

```json
{
  "delta": 10,
  "score": 10,
  "explanation": "Mestre: a=b=2, f(n)=n ⇒ caso 2 ⇒ O(n log n).",
  "correct": true
}
```

> Na Fase 3, esse fluxo foi demonstrado em vídeo, incluindo consulta ao banco (`sessions` e `attempts`) e mapa mental da execução ponta a ponta.

---

# 🗄️ Banco de Dados (Fase 3)

O **modelo relacional** simplificado é:

## Tabela `sessions`
- `id_sessao` (PK)  
- `user`  
- `position`  
- `score`  
- `created_at`  

## Tabela `attempts`
- `id_attempt` (PK)  
- `id_sessao` (FK → sessions.id_sessao)  
- `payload_id`  
- `answer`  
- `delta`  
- `created_at`  

Na Fase 3 foram:

- Definidas as entidades e relacionamentos.  
- Implementadas as `CREATE TABLE` em SQLite.  
- Gravadas sessões e tentativas durante o fluxo `/launch` → `/score`.  
- Registrados evidências (vídeo + mapa mental) mostrando a consulta ao banco.

---

# 🧪 Testes Funcionais (Fase 4)

Principais cenários executados e validados:

| Cenário | Resultado esperado | Status |
|--------|--------------------|--------|
| `/health` sem token | 200 OK | ✅ |
| `/launch` com token válido | 200 + sessão criada em `sessions` | ✅ |
| `/launch` sem token | 401 Unauthorized | ✅ |
| `/score` com `session_id` válido e resposta correta | 200 + score atualizado + registro em `attempts` | ✅ |
| `/score` com `session_id` inválido | 400 Bad Request (`session_id inválido`) | ✅ |
| `/score` sem token | 401 Unauthorized | ✅ |

Esses testes garantem a consistência entre os objetivos do jogo e a implementação técnica.

---

# 🧪 Exemplos via curl

## Criar partida (Fase 2+)

```bash
curl -X POST "http://127.0.0.1:8000/launch" -H "x-api-key: computerrak-dev" -H "Content-Type: application/json" -d "{\"user\":\"ana\"}"
```

## Registrar resposta (Fase 2+)

```bash
curl -X POST "http://127.0.0.1:8000/score" -H "x-api-key: computerrak-dev" -H "Content-Type: application/json" -d "{\"session_id\":\"ID\",\"payload_id\":\"q_001\",\"answer\":1}"
```

---

# 📌 Convenção de Branches

- `main` → versão estável  
- `dev` → integração contínua  
- `feat/<nome>` → novas funcionalidades  
- `docs/<descricao>` → alterações na documentação  

Commits seguem a ideia de **Conventional Commits** (ex.: `feat: adiciona rota /score`).

---

# 🛣️ Roadmap — Fases do Projeto

### **Fase 1 — Repositório e Healthcheck**
- Estrutura base do projeto  
- Configuração do GitHub  
- FastAPI com `/health` respondendo `"ok"`  

### **Fase 2 — Regras básicas do jogo**
- Implementação das rotas `/launch` e `/score` com lógica básica  
- Mock de desafios de computabilidade  
- Primeira versão do fluxo de jogo (sem banco)

### **Fase 3 — Modelo Relacional e Banco de Dados**
- Desenho do modelo relacional (JSON/DER)  
- Criação do **SQLite** com tabelas `sessions` e `attempts`  
- Implementação da persistência real nas rotas  
- Vídeo + mapa mental demonstrando o fluxo ponta a ponta

### **Fase 4 — Ajustes de Objetivos, Autenticação e Testes**
- Revisão dos objetivos do projeto e conexão explícita com os fundamentos teóricos  
- Inclusão de autenticação simples por token fixo (`x-api-key`)  
- Execução e registro de testes funcionais do sistema

### **Fase 5 — Documentação e Preparação para Execução**
- Completar e revisar o `README.md`  
- Detalhar instalação, dependências, token, rotas e exemplos de uso  
- Preparar o projeto para ser executado por qualquer usuário sem conhecimento prévio do código

### **Fase 6 — Próximos Passos (fora do escopo obrigatório, mas planejados)**
- Frontend em **Streamlit** com tabuleiro visual  
- Empacotamento em **Docker**  
- Ajustes finais, testes adicionais e apresentação estendida

---

# 🛠️ Debug / Problemas Comuns

| Problema | Possível causa | Solução |
|---------|----------------|---------|
| venv não ativa (Windows) | Política de execução do PowerShell | Abrir como admin e rodar `Set-ExecutionPolicy RemoteSigned` |
| Porta 8000 em uso | Outro serviço ocupando a porta | Rodar `uvicorn app.main:app --reload --port 8001` |
| `session_id inválido` no `/score` | ID não veio de um `/launch` válido | Criar sessão via `/launch` e reutilizar o `session_id` retornado |
| 401 Unauthorized | Token ausente ou errado | Conferir header `x-api-key: computerrak-dev` |

---

# 👥 Integrantes

- **Ana Luiza Guilherme** — 33911410 — analuizaguilher0@gmail.com  
- **Kayky Mourão de Oliveira** — 33579016 — kaykyoliveiramourao2004@gmail.com  
- **Rafael de Albuquerque Tavares** — 34225013 — rafaelalbuquerquetavares123@gmail.com  

---

# 📄 Licença

Este projeto poderá adotar licença **MIT**.

---

# 🎉 Considerações Finais

O *ComputerRak* surge como uma ponte entre teoria e prática, tornando Computabilidade mais acessível, visual e interativa.  
O jogo transforma conteúdos historicamente complexos em desafios progressivos que estimulam **autonomia, lógica e raciocínio estruturado**, alinhando-se às fases propostas na disciplina até a Fase 5, com código, banco de dados e documentação prontos para uso.
