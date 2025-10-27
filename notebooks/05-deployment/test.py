import requests

url = "http://localhost:9696/predict"
clients = [
    {
        "lead_source": "paid_ads",
        "number_of_courses_viewed": 2,
        "annual_income": 79276.0,
    },
    {
        "lead_source": "organic_search",
        "number_of_courses_viewed": 4,
        "annual_income": 80304.0,
    },
]

for client in clients:
    response = requests.post(url, json=client).json()
    print(f"Client: {client}")
    print(f"Response: {response}")
    print()
