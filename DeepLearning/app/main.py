from pathlib import Path

import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field


class MultiClassClasification(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 3),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer_stack(x)


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0.0)
    sepal_width: float = Field(..., ge=0.0)
    petal_length: float = Field(..., ge=0.0)
    petal_width: float = Field(..., ge=0.0)


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "iris_classification_model.pth"
CLASS_NAMES = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI(title="Iris Classifier")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

model = MultiClassClasification().to(DEVICE)
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model dosyasi bulunamadi: {MODEL_PATH}")

state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
model.load_state_dict(state_dict)
model.eval()


def _predict(features: IrisFeatures) -> dict:
    input_tensor = torch.tensor(
        [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ],
        dtype=torch.float32,
        device=DEVICE,
    )

    with torch.inference_mode():
        logits = model(input_tensor)
        probabilities = torch.softmax(logits, dim=1).squeeze(0)
        predicted_idx = int(torch.argmax(probabilities).item())

    return {
        "device": str(DEVICE),
        "predicted_class_index": predicted_idx,
        "predicted_class_name": CLASS_NAMES[predicted_idx],
        "probabilities": {
            CLASS_NAMES[i]: round(float(probabilities[i].item()), 6)
            for i in range(len(CLASS_NAMES))
        },
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "device": str(DEVICE),
        "cuda_available": torch.cuda.is_available(),
    }


@app.post("/predict")
async def predict(features: IrisFeatures):
    try:
        return _predict(features)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
