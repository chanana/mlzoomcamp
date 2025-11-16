# Wine Quality Prediction Model

A machine learning service that predicts the quality of red wine based on physicochemical properties using XGBoost regression.

## Problem

### The Challenge

Wine quality assessment traditionally relies on expert sommeliers and lengthy tasting panels, which are, time-consuming, expensives, subjective, and have scalability issues.

### The Solution

This machine learning service provides **instant, objective wine quality predictions** based on measurable chemical properties that can be obtained through standard laboratory analysis. The model predicts quality scores (1-10 scale) using 11 physicochemical features.

### Use Cases
- Wine Production & Quality Control (Monitoring quality trends in real-time, Batch evaluation, Quality gates)
- Winery Operations (Blending decisions, Inventory management, Cost optimization)
- Supply Chain & Distribution (Supplier screening, Quality assurance, Market positioning)
- Research & Development (Recipe development, Feature analysis, Process optimization)

### Why This Approach?

**Regression over Classification**: We treat wine quality as a continuous prediction problem rather than discrete classes because:
- Preserves the ordinal nature of quality scores (7 is objectively better than 5)
- Provides granular predictions (e.g., 6.3 vs 6.8) useful for fine-grained decisions
- Avoids arbitrary classification boundaries

**Real-time API**: Deployed as a web service for:
- Integration with existing lab information systems (LIMS)
- Batch processing of multiple samples
- Mobile/web applications for on-site quality checks

## 📊 Dataset

**Source**: Red Wine Quality Dataset (`winequality-red.csv`)

- **Samples**: 1,599 wines
- **Features**: 11 physicochemical properties (all float values)
  - Fixed acidity
  - Volatile acidity
  - Citric acid
  - Residual sugar
  - Chlorides
  - Free sulfur dioxide
  - Total sulfur dioxide
  - Density
  - pH
  - Sulphates
  - Alcohol content
- **Target**: Quality score (integer from 1-10)

## 🔬 Methodology & Experiments

### 1. Exploratory Data Analysis (EDA)

- **Missing Values**: No missing data
- **Data Types**: All features are continuous (float64), target is integer
- **Distributions**: Visualized histograms for all features
- **Correlation Analysis**: Examined feature relationships using heatmap
  - Notable correlations: pH correlates with acidity features (as expected)
- **Feature Importance**: Used 1-depth decision tree to identify most important feature
  - **Result**: Alcohol content is the primary split feature

### 2. Data Splitting

- **Training**: 60% (959 samples)
- **Validation**: 20% (320 samples)
- **Test**: 20% (320 samples)
- Random state: 1 (for reproducibility)

### 3. Feature Engineering

- Used `DictVectorizer` to transform features for model training
- Preserved original column names with spaces for consistency with dataset

### 4. Model Experiments

#### Random Forest Regressor
- **Baseline Model**: 10 estimators, max_depth=5
- **Hyperparameter Tuning**:
  - Tested n_estimators: 10 to 200 (step 10)
  - Tested max_depth: [10, 15, 20, 25]
  - Evaluated using RMSE on validation set
  - **Best max_depth**: 20 (based on mean RMSE across different n_estimators)
  - **Optimal n_estimators**: ~30 (diminishing returns after this point)

#### XGBoost Regressor (Final Model)
- **Approach**: Treated as regression problem (predicting continuous quality scores)
- **Hyperparameter Tuning**: Used GridSearchCV with 5-fold cross-validation
  - **eta** (learning rate): Tested range 0.01 to 0.30
  - **max_depth**: Tested range 1 to 10
  - **min_child_weight**: Tested range 1 to 10
  - **Objective**: `reg:squarederror`
  - **Scoring metric**: Negative mean squared error
- **Model Serialization**: Saved as `model.bin` with DictVectorizer

### 5. Model Evaluation

- **Primary Metric**: RMSE (Root Mean Squared Error)
- Random Forest achieved competitive performance
- XGBoost with optimized hyperparameters provided the best results

## 🚀 Deployment

### API Service

Built a FastAPI service (`predict.py`) that:
- Loads the trained XGBoost model and DictVectorizer
- Exposes a `/predict` endpoint for wine quality predictions
- Uses Pydantic models for request/response validation
- Returns quality predictions as float values

### Docker Containerization

Containerized using Docker/Podman with:
- Base image: `python:3.13.5-slim-bookworm`
- Package manager: `uv` (fast Python package installer)
- Exposed port: 9696
- ASGI server: Uvicorn

## 🏃 Running Locally

### Prerequisites

- Python 3.12+
- `uv` package manager (or pip)
- Docker/Podman (for containerized deployment)

### Option 1: Run with Python/UV

```bash
# Navigate to the project directory
cd notebooks/07-midterm

# Run the FastAPI server
uv run uvicorn predict:app --port 9696 --reload

# In another terminal, test the API
uv run python test.py
```

### Option 2: Run with Docker/Podman

```bash
# Build the Docker image (from project root)
docker build -t midterm -f notebooks/07-midterm/Dockerfile .

# Or with Podman
podman build --platform linux/amd64 -t midterm -f notebooks/07-midterm/Dockerfile .

# Run the container with port mapping
docker run -it --rm -p 9696:9696 midterm

# Or with Podman
podman run --platform linux/amd64 -it --rm -p 9696:9696 midterm

# Test the API (from another terminal)
cd notebooks/07-midterm
uv run python test.py
```

### Testing the API

#### Using Python test script:

```bash
python test.py
```

#### Using curl:

```bash
curl -X 'POST' \
  'http://localhost:9696/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
    "alcohol": 9.8
  }'
```

#### Expected Response:

```json
{
  "quality": 5.234567
}
```

## 💼 Real-World Usage Examples

### Example 1: Quality Control in Production

A winery sends daily samples from fermentation tanks to their lab. Lab results show:
- Fixed acidity: 8.2, Volatile acidity: 0.42, Citric acid: 0.38
- Residual sugar: 2.1, Chlorides: 0.081
- Free sulfur dioxide: 15.0, Total sulfur dioxide: 42.0
- Density: 0.9968, pH: 3.28, Sulphates: 0.68, Alcohol: 11.2

**API Call:**
```python
import requests

result = requests.post(
    "https://wine-quality-predictor-xxx.run.app/predict",
    json={
        "fixed_acidity": 8.2, "volatile_acidity": 0.42, "citric_acid": 0.38,
        "residual_sugar": 2.1, "chlorides": 0.081,
        "free_sulfur_dioxide": 15.0, "total_sulfur_dioxide": 42.0,
        "density": 0.9968, "pH": 3.28, "sulphates": 0.68, "alcohol": 11.2
    }
).json()

print(f"Predicted Quality: {result['quality']:.2f}")
# Output: Predicted Quality: 6.45
```

**Decision**: Quality score > 6.0 → Proceed with bottling

### Example 2: Batch Evaluation

A distributor receives lab reports for 100 wine samples and needs to quickly identify premium wines (quality ≥ 7):

```python
import pandas as pd
import requests

# Load lab reports
samples = pd.read_csv("lab_reports.csv")

# Batch predict
for idx, row in samples.iterrows():
    wine_data = row.drop('sample_id').to_dict()
    result = requests.post(API_URL, json=wine_data).json()
    
    if result['quality'] >= 7.0:
        print(f"Premium wine found: Sample {row['sample_id']} - Quality {result['quality']:.2f}")
```

### Example 3: Blending Optimization

A winemaker wants to predict quality before physically blending two wines:

```python
# Wine A properties
wine_a = {"fixed_acidity": 7.1, "alcohol": 9.8, ...}
wine_b = {"fixed_acidity": 8.9, "alcohol": 12.3, ...}

# Simulate 50/50 blend
blend = {key: (wine_a[key] + wine_b[key]) / 2 for key in wine_a}

quality = requests.post(API_URL, json=blend).json()['quality']
print(f"Expected blend quality: {quality:.2f}")
```

## 📂 Project Structure

```
07-midterm/
├── README.md                 # This file
├── homework.ipynb            # Complete EDA and model training notebook
├── winequality-red.csv       # Dataset
├── model.bin                 # Serialized model (DictVectorizer + XGBoost)
├── predict.py                # FastAPI prediction service
├── test.py                   # Test script for the API
└── Dockerfile                # Container configuration
```

## 🔍 API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:9696/docs
- **Alternative docs**: http://localhost:9696/redoc

## 📈 Model Performance

The final XGBoost model was selected based on:
- Cross-validated grid search performance
- RMSE on validation set
- Training efficiency

Quality predictions range from approximately 3 to 8 (reflecting the dataset's quality distribution).

## 🛠 Technologies Used

- **Python 3.12**
- **Machine Learning**: scikit-learn, XGBoost
- **API Framework**: FastAPI
- **Data Processing**: pandas, numpy
- **Serialization**: pickle
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker/Podman
- **Package Management**: uv

## 📝 Notes

- The model treats wine quality prediction as a **regression problem** rather than classification
- This approach preserves the ordinal nature of quality scores (e.g., 7 is better than 5)
- For binary classification (good vs. bad wine), a threshold could be applied to predictions
- AUC metric would require converting to classification format

## 🔗 Related Files

- Main project notebook: `homework.ipynb`
- Model artifacts: `model.bin`
- Docker configuration: `Dockerfile`
- API implementation: `predict.py`
- Test cases: `test.py`
