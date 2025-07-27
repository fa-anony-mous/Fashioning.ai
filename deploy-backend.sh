#!/bin/bash

# GCP Backend Deployment Script
# Make sure you have gcloud CLI installed and configured

set -e

# Configuration
PROJECT_ID="fashioning"
REGION="us-central1"
SERVICE_NAME="fashioning-ai-backend"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Fashioning.ai Backend to Google Cloud Run..."

# Build and push Docker image
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME ./backend

echo "📤 Pushing image to Google Container Registry..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "ENVIRONMENT=production"

echo "✅ Backend deployed successfully!"
echo "🌍 Service URL: https://$SERVICE_NAME-$REGION.run.app" 