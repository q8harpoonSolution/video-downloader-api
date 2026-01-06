from typing import List
from pydantic import BaseModel, HttpUrl


class VideoChunk(BaseModel):
    """Represents a single video chunk."""
    index: int
    data: str  # Base64 encoded video data
    size_mb: float
    format: str = "mp4"


class DownloadResponse(BaseModel):
    """Response model for video download endpoint."""
    title: str
    source: str
    total_size_mb: float
    chunks: List[VideoChunk]
    duration_seconds: float | None = None
    thumbnail_url: str | None = None


class DownloadRequest(BaseModel):
    """Request model for video download endpoint."""
    url: HttpUrl


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: str | None = None
