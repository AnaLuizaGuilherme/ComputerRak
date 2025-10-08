"ComputerRak API – serviço FastAPI com endpoint de saúde."

from fastapi import FastAPI

# dois espaços em branco antes de função (evita flake8 E302)
app = FastAPI(title="ComputerRak API", version="0.1.0")


@app.get("/health")
def health():
    "Endpoint de verificação de saúde do serviço."
    return {"status": "ok", "service": "computerrak-api"}
