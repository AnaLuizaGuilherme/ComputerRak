from datetime import datetime
from typing import Dict, Set
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from uuid import uuid4

app = FastAPI(title="ComputerRak API", version="0.2.1")

# ---------- Models ----------
class LaunchReq(BaseModel):
    user: str

class ScoreReq(BaseModel):
    session_id: str
    payload_id: str
    answer: conint(ge=0)  # inteiro >= 0

class LaunchResp(BaseModel):
    session_id: str
    position: int
    score: int
    message: str

class ScoreResp(BaseModel):
    delta: int
    score: int
    explanation: str
    correct: bool
    already_answered: bool
    at: str  # ISO timestamp

# ---------- In-memory state ----------
# sessions[sid] = {"user": str, "position": int, "score": int, "answered": set[str]}
sessions: Dict[str, Dict] = {}

# Desafio mock: inclua "choices" para validar o índice
challenges = {
    "q_001": {
        "correct": 1,
        "choices": 3,  # há 3 alternativas (0,1,2)
        "explanation": "Mestre: a=b=2 e f(n)=n ⇒ caso 2 ⇒ O(n log n).",
        "points": 10,
    }
}

# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok", "service": "computerrak-api"}

@app.post("/launch", response_model=LaunchResp)
def launch(req: LaunchReq):
    sid = str(uuid4())
    sessions[sid] = {"user": req.user, "position": 0, "score": 0, "answered": set()}  # type: ignore
    return {"session_id": sid, "position": 0, "score": 0, "message": "partida iniciada"}

@app.post("/score", response_model=ScoreResp)
def score(req: ScoreReq):
    sess = sessions.get(req.session_id)
    if not sess:
        raise HTTPException(400, "session_id inválido")

    ch = challenges.get(req.payload_id)
    if not ch:
        raise HTTPException(400, "payload_id desconhecido")

    # valida índice da resposta
    if req.answer >= ch["choices"]:
        raise HTTPException(422, f"answer deve estar entre 0 e {ch['choices']-1}")

    now = datetime.utcnow().isoformat() + "Z"

    # evita pontuar duas vezes o mesmo desafio
    answered: Set[str] = sess["answered"]
    if req.payload_id in answered:
        return {
            "delta": 0,
            "score": sess["score"],
            "explanation": "Resposta já registrada para este desafio.",
            "correct": (req.answer == ch["correct"]),
            "already_answered": True,
            "at": now,
        }

    correct = (req.answer == ch["correct"])
    delta = ch["points"] if correct else 0
    sess["score"] += delta
    answered.add(req.payload_id)

    return {
        "delta": delta,
        "score": sess["score"],
        "explanation": ch["explanation"],
        "correct": correct,
        "already_answered": False,
        "at": now,
    }
