#!/bin/bash

# GCP Frontend Deployment Script
# Make sure you have gcloud CLI installed and configured

set -e

# Configuration
PROJECT_ID="fashioning"
BUCKET_NAME="fashioning-ai-frontend"
REGION="us-central1"

echo "🚀 Deploying Fashioning.ai Frontend to Google Cloud Storage..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Create bucket if it doesn't exist
echo "🪣 Creating/checking Cloud Storage bucket..."
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://$BUCKET_NAME 2>/dev/null || echo "Bucket already exists"

# Make bucket public
echo "🌐 Making bucket public..."
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Upload files
echo "📤 Uploading files to Cloud Storage..."
gsutil -m rsync -r -d frontend/dist gs://$BUCKET_NAME

# Set website configuration
echo "⚙️ Configuring website..."
gsutil web set -m index.html -e 404.html gs://$BUCKET_NAME

echo "✅ Frontend deployed successfully!"
echo "🌍 Website URL: https://storage.googleapis.com/$BUCKET_NAME/index.html"
echo "🌍 Custom domain: https://$BUCKET_NAME.storage.googleapis.com" 