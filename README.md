# Computer Rak — Jogo de Tabuleiro Digital (Computabilidade)

> Jogo de tabuleiro digital para apoiar o estudo de **Computabilidade**.  
> O jogador avança casas e resolve **quizzes** e **provas guiadas** (ordenar passos de provas/reduções).

**Status:** Fase **1/6** — preparar repositório e validar o endpoint `/health`.

---

## 🎯 Objetivo do Projeto

Criar um plugin/jogo com **backend em FastAPI** e **frontend em Streamlit** (a partir da Fase 2).

Na **Fase 1**, garantir que o serviço está no ar via rota `/health` e documentar como rodar localmente.

---

## 🧰 Stack Utilizada

- **Linguagem:** Python 3.11+
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit (a partir da Fase 2)
- **Banco:** SQLite (a partir da Fase 3)
- **Controle de versão:** Git/GitHub
- **Empacotamento:** Docker (Fase 5)

---

## 🗂️ Estrutura Inicial do Projeto

```
algoboard/
├─ app/
│  └─ main.py           # FastAPI com /health
├─ requirements.txt     # deps da Fase 1
├─ .gitignore
└─ README.md
```

**`app/main.py` (mínimo da Fase 1)**

```python
from fastapi import FastAPI

app = FastAPI(title="AlgoBoard API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "algoboard-api"}
```

**`requirements.txt` (Fase 1)**

```
fastapi
uvicorn[standard]
```

**`.gitignore` (essencial)**

```
venv/
__pycache__/
*.sqlite
.env
```

---

## ▶️ Como Rodar Localmente

1) **Clonar o repositório**
```bash
git clone <URL_DO_SEU_REPO> algoboard
cd algoboard
```

2) **Criar e ativar ambiente virtual**

**Windows (PowerShell)**
```powershell
python -m venv venv
.env\Scriptsctivate
```

**Linux/Mac**
```bash
python -m venv venv
source venv/bin/activate
```

3) **Instalar dependências**
```bash
pip install -r requirements.txt
```

4) **Subir o servidor FastAPI (dev)**
```bash
uvicorn app.main:app --reload
```

O serviço ficará acessível em: **http://127.0.0.1:8000**

---

## 🩺 Testar o endpoint `/health`

**Curl (Linux/Mac)**
```bash
curl -s http://127.0.0.1:8000/health
```

**PowerShell (Windows)**
```powershell
irm http://127.0.0.1:8000/health
```

**Resposta esperada (HTTP 200)**
```json
{ "status": "ok", "service": "algoboard-api" }
```

---

## 🧩 Escopo Pedagógico (resumo)

**Conteúdo:** Computabilidade (decidibilidade, RE/co-RE, reduções ≤m, Teorema de Rice, PCP, diagonalização).

**Tipos de desafio do jogo (a partir da Fase 2):**
- **Quiz** (múltipla escolha com explicação).
- **Prova guiada** (ordenar 5–7 passos de uma prova/redução).

---

## ✅ Checklist da Fase 1

- [x] Projeto no GitHub  
- [x] `.gitignore` e `requirements.txt`  
- [x] Ambiente virtual criado e ativado  
- [x] Servidor FastAPI rodando localmente  
- [x] `/health` respondendo `{"status":"ok"}`  
- [x] README com objetivo, stack, estrutura e passos de execução  

---

## 👥 Integrantes do Grupo

- Ana Luiza Guilherme — 33911410 / analuizaguilher0@gmail.com  
- Kayky Mourão de Oliveira — 33579016 / kaykyoliveiramourao2004@gmail.com   
- Rafael de Albuquerque Tavares — 34225013 / rafaelalbuquerquetavares123@gmail.com

---

## 🔀 Convenção de Branches (sugestão)

- `main` — estável / releases  
- `dev` — integração contínua  
- `feat/<nome-da-feature>` — novas funcionalidades  
- `docs/<ajuste-de-docs>` — alterações de documentação  

> Dica: adote **Conventional Commits** (ex.: `feat: adiciona endpoint /launch`).

---

## 📦 Roadmap — Próximas Fases

- **Fase 2:** `/launch` e `/score`, tabuleiro no Streamlit e desafio *mock*  
- **Fase 3:** SQLite, persistência de sessões/score  
- **Fase 4:** Integração fina, auth simples, desafios reais  
- **Fase 5:** Docker + relatório pedagógico  
- **Fase 6:** Testes finais e apresentação  

---

## 🛠️ Solução de Problemas (rápido)

- **Uvicorn não inicia / porta em uso:** finalize processos na porta 8000 ou rode com `--port 8001`.  
- **Ambiente virtual não ativa (Windows):** execute o PowerShell como Admin e rode `Set-ExecutionPolicy RemoteSigned`.  
- **Dependências faltando:** confira `pip -V` (usa o Python do `venv`?) e reinstale `pip install -r requirements.txt`.

---

## 📄 Licença

Definir (ex.: MIT).
