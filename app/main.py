import subprocess

from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(
    title="Secure CI/CD Demo Application",
    description="Тестовое приложение для демонстрации безопасного CI/CD-конвейера",
    version="1.0.0"
)

REQUEST_COUNTER = Counter(
    "app_requests_total",
    "Total number of requests to the application"
)


@app.get("/")
def read_root():
    REQUEST_COUNTER.inc()
    return {
        "message": "Secure CI/CD demo application is running"
    }


@app.get("/health")
def health_check():
    REQUEST_COUNTER.inc()
    return {
        "status": "ok"
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    REQUEST_COUNTER.inc()
    return {
        "item_id": item_id,
        "name": f"Item {item_id}"
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/unsafe/{cmd}")
def unsafe_command(cmd: str):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return {"output": result.stdout}