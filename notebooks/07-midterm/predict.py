import pickle
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="wine-quality-predictor")
CURRENT_DIR = Path(__file__).parent
MODEL_FILE = CURRENT_DIR / "model.bin"

with open(MODEL_FILE, "rb") as f_in:
    dv, loaded_model = pickle.load(f_in)


class Wine(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

    class Config:
        populate_by_name = True  # Allows both original and alias names


def predict_single(wine: Wine):
    print(wine)
    wine_dict = wine.model_dump(by_alias=True)
    x_test_sample = dv.transform([wine_dict])[0]
    result = loaded_model.predict(x_test_sample)
    return result


class PredictResponse(BaseModel):
    quality: float


print("""
curl -X 'POST' \
  'http://127.0.0.1:9696/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"fixed_acidity": 7.6, "volatile_acidity": 0.9, "citric_acid": 0.06, "residual_sugar": 2.5, "chlorides": 0.079, "free_sulfur_dioxide": 5.0, "total_sulfur_dioxide": 10.0, "density": 0.9967, "pH": 3.39, "sulphates": 0.56, "alcohol": 9.8}'
""")


@app.post("/predict")
def predict(wine: Wine) -> PredictResponse:
    y_pred = predict_single(wine)
    return {"quality": float(y_pred[0])}


if __name__ == "__main__":
    uvicorn.run(app, port=9696)
