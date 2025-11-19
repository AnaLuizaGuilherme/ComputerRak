"""
ComputerRak API — Backend do jogo de tabuleiro de Computabilidade.

- Serve o tabuleiro HTML na raiz (/)
- Gerencia sessões com SQLite
- Carrega QUIZ_BANK, EXAM_BANK e FACT_BANK de arquivos JSON "estilo Python"
- Fornece desafios (quiz/prova/fact) via /next_challenge
- Corrige respostas via /score e acumula pontuação
"""
from __future__ import annotations

from uuid import uuid4
import sqlite3
import json
import random
import ast
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -------------------------------------------------------------------
# Caminhos de arquivos
# -------------------------------------------------------------------

# Este arquivo fica em app/main.py, então BASE_DIR é a pasta raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "computerrak.db"
INDEX_PATH = BASE_DIR / "index.html"
QUIZ_PATH = BASE_DIR / "QUIZ_BANK.json"
EXAM_PATH = BASE_DIR / "EXAM_BANK.json"
FACT_PATH = BASE_DIR / "FACT_BANK.json"


# -------------------------------------------------------------------
# Utilitário para carregar bancos com sintaxe:
#   VAR_NAME = [ { ... }, ... ]
# ou JSON puro.
# -------------------------------------------------------------------
def load_bank(path: Path, var_name: str) -> list:
    if not path.exists():
        print(f"[AVISO] Arquivo não encontrado: {path}. Usando lista vazia.")
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        print(f"[AVISO] Arquivo vazio: {path}.")
        return []

    try:
        # Caso seja JSON puro começando com [ ou {
        if text[0] in "[{":
            return json.loads(text)

        # Caso seja VAR_NAME = [...]
        # Usamos AST para localizar o valor da variável
        module = ast.parse(text, mode="exec")
        for node in module.body:
            if isinstance(node, ast.Assign):
                if (
                    len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == var_name
                ):
                    value = ast.literal_eval(node.value)
                    if isinstance(value, list):
                        return value
                    else:
                        print(f"[AVISO] {path}: valor de {var_name} não é lista.")
                        return []
        print(f"[AVISO] {path}: não encontrou atribuição para {var_name}.")
        return []
    except Exception as exc:
        print(f"[ERRO] Falha ao carregar {path}: {exc}")
        return []


QUIZ_BANK = load_bank(QUIZ_PATH, "QUIZ_BANK")
EXAM_BANK = load_bank(EXAM_PATH, "EXAM_BANK")
FACT_BANK = load_bank(FACT_PATH, "FACT_BANK")

print(f"[INFO] QUIZ_BANK carregado com {len(QUIZ_BANK)} itens.")
print(f"[INFO] EXAM_BANK carregado com {len(EXAM_BANK)} provas.")
print(f"[INFO] FACT_BANK carregado com {len(FACT_BANK)} fatos/dicas.")

# -------------------------------------------------------------------
# Mapa de payloads -> informação de correção (para /score)
# -------------------------------------------------------------------

PAYLOADS: Dict[str, Dict[str, object]] = {}

# Quizzes (uma questão)
for q in QUIZ_BANK:
    pid = q.get("id")
    if not pid:
        continue
    PAYLOADS[pid] = {
        "kind": "quiz",
        "correct_index": q.get("correct_index"),
        "explanation": q.get("explanation", ""),
        "points": q.get("points", 10),
    }

# Questões dentro das provas
for exam in EXAM_BANK:
    for q in exam.get("questions", []):
        pid = q.get("id")
        if not pid:
            continue
        PAYLOADS[pid] = {
            "kind": "exam_question",
            "correct_index": q.get("correct_index"),
            "explanation": q.get("explanation", ""),
            "points": q.get("points", 10),
        }


def get_payload_info(payload_id: str) -> Dict[str, object]:
    info = PAYLOADS.get(payload_id)
    if not info:
        raise HTTPException(status_code=400, detail="payload_id desconhecido")
    if info.get("correct_index") is None:
        raise HTTPException(
            status_code=500, detail="payload sem gabarito configurado"
        )
    return info


# -------------------------------------------------------------------
# DB
# -------------------------------------------------------------------
def get_conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    # Tabela de sessões (partidas)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id_sessao TEXT PRIMARY KEY,
            user TEXT NOT NULL,
            position INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    # Tabela de tentativas (respostas)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attempts (
            id_attempt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sessao TEXT NOT NULL,
            payload_id TEXT NOT NULL,
            answer INTEGER NOT NULL,
            delta INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_sessao) REFERENCES sessions(id_sessao)
        );
        """
    )
    conn.commit()
    conn.close()


init_db()

# -------------------------------------------------------------------
# Pydantic models
# -------------------------------------------------------------------
class LaunchReq(BaseModel):
    user: str


class LaunchResp(BaseModel):
    session_id: str
    position: int
    score: int
    message: str


class ScoreReq(BaseModel):
    session_id: str
    payload_id: str
    answer: int  # índice marcado pelo jogador


class ScoreResp(BaseModel):
    delta: int
    score: int
    explanation: str
    correct: bool


# -------------------------------------------------------------------
# FastAPI app
# -------------------------------------------------------------------
app = FastAPI(title="ComputerRak API", version="0.5.0")

# CORS liberado para facilitar testes locais com o HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# Rotas básicas
# -------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "service": "computerrak-api"}


@app.get("/", response_class=HTMLResponse)
def index():
    if not INDEX_PATH.exists():
        raise HTTPException(status_code=404, detail="index.html não encontrado")
    return INDEX_PATH.read_text(encoding="utf-8")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Evita erro 404 no favicon; o front não precisa de ícone aqui
    return {}


# -------------------------------------------------------------------
# /launch — cria nova sessão
# -------------------------------------------------------------------
@app.post("/launch", response_model=LaunchResp)
def launch(req: LaunchReq):
    session_id = str(uuid4())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sessions (id_sessao, user, position, score) VALUES (?, ?, 0, 0)",
        (session_id, req.user),
    )
    conn.commit()
    conn.close()
    return LaunchResp(
        session_id=session_id,
        position=0,
        score=0,
        message="partida iniciada",
    )


# -------------------------------------------------------------------
# /next_challenge — sorteia QUIZ / EXAM / FACT
# -------------------------------------------------------------------
@app.get("/next_challenge")
def next_challenge():
    """
    Retorna um desafio baseado nos bancos:
    - Quiz: item de QUIZ_BANK (1 pergunta)
    - Exam: item de EXAM_BANK (3 perguntas)
    - Fact: item de FACT_BANK (curiosidade)

    Distribuição: 50% quiz, 30% exam, 20% fact (ajustando se algum estiver vazio)
    """
    has_quiz = bool(QUIZ_BANK)
    has_exam = bool(EXAM_BANK)
    has_fact = bool(FACT_BANK)

    if not (has_quiz or has_exam or has_fact):
        raise HTTPException(
            status_code=500, detail="Nenhum banco de desafios carregado."
        )

    r = random.random()  # 0..1

    # 0–0.5 -> Quiz
    if r < 0.5 and has_quiz:
        q = random.choice(QUIZ_BANK)
        return {
            "type": "quiz",
            "payload_id": q["id"],
            "question": q.get("question") or q.get("pergunta"),
            "options": q.get("options") or q.get("opcoes", []),
        }

    # 0.5–0.8 -> Exam
    if r < 0.8 and has_exam:
        exam = random.choice(EXAM_BANK)
        raw_questions = exam.get("questions") or exam.get("questoes")
        if not raw_questions:
            raise HTTPException(
                status_code=500,
                detail=f"Prova {exam.get('id')} sem campo 'questions'/'questoes'",
            )
        questions = []
        for q in raw_questions:
            questions.append(
                {
                    "payload_id": q["id"],
                    "question": q.get("question") or q.get("pergunta"),
                    "options": q.get("options") or q.get("opcoes", []),
                }
            )
        return {
            "type": "exam",
            "payload_id": exam["id"],
            "title": exam.get("title", ""),
            "questions": questions,
        }

    # 0.8–1.0 -> Fact
    if has_fact:
        f = random.choice(FACT_BANK)
        return {
            "type": "fact",
            "payload_id": f["id"],
            "text": f.get("text") or f.get("texto", ""),
        }

    # Se chegou aqui, algum banco deveria existir mas falhou
    raise HTTPException(status_code=500, detail="Erro inesperado ao gerar desafio.")


# -------------------------------------------------------------------
# /score — corrige resposta e atualiza pontuação
# -------------------------------------------------------------------
@app.post("/score", response_model=ScoreResp)
def score(req: ScoreReq):
    # Verificar sessão
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT score FROM sessions WHERE id_sessao = ?", (req.session_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=400, detail="session_id inválido")

    current_score = row[0]

    # Buscar info do payload
    info = get_payload_info(req.payload_id)
    correct_index = int(info["correct_index"])
    explanation = str(info.get("explanation") or "")
    points = int(info.get("points") or 0)

    correct = req.answer == correct_index
    delta = points if correct else 0
    new_score = current_score + delta

    # Atualizar sessão
    cur.execute(
        "UPDATE sessions SET score = ? WHERE id_sessao = ?",
        (new_score, req.session_id),
    )
    # Registrar tentativa
    cur.execute(
        """
        INSERT INTO attempts (id_sessao, payload_id, answer, delta)
        VALUES (?, ?, ?, ?)
        """,
        (req.session_id, req.payload_id, req.answer, delta),
    )
    conn.commit()
    conn.close()

    return ScoreResp(
        delta=delta,
        score=new_score,
        explanation=explanation,
        correct=correct,
    )
