import requests
import os

# Public Cloud Run endpoint
# To test locally, use: export TEST_URL=http://localhost:9696
CLOUD_URL = "https://wine-quality-predictor-933028008008.us-central1.run.app/predict"

url = os.getenv("TEST_URL", CLOUD_URL)
print(f"🧪 Testing Wine Quality Predictor at: {url}\n")
wines = [
    {
        "fixed_acidity": 7.6,
        "volatile_acidity": 0.9,
        "citric_acid": 0.06,
        "residual_sugar": 2.5,
        "chlorides": 0.079,
        "free_sulfur_dioxide": 5.0,
        "total_sulfur_dioxide": 10.0,
        "density": 0.9967,
        "pH": 3.39,
        "sulphates": 0.56,
        "alcohol": 9.8,
    },
    {
        "fixed_acidity": 7.1,
        "volatile_acidity": 0.27,
        "citric_acid": 0.6,
        "residual_sugar": 2.1,
        "chlorides": 0.074,
        "free_sulfur_dioxide": 17.0,
        "total_sulfur_dioxide": 25.0,
        "density": 0.99814,
        "pH": 3.38,
        "sulphates": 0.72,
        "alcohol": 10.6,
    },
]

for w in wines:
    response = requests.post(url, json=w).json()
    print(f"Wine: {w}")
    print("=" * 50)
    print(f"Quality: {response['quality']}")
    print("=" * 50)
    print()
