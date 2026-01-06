# Video Downloader API 🎥

A powerful FastAPI-based service for downloading videos from social media platforms with automatic splitting for large files. Perfect for n8n workflows and AI video analysis.

## Features ✨

- 🌐 **Universal Support**: Download from Instagram, YouTube, Twitter, TikTok, and 1000+ other sites via yt-dlp
- 🔐 **API Key Authentication**: Secure your API with custom API keys
- 📦 **Automatic Splitting**: Videos larger than 25MB are automatically split into chunks
- 🎯 **Optimized for AI**: Videos are compressed to optimal quality for AI analysis
- 📤 **Base64 Encoding**: Returns video chunks as base64-encoded data in JSON (perfect for n8n)
- 🐳 **Docker Ready**: Easy deployment with Docker Compose
- ⚡ **Fast & Lightweight**: Built with FastAPI for high performance

## Supported Platforms

- Instagram (Posts, Reels, Stories)
- YouTube (Videos, Shorts)
- Twitter/X (Video posts)
- TikTok
- Facebook
- Reddit
- And 1000+ more sites!

## Quick Start 🚀

### Prerequisites

- Docker and Docker Compose installed
- Git (for version control)

### Installation

1. **Clone or navigate to the project**:
```bash
cd "c:\projects\Video Downloader"
```

2. **Configure your API key**:

Edit `docker-compose.yml` and change the API key:
```yaml
environment:
  - API_KEY=your-super-secret-api-key-change-this  # Change this!
```

3. **Start the service**:
```bash
docker-compose up -d
```

4. **Verify it's running**:
```bash
curl http://localhost:8000/health
```

## API Usage 📖

### Authentication

All requests require an API key in the `X-API-Key` header:

```bash
X-API-Key: your-super-secret-api-key-change-this
```

### Endpoints

#### Health Check
```bash
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "max_file_size_mb": 25,
  "video_quality": "worst"
}
```

#### Download Video
```bash
POST /download
Content-Type: application/json
X-API-Key: your-api-key-here

{
  "url": "https://www.instagram.com/reel/..."
}
```

**Response**:
```json
{
  "title": "Video Title",
  "source": "instagram",
  "total_size_mb": 45.2,
  "duration_seconds": 120.5,
  "thumbnail_url": "https://...",
  "chunks": [
    {
      "index": 1,
      "data": "base64_encoded_video_data...",
      "size_mb": 24.8,
      "format": "mp4"
    },
    {
      "index": 2,
      "data": "base64_encoded_video_data...",
      "size_mb": 20.4,
      "format": "mp4"
    }
  ]
}
```

### Example with cURL

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-super-secret-api-key-change-this" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Example with Python

```python
import requests
import base64

url = "http://localhost:8000/download"
headers = {
    "X-API-Key": "your-super-secret-api-key-change-this",
    "Content-Type": "application/json"
}
data = {
    "url": "https://www.instagram.com/reel/..."
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

# Save chunks to files
for chunk in result["chunks"]:
    video_data = base64.b64decode(chunk["data"])
    filename = f"video_part_{chunk['index']}.mp4"
    with open(filename, "wb") as f:
        f.write(video_data)
    print(f"Saved {filename} ({chunk['size_mb']} MB)")
```

## n8n Integration 🔄

### Workflow Setup

1. **HTTP Request Node**:
   - Method: POST
   - URL: `http://your-server:8000/download`
   - Headers:
     - `X-API-Key`: `your-super-secret-api-key-change-this`
     - `Content-Type`: `application/json`
   - Body: `{"url": "{{ $json.video_url }}"}`

2. **Process Response**:
   - The response contains an array of chunks in `chunks`
   - Each chunk has `data` (base64), `size_mb`, and `index`
   - Loop through chunks using a Split In Batches node

3. **Decode Base64**:
   ```javascript
   // In a Function node
   const chunk = $input.item.json.chunks[0];
   const buffer = Buffer.from(chunk.data, 'base64');
   return { binary: { data: buffer } };
   ```

## Configuration ⚙️

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `your-super-secret-api-key-change-this` | API key for authentication |
| `MAX_FILE_SIZE_MB` | `25` | Maximum size per chunk in MB |
| `VIDEO_QUALITY` | `worst` | Video quality (worst/best) |

### Customization

Edit `docker-compose.yml` to change settings:

```yaml
environment:
  - API_KEY=my-custom-key-123
  - MAX_FILE_SIZE_MB=30
  - VIDEO_QUALITY=worst
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## Development 💻

### Local Development (without Docker)

1. **Create virtual environment**:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set environment variables**:
```bash
$env:API_KEY="your-api-key"
```

4. **Run the server**:
```bash
uvicorn app.main:app --reload
```

5. **Access API docs**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Error Handling 🚨

### Common Errors

| Status Code | Error | Solution |
|-------------|-------|----------|
| 401 | Missing API Key | Add `X-API-Key` header |
| 403 | Invalid API Key | Check your API key in docker-compose.yml |
| 400 | Invalid URL or download failed | Verify the URL is accessible and supported |
| 500 | Internal server error | Check logs: `docker-compose logs` |

### Debugging

View logs:
```bash
docker-compose logs -f video-downloader
```

## Performance Tips 🚀

- Videos are automatically compressed for optimal AI analysis
- Larger videos are split into 25MB chunks to avoid memory issues
- Use the `worst` quality setting for fastest downloads and smallest files
- The API is stateless - no cleanup needed!

## GitHub Version Control 📚

### Initialize Repository

```bash
cd "c:\projects\Video Downloader"
git init
git add .
git commit -m "Initial commit: Video Downloader API"
```

### Create GitHub Repository

```bash
# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/video-downloader-api.git
git branch -M main
git push -u origin main
```

## License

MIT License - feel free to use this in your projects!

## Support

For issues or questions, please create an issue on GitHub.

---

**Built with ❤️ using FastAPI and yt-dlp**
