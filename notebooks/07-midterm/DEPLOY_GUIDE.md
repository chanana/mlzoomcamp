# Google Cloud Run Deployment - Step by Step

Follow these steps to deploy your Wine Quality Predictor to Google Cloud Run.

## Prerequisites

1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project YOUR_PROJECT_ID`

## Step-by-Step Deployment

### Step 1: Create Artifact Registry Repository

This creates a place to store your Docker images.

```bash
# Set your region (choose one close to you)
export REGION=us-central1

# Create the repository
gcloud artifacts repositories create model-repo \
    --repository-format=docker \
    --location=$REGION \
    --description="ML Model Docker images"
```

**Expected output**: `Created repository [model-repo]`

If it already exists, you'll see an error - that's fine, continue to Step 2.

---

### Step 2: Build and Push Docker Image

Navigate to your **project root** (mlzoomcamp directory):

```bash
cd /Users/shauryachanana/code/mlzoomcamp
```

Build and push the image:

```bash
# Get your project ID
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1

# Build and push
gcloud builds submit \
    --tag $REGION-docker.pkg.dev/$PROJECT_ID/model-repo/wine-quality-service \
    --gcs-source-staging-dir=gs://$PROJECT_ID\_cloudbuild/source
```

**Note**: This will:
- Upload your code to Google Cloud Storage
- Build the Docker image using your Dockerfile
- Push it to Artifact Registry
- Takes ~5-10 minutes

---

### Step 3: Deploy to Cloud Run

Once the image is built:

```bash
gcloud run deploy wine-quality-predictor \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/model-repo/wine-quality-service \
    --platform managed \
    --region $REGION \
    --port 9696 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --timeout 300
```

**When asked**:
- "Allow unauthenticated invocations?" → Press `y` and Enter

---

### Step 4: Get Your Service URL

```bash
gcloud run services describe wine-quality-predictor \
    --region $REGION \
    --format 'value(status.url)'
```

This will output your service URL (e.g., `https://wine-quality-predictor-abc123.run.app`)

---

### Step 5: Test Your Deployment

```bash
# Replace with your actual service URL
export SERVICE_URL=https://wine-quality-predictor-abc123.run.app

# Test it
curl -X 'POST' \
  "$SERVICE_URL/predict" \
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

**Expected response**:
```json
{"quality": 5.234567}
```

Or use the test script:

```bash
cd notebooks/07-midterm
./test_cloud.sh $SERVICE_URL
```

---

## Troubleshooting

### Error: "Dockerfile required when specifying --tag"

**Solution**: Make sure you're in the project root (`mlzoomcamp` directory), not in `notebooks/07-midterm`.

```bash
# Check your current directory
pwd  # Should show: /Users/shauryachanana/code/mlzoomcamp

# If not, navigate there
cd /Users/shauryachanana/code/mlzoomcamp
```

### Error: "Cloud Build has not been used in project..."

**Solution**: Enable Cloud Build API:

```bash
gcloud services enable cloudbuild.googleapis.com
```

### Error: "Permission denied"

**Solution**: Make sure your account has the necessary permissions:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/run.admin"
```

---

## Quick Command Reference

```bash
# View your service
gcloud run services list --region=$REGION

# View logs
gcloud run services logs read wine-quality-predictor --region=$REGION

# Delete the service (to save costs)
gcloud run services delete wine-quality-predictor --region=$REGION

# Delete the image
gcloud artifacts docker images delete \
    $REGION-docker.pkg.dev/$PROJECT_ID/model-repo/wine-quality-service
```

---

## Cost Estimation

- **Cloud Run**: Pay per request, first 2 million requests/month are free
- **Artifact Registry**: $0.10 per GB/month for storage
- **Cloud Build**: First 120 build-minutes/day are free

With minimal usage, this should stay within the free tier! 💰

