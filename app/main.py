"""
ComputerRak API — com SQLite + Autenticação simples
Fluxo: /health, /launch, /score (persistidos em SQLite).
Token fixo via header: X-API-Key: computerrak-dev
"""

from uuid import uuid4
import sqlite3

from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel

DB_PATH = "computerrak.db"
API_KEY = "computerrak-dev"

app = FastAPI(title="ComputerRak API", version="0.4.0")


# ---------------- AUTENTICAÇÃO ----------------
def require_api_key(x_api_key: str | None = Header(default=None)):
    """
    Autenticação simples por token fixo em header.
    Requisições sem token ou com token incorreto retornam 401.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente. Use header X-API-Key."
        )


# ---------------- DB ----------------
def get_conn() -> sqlite3.Connection:
    """Abre conexão com SQLite e garante FKs ativas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_conn()
    try:
        cur = conn.cursor()
        # sessões (partidas)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id_sessao  TEXT PRIMARY KEY,
                user       TEXT NOT NULL,
                position   INTEGER DEFAULT 0,
                score      INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        # tentativas (respostas)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id_attempt INTEGER PRIMARY KEY AUTOINCREMENT,
                id_sessao  TEXT NOT NULL,
                payload_id TEXT NOT NULL,
                answer     INTEGER NOT NULL,
                delta      INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_sessao) REFERENCES sessions(id_sessao)
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


init_db()


# ------------- MODELOS -------------
class HealthResp(BaseModel):
    status: str
    service: str


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
    answer: int


class ScoreResp(BaseModel):
    delta: int
    score: int
    explanation: str
    correct: bool


# desafio mock para validar /score
CHALLENGES = {
    "q_001": {
        "correct": 1,
        "explanation": "Mestre: a=b=2, f(n)=n ⇒ caso 2 ⇒ O(n log n).",
        "points": 10,
    }
}


# ------------- ENDPOINTS -------------
@app.get("/health", response_model=HealthResp, summary="Healthcheck público")
def health():
    """Verifica se o serviço está no ar (sem precisar de token)."""
    return {"status": "ok", "service": "computerrak-api"}


@app.post(
    "/launch",
    response_model=LaunchResp,
    summary="Criar partida/sessão",
    dependencies=[Depends(require_api_key)],
)
def launch(req: LaunchReq):
    """
    Cria nova sessão de jogo para um usuário.
    Requer header X-API-Key com token válido.
    """
    session_id = str(uuid4())
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions (id_sessao, user, position, score) VALUES (?, ?, 0, 0)",
            (session_id, req.user),
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "session_id": session_id,
        "position": 0,
        "score": 0,
        "message": "partida iniciada",
    }


@app.post(
    "/score",
    response_model=ScoreResp,
    summary="Registrar resposta e pontuação",
    dependencies=[Depends(require_api_key)],
)
def score(req: ScoreReq):
    """
    Registra resposta de um desafio, calcula pontos e atualiza score da sessão.
    Requer header X-API-Key com token válido.
    """
    conn = get_conn()
    try:
        cur = conn.cursor()

        # buscar sessão
        cur.execute(
            "SELECT score FROM sessions WHERE id_sessao = ?",
            (req.session_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=400, detail="session_id inválido")

        current_score = row[0]

        # desafio mock
        ch = CHALLENGES.get(req.payload_id)
        if not ch:
            raise HTTPException(status_code=400, detail="payload_id desconhecido")

        correct = req.answer == ch["correct"]
        delta = ch["points"] if correct else 0
        new_score = current_score + delta

        # atualizar score da sessão
        cur.execute(
            "UPDATE sessions SET score = ? WHERE id_sessao = ?",
            (new_score, req.session_id),
        )

        # registrar tentativa
        cur.execute(
            """
            INSERT INTO attempts (id_sessao, payload_id, answer, delta)
            VALUES (?, ?, ?, ?)
            """,
            (req.session_id, req.payload_id, req.answer, delta),
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "delta": delta,
        "score": new_score,
        "explanation": ch["explanation"],
        "correct": correct,
    }


# opcional: evitar 404 do favicon no log
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return {}
