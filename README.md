# ComputerRak — Jogo de Tabuleiro Digital (Computabilidade)

> Plataforma gamificada para apoiar o estudo de **Computabilidade** e **Complexidade de Algoritmos**, utilizando um **tabuleiro digital**, quizzes e provas guiadas.  
> Backend em **FastAPI**, Banco **SQLite**, Frontend em **Streamlit** (planejado) e empacotamento final em **Docker** (planejado).

**Status do Projeto:** Até a **Fase 6** concluída no contexto da disciplina  
- **Fase 1** → Estruturação do repositório + `/health`  
- **Fase 2** → Rotas `/launch` e `/score` com lógica básica de jogo  
- **Fase 3** → Modelo relacional + persistência em **SQLite** + fluxo ponta a ponta (vídeo + mapa mental)  
- **Fase 4** → Ajustes de objetivos, testes funcionais e autenticação simples  
- **Fase 5** → Documentação: README completo, pronto para execução pelo usuário
- **Fase 6** → Inserção da interface

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

# Como o jogo favorece o aprendizado

- Estimula **resolução de problemas**, compreensão de *por que* a resposta está correta.  
- Conecta o aluno à teoria por meio de **exemplos contextualizados** e feedback imediato.  
- Incentiva **aprendizagem ativa**, substituindo leitura passiva por prática guiada.  
- Ajuda a fixar conceitos difíceis com **repetição espaçada** e desafios progressivos.

---

# Stack Tecnológica

- **Python 3.11+**  
- **FastAPI + Uvicorn** (backend)  
- **SQLite** (persistência de sessões e tentativas) — **Fase 3**
- **HTML** (frontend/tabuleiro digital)
- **Streamlit** (frontend/tabuleiro digital) — **planejado para fases seguintes**  
- **Docker** (empacotamento) — **planejado para fase final**  
- **Git/GitHub** (controle de versão)  

---

# 🗂️ Estrutura Atual do Projeto

```text
.
├── .github/
│   └── instructions/
│       └── codacy.instructions.md
│
├── .vscode/
│   └── settings.json
│
├── app/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── computerak.db                     # Banco SQLite (gerado automaticamente na Fase 3)
│   └── main.py                           # Lógica principal da API (health, launch, score, auth, SQLite)
│
├── venv/
│   ├── etc/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── share/
│   └── pyvenv.cfg
│
├── .gitignore
├── bd.json
├── computerak.db
├── EXAM_BANK.json
├── FACT_BANK.json
├── index.html
├── LICENSE
├── QUIZ_BANK.json
├── README.md
├── Relatorio_ComputerRak.md
└── Relatorio-Pedagogico-ComputerRak.md
```

---

# Como Rodar o Projeto Localmente

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

# Roadmap — Fases do Projeto

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

### **Fase 6  — Implementação da Interface
- Frontend em **HTML** com tabuleiro visual
  
### **Fase 7 — Próximos Passos (fora do escopo obrigatório, mas planejados)**
- Frontend em **Streamlit** com tabuleiro visual  
- Empacotamento em **Docker**  
- Ajustes finais, testes adicionais e apresentação estendida

---

#  Debug / Problemas Comuns

| Problema | Possível causa | Solução |
|---------|----------------|---------|
| venv não ativa (Windows) | Política de execução do PowerShell | Abrir como admin e rodar `Set-ExecutionPolicy RemoteSigned` |
| Porta 8000 em uso | Outro serviço ocupando a porta | Rodar `uvicorn app.main:app --reload --port 8001` |
| `session_id inválido` no `/score` | ID não veio de um `/launch` válido | Criar sessão via `/launch` e reutilizar o `session_id` retornado |
| 401 Unauthorized | Token ausente ou errado | Conferir header `x-api-key: computerrak-dev` |

---

#  Integrantes

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
