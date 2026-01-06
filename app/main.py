from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import DownloadRequest, DownloadResponse, ErrorResponse
from app.downloader import VideoDownloader

# Initialize FastAPI app
app = FastAPI(
    title="Video Downloader API",
    description="Download videos from social media platforms with automatic splitting for large files",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key from request header."""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide X-API-Key header.",
        )
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    return api_key


# Initialize downloader
downloader = VideoDownloader()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Video Downloader API",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "max_file_size_mb": settings.max_file_size_mb,
        "video_quality": settings.video_quality,
    }


@app.post(
    "/download",
    response_model=DownloadResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Missing API Key"},
        403: {"model": ErrorResponse, "description": "Invalid API Key"},
        400: {"model": ErrorResponse, "description": "Invalid URL or download failed"},
    },
)
async def download_video(
    request: DownloadRequest,
    api_key: str = Security(verify_api_key)
):
    """
    Download video from provided URL.
    
    Supports Instagram, YouTube, Twitter, TikTok, and 1000+ other sites.
    Automatically splits videos larger than 25MB into chunks.
    
    Args:
        request: DownloadRequest containing the video URL
        api_key: API key for authentication (from X-API-Key header)
        
    Returns:
        DownloadResponse with video metadata and base64-encoded chunks
    """
    try:
        # Download and process video
        result = downloader.download_video(str(request.url))
        
        return DownloadResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download video: {str(e)}",
        )


# Custom exception handler for better error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "detail": None},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
        },
    )
