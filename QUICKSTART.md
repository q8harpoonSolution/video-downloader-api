# Quick Start Guide

## 🚀 Deploy with Docker

```bash
cd "c:\projects\Video Downloader"

# Edit docker-compose.yml and set your API key
# Then start the service:
docker-compose up -d

# Check if it's running:
curl http://localhost:8000/health
```

## 🐙 Push to GitHub

```bash
# Create a new repository on GitHub first, then:
cd "c:\projects\Video Downloader"
git remote add origin https://github.com/YOUR_USERNAME/video-downloader-api.git
git branch -M main
git push -u origin main
```

## 🧪 Test the API

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-super-secret-api-key-change-this" \
  -d "{\"url\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"}"
```

## 📊 View Logs

```bash
docker-compose logs -f video-downloader
```

## 🛑 Stop Service

```bash
docker-compose down
```

## 🔄 Update and Restart

```bash
docker-compose down
docker-compose up -d --build
```
