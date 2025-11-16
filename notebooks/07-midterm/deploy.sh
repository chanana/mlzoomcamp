#!/bin/bash
# Complete deployment script for Wine Quality Predictor to Google Cloud Run
# 
# Prerequisites:
# 1. gcloud CLI installed and authenticated
# 2. Podman/Docker image already built locally as 'midterm'
#
# Usage: ./deploy.sh

set -e  # Exit on error
# Configuration
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export IMAGE_URI=$REGION-docker.pkg.dev/$PROJECT_ID/model-repo/wine-quality-service
export SERVICE_NAME=wine-quality-predictor

echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Image: $IMAGE_URI"
echo ""

# Step 1: Tag and push local Podman image
echo "📦 Step 1: Tagging and pushing local image..."
podman tag localhost/midterm $IMAGE_URI

echo "Configuring Docker auth..."
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

echo "Pushing to Artifact Registry..."
podman push $IMAGE_URI

echo "✅ Image pushed successfully"
echo ""

# Step 2: Deploy to Cloud Run
echo "☁️  Step 2: Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URI \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 1 \
    --timeout 60

# Step 3: Get service URL
echo ""
echo "🔍 Getting service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --format 'value(status.url)')

echo ""
echo "🎉 Deployment complete!"
echo "========================================"
echo "Service URL: $SERVICE_URL"
echo "API Docs: $SERVICE_URL/docs"
echo "========================================"
echo ""
echo "Test your deployment:"
echo "./test_cloud.sh $SERVICE_URL"
