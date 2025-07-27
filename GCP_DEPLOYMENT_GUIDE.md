# 🚀 GCP Deployment Guide for Fashioning.ai

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud CLI** installed and configured
3. **Docker** installed locally
4. **Node.js** and **npm** installed

## Step 1: Setup Google Cloud Project

### 1.1 Create/Select Project
```bash
# List existing projects
gcloud projects list

# Create new project (if needed)
gcloud projects create fashioning-ai-[YOUR-UNIQUE-ID]

# Set the project
gcloud config set project fashioning-ai-[YOUR-UNIQUE-ID]
```

### 1.2 Enable Required APIs
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Storage API
gcloud services enable storage.googleapis.com
```

### 1.3 Configure Docker for GCR
```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker
```

## Step 2: Deploy Backend to Cloud Run

### 2.1 Update Configuration
Edit `deploy-backend.sh` and replace:
- `your-gcp-project-id` with your actual project ID

### 2.2 Deploy Backend
```bash
# Make script executable
chmod +x deploy-backend.sh

# Run deployment
./deploy-backend.sh
```

### 2.3 Set Environment Variables
After deployment, set environment variables in Cloud Run:
```bash
gcloud run services update fashioning-ai-backend \
  --region=us-central1 \
  --set-env-vars="GEMINI_API_KEY=your_gemini_key,ALGOLIA_APP_ID=your_algolia_id,ALGOLIA_ADMIN_API_KEY=your_algolia_key"
```

## Step 3: Deploy Frontend to Cloud Storage

### 3.1 Update Configuration
Edit `deploy-frontend.sh` and replace:
- `your-gcp-project-id` with your actual project ID

### 3.2 Update Frontend API URL
Before building, update `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://fashioning-ai-backend-us-central1.run.app/api/v1';
```

### 3.3 Deploy Frontend
```bash
# Make script executable
chmod +x deploy-frontend.sh

# Run deployment
./deploy-frontend.sh
```

## Step 4: Configure Custom Domain (Optional)

### 4.1 Map Custom Domain
```bash
# Map custom domain to Cloud Run
gcloud run domain-mappings create \
  --service fashioning-ai-backend \
  --domain api.yourdomain.com \
  --region us-central1
```

### 4.2 Configure Cloud Storage for Custom Domain
```bash
# Create load balancer for custom domain
# (This requires additional setup with Cloud Load Balancing)
```

## Step 5: Monitoring and Logging

### 5.1 View Logs
```bash
# View Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=fashioning-ai-backend"

# View Cloud Storage logs
gcloud logging read "resource.type=gcs_bucket"
```

### 5.2 Monitor Performance
- Go to Google Cloud Console
- Navigate to Cloud Run > fashioning-ai-backend
- Check metrics and performance

## Cost Optimization

### Backend (Cloud Run)
- **Free Tier**: 2 million requests/month
- **Pricing**: Pay per request and compute time
- **Optimization**: Set max instances to limit costs

### Frontend (Cloud Storage)
- **Free Tier**: 5GB storage, 1GB/day egress
- **Pricing**: Very low cost for static hosting
- **Optimization**: Use Cloud CDN for better performance

## Troubleshooting

### Common Issues:
1. **Permission Denied**: Ensure proper IAM roles
2. **Build Failures**: Check Dockerfile and requirements.txt
3. **CORS Issues**: Verify CORS configuration in backend
4. **Environment Variables**: Ensure all required vars are set

### Useful Commands:
```bash
# Check service status
gcloud run services describe fashioning-ai-backend --region=us-central1

# View recent deployments
gcloud run revisions list --service=fashioning-ai-backend --region=us-central1

# Update service configuration
gcloud run services update fashioning-ai-backend --region=us-central1 --memory=2Gi
```

## URLs After Deployment

- **Backend API**: `https://fashioning-ai-backend-us-central1.run.app`
- **Frontend**: `https://fashioning-ai-frontend.storage.googleapis.com`
- **API Docs**: `https://fashioning-ai-backend-us-central1.run.app/docs` 