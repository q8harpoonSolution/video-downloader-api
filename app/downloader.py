import base64
import io
import math
import tempfile
from pathlib import Path
from typing import List, Dict, Any

import yt_dlp

from app.config import settings
from app.models import VideoChunk


class VideoDownloader:
    """Handles video downloading and processing using yt-dlp."""
    
    def __init__(self):
        self.max_size_bytes = settings.max_file_size_mb * 1024 * 1024
        
    def download_video(self, url: str) -> Dict[str, Any]:
        """
        Download video from URL and return processed chunks.
        
        Args:
            url: Video URL to download
            
        Returns:
            Dictionary containing video metadata and chunks
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "video.%(ext)s"
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'worst[ext=mp4]/worst',
                'outtmpl': str(output_path),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'nocheckcertificate': True,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'postprocessor_args': [
                    '-c:v', 'libx264',
                    '-crf', '28',
                    '-preset', 'fast',
                    '-c:a', 'aac',
                    '-b:a', '64k',
                ],
            }

            # Apply proxy if configured
            if settings.proxy_url:
                print(f"DEBUG: Using proxy: {settings.proxy_url}")
                ydl_opts['proxy'] = settings.proxy_url

            # Check for cookies/tokens
            cookies_file = Path("cookies.txt")
            
            # YouTube Extractor Args (2025 Bot Bypass)
            # Reference: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp
            yt_extractor_args = {
                'player_client': ['web', 'android'],
                'player_skip': ['webpage', 'configs', 'js'],
            }
            
            if settings.po_token:
                print(f"DEBUG: Using PO Token for YouTube")
                yt_extractor_args['po_token'] = [f"web+{settings.po_token}"]

            # Clean up potential directory error (self-healing)
            if cookies_file.exists() and cookies_file.is_dir():
                print(f"DEBUG: Found cookies.txt as a DIRECTORY (bad state). Deleting it.")
                import shutil
                shutil.rmtree(cookies_file)

            if cookies_file.exists():
                print(f"DEBUG: Found cookies.txt, using it.")
                ydl_opts['cookiefile'] = "cookies.txt"
                # If cookies exist, prioritize web client to match browser session
                yt_extractor_args['player_client'] = ['web']
            else:
                print(f"DEBUG: No cookies.txt found. Using Android fallback.")

            ydl_opts['extractor_args'] = {'youtube': yt_extractor_args}
            
            # Download video and extract info
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Find the downloaded file
                video_file = None
                for file in Path(temp_dir).glob("video.*"):
                    video_file = file
                    break
                
                if not video_file or not video_file.exists():
                    raise Exception("Failed to download video")
                
                # Read video file
                video_data = video_file.read_bytes()
                file_size = len(video_data)
                file_size_mb = file_size / (1024 * 1024)
                
                # Prepare metadata
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'source': info.get('extractor', 'Unknown'),
                    'total_size_mb': round(file_size_mb, 2),
                    'duration_seconds': info.get('duration'),
                    'thumbnail_url': info.get('thumbnail'),
                }
                
                # Split video if needed
                chunks = self._split_video(video_data, file_size)
                metadata['chunks'] = chunks
                
                return metadata
    
    def _split_video(self, video_data: bytes, total_size: int) -> List[VideoChunk]:
        """
        Split video data into chunks if it exceeds max size.
        
        Args:
            video_data: Raw video bytes
            total_size: Total size in bytes
            
        Returns:
            List of VideoChunk objects
        """
        chunks = []
        
        if total_size <= self.max_size_bytes:
            # No splitting needed
            encoded_data = base64.b64encode(video_data).decode('utf-8')
            chunks.append(VideoChunk(
                index=1,
                data=encoded_data,
                size_mb=round(total_size / (1024 * 1024), 2),
                format="mp4"
            ))
        else:
            # Split into multiple chunks
            num_chunks = math.ceil(total_size / self.max_size_bytes)
            chunk_size = math.ceil(total_size / num_chunks)
            
            for i in range(num_chunks):
                start = i * chunk_size
                end = min(start + chunk_size, total_size)
                chunk_data = video_data[start:end]
                
                encoded_data = base64.b64encode(chunk_data).decode('utf-8')
                chunk_size_mb = round(len(chunk_data) / (1024 * 1024), 2)
                
                chunks.append(VideoChunk(
                    index=i + 1,
                    data=encoded_data,
                    size_mb=chunk_size_mb,
                    format="mp4"
                ))
        
        return chunks
