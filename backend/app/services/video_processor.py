"""
Video Processing Service for Project.MilanoLibrary
Handles video file operations and metadata extraction
"""

import os
import subprocess
import json
from typing import Dict, Any, Optional


class VideoProcessor:
    """Video processing utilities"""
    
    def __init__(self):
        self.temp_dir = os.getenv("TEMP_DIR", "/tmp/milano_library")
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def extract_metadata(self, video_path: str) -> Dict[str, Any]:
        """
        Extract metadata from video file using FFmpeg
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        try:
            # Use FFprobe to get metadata
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # Extract relevant info
                format_info = data.get("format", {})
                streams = data.get("streams", [])
                
                # Find video stream
                video_stream = None
                for stream in streams:
                    if stream.get("codec_type") == "video":
                        video_stream = stream
                        break
                
                return {
                    "duration": float(format_info.get("duration", 0)),
                    "size": int(format_info.get("size", 0)),
                    "format": format_info.get("format_name", ""),
                    "width": video_stream.get("width") if video_stream else None,
                    "height": video_stream.get("height") if video_stream else None,
                    "fps": self._parse_fps(video_stream) if video_stream else None,
                    "success": True
                }
            else:
                return {"success": False, "error": "FFprobe failed"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            output_path: Optional output path for audio file
            
        Returns:
            Path to extracted audio file
        """
        if output_path is None:
            video_id = os.path.basename(video_path).split("_")[0]
            output_path = os.path.join(self.temp_dir, f"{video_id}_audio.mp3")
        
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vn",  # No video
                "-acodec", "libmp3lame",
                "-q:a", "2",  # Quality
                "-y",  # Overwrite
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            else:
                raise Exception(f"FFmpeg failed: {result.stderr.decode()}")
                
        except Exception as e:
            raise Exception(f"Audio extraction failed: {e}")
    
    def extract_frame(self, video_path: str, timestamp: float, output_path: Optional[str] = None) -> str:
        """
        Extract a single frame from video at specified timestamp
        
        Args:
            video_path: Path to video file
            timestamp: Time in seconds
            output_path: Optional output path for frame
            
        Returns:
            Path to extracted frame
        """
        if output_path is None:
            video_id = os.path.basename(video_path).split("_")[0]
            output_path = os.path.join(self.temp_dir, f"{video_id}_frame_{int(timestamp)}.jpg")
        
        try:
            cmd = [
                "ffmpeg",
                "-ss", str(timestamp),  # Seek to timestamp
                "-i", video_path,
                "-vframes", "1",  # Single frame
                "-q:v", "2",  # Quality
                "-y",  # Overwrite
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            else:
                raise Exception(f"Frame extraction failed")
                
        except Exception as e:
            raise Exception(f"Frame extraction failed: {e}")
    
    def extract_clip(self, video_path: str, start_time: float, end_time: float, output_path: Optional[str] = None) -> str:
        """
        Extract a video clip from start_time to end_time
        
        Args:
            video_path: Path to video file
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Optional output path for clip
            
        Returns:
            Path to extracted clip
        """
        if output_path is None:
            video_id = os.path.basename(video_path).split("_")[0]
            output_path = os.path.join(self.temp_dir, f"{video_id}_clip_{int(start_time)}_{int(end_time)}.mp4")
        
        duration = end_time - start_time
        
        try:
            cmd = [
                "ffmpeg",
                "-ss", str(start_time),
                "-t", str(duration),
                "-i", video_path,
                "-c", "copy",  # Copy codec (fast)
                "-y",  # Overwrite
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            else:
                # Try with re-encoding if copy fails
                cmd = [
                    "ffmpeg",
                    "-ss", str(start_time),
                    "-t", str(duration),
                    "-i", video_path,
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-y",
                    output_path
                ]
                result = subprocess.run(cmd, capture_output=True)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    return output_path
                else:
                    raise Exception(f"Clip extraction failed")
                    
        except Exception as e:
            raise Exception(f"Clip extraction failed: {e}")
    
    def _parse_fps(self, video_stream: Dict[str, Any]) -> Optional[float]:
        """Parse FPS from video stream info"""
        try:
            # Try avg_frame_rate first
            fps_str = video_stream.get("avg_frame_rate", "")
            if fps_str and "/" in fps_str:
                num, den = fps_str.split("/")
                return float(num) / float(den)
            
            # Try r_frame_rate
            fps_str = video_stream.get("r_frame_rate", "")
            if fps_str and "/" in fps_str:
                num, den = fps_str.split("/")
                return float(num) / float(den)
            
            return None
        except:
            return None


# Global instance
video_processor = VideoProcessor()
