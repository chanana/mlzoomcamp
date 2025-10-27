import pickle
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI(title="will-customer-join-the-course")
CURRENT_DIR = Path(__file__).parent
MODEL_FILE = CURRENT_DIR / "pipeline_v2.bin"


with open(MODEL_FILE, "rb") as f_in:
    pipeline = pickle.load(f_in)


class Customer(BaseModel):
    lead_source: str
    number_of_courses_viewed: int = Field(ge=0)
    annual_income: float = Field(ge=0)


def predict_single(customer: Customer):
    # Convert Pydantic model to dictionary for sklearn pipeline
    customer_dict = customer.model_dump()
    result = pipeline.predict_proba([customer_dict])[0, 1]
    return result


class PredictResponse(BaseModel):
    probability: float
    will_customer_buy: bool


"""
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"lead_source": "paid_ads","number_of_courses_viewed": 2,"annual_income": 79276.0}'
"""


@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    y_pred = predict_single(customer)
    result = y_pred >= 0.5

    return {"probability": float(y_pred), "will_customer_buy": bool(result)}


if __name__ == "__main__":
    uvicorn.run(app, port=9696)
