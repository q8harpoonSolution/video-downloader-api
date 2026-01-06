# 🎬 Social Media Video Downloader API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Ready-FF6560?style=for-the-badge&logo=n8n&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

**A high-performance, stateless API to download videos from Instagram, YouTube, TikTok, Twitter, and 1000+ other sites.**

[Features](#-features) • [Installation](#-quick-start) • [API Usage](#-api-documentation) • [n8n Integration](#-n8n-workflow-integration) • [Configuration](#-%EF%B8%8F-configuration)

</div>

---

## ⚡ Overview

This API is designed for **AI automation workflows** (like n8n, LangChain, or Zapier). It solves the common problem of handling large video files by automatically optimizing quality and splitting videos into manageable chunks.

### Why use this?
- **Stateless Design**: No file cleanup scripts needed. Returns base64-encoded binary chunks directly.
- **AI-Optimized**: Automatically compresses videos to the "sweet spot" resolution for AI analysis.
- **Smart Splitter**: Automatically detects if a video exceeds 25MB (common API limit) and splits it into precise parts.
- **Universal**: Built on top of `yt-dlp`, supporting virtually every video platform in existence.

---

## ✨ Features

- 🌐 **1000+ Sources**: Universal support for Instagram (Reels/Stories), YouTube (Shorts/Videos), TikTok, X/Twitter, and more.
- 🔐 **Secure Authentication**: Simple but effective API Key protection.
- 📦 **Smart Chunking**: Automatically splits files > 25MB (configurable) into sequential parts.
- 🚀 **Zero Storage**: Streams processing in-memory and returns JSON with base64 data.
- 🐳 **Dockerized**: Deploy anywhere in seconds with a single command.
- 📊 **Health Monitoring**: Built-in health checks for production reliability.

---

## 🚀 Quick Start

### 1. Requirements
- Docker & Docker Compose
- That's it!

### 2. Deployment

```bash
# Clone the repository
git clone https://github.com/q8harpoonSolution/video-downloader-api.git
cd video-downloader-api

# Start the service
docker-compose up -d
```

> **Note**: Update the API Key in `docker-compose.yml` before production use!

### 3. Verify
```bash
curl http://localhost:8000/health
```

---

## 📖 API Documentation

### Authentication
Include the API key in the header of every request:
`X-API-Key: your-super-secret-api-key-change-this`

### Endpoints

#### `POST /download`
Downloads and processes a video URL.

**Request:**
```json
{
  "url": "https://www.instagram.com/reel/C123abc/"
}
```

**Response:**
```json
{
  "title": "Amazing Sunset Reel",
  "source": "instagram",
  "total_size_mb": 45.2,
  "duration_seconds": 60.5,
  "chunks": [
    {
      "index": 1,
      "data": "AAAAFGZ0eXBtcDQyAAAAIG...", // Base64 encoded video
      "size_mb": 24.8,
      "format": "mp4"
    },
    {
      "index": 2,
      "data": "AAAAFGZ0eXBtcDQyAAAAIG...",
      "size_mb": 20.4,
      "format": "mp4"
    }
  ]
}
```

#### `GET /health`
Returns service status and configuration limits.

---

## 🔄 n8n Workflow Integration

This API is purpose-built for n8n. Here is the perfect workflow pattern:

1. **HTTP Request Node**:
   - method: `POST`
   - url: `http://video-downloader:8000/download`
   - headers: `X-API-Key: ...`

2. **Split In Batches**:
   - Look at `{{ $json.chunks }}`
   - Batch size: 1

3. **Code Node (Decode)**:
   ```javascript
   // Convert base64 to binary for AI nodes
   const chunk = $input.item.json;
   return {
     binary: {
       data: {
         data: Buffer.from(chunk.data, 'base64'),
         mimeType: 'video/mp4',
         fileName: `video_part_${chunk.index}.mp4`
       }
     }
   }
   ```

4. **AI Analysis Node**:
   - Send the binary data to OpenAI Vision / Gemini / etc.

---

## ⚙️ Configuration

Manage settings via environment variables in `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `your-super-secret...` | Security key for all requests |
| `MAX_FILE_SIZE_MB` | `25` | Target size for splitting (MB) |
| `VIDEO_QUALITY` | `worst` | `worst` (smallest) or `best` |

---

## 🏗️ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast (high-performance) web framework for building APIs.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: The heavy lifter for video extraction.
- **[FFmpeg](https://ffmpeg.org/)**: For world-class video processing and compression.

---

<div align="center">

**[q8harpoonSolution](https://github.com/q8harpoonSolution)**

Built for the community. MIT License.

</div>
