"""
Project.MilanoLibrary Backend
FastAPI application for video analysis and AI-powered learning
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import uuid
import shutil
import asyncio

# Import services
from app.services.ai_service import ai_service
from app.services.video_processor import video_processor

app = FastAPI(
    title="Project.MilanoLibrary API",
    description="AI-powered video content extraction and learning platform",
    version="2.0.3"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置
UPLOAD_DIR = os.getenv("TEMP_DIR", "/tmp/milano_library/uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "500")) * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)

# 内存存储 (MVP 阶段)
videos_db = {}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Project.MilanoLibrary API",
        "version": "2.0.3",
        "status": "running",
        "ai_enabled": True
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/videos/upload")
async def upload_video(file: UploadFile = File(...)):
    """上传视频文件"""
    # 验证文件类型
    allowed_types = ["video/mp4", "video/avi", "video/mov", "video/mkv"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")
    
    # 生成唯一ID
    video_id = f"video_{uuid.uuid4().hex[:8]}"
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 记录到数据库
    videos_db[video_id] = {
        "id": video_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_path": file_path,
        "status": "uploaded",
        "created_at": datetime.now().isoformat(),
        "analysis": None
    }
    
    return {
        "id": video_id,
        "filename": file.filename,
        "status": "uploaded",
        "message": "Video uploaded successfully. Processing will start soon."
    }

@app.get("/api/v1/videos/{video_id}/status")
async def get_video_status(video_id: str):
    """获取视频处理状态"""
    if video_id not in videos_db:
        raise HTTPException(404, "Video not found")
    
    video = videos_db[video_id]
    return {
        "id": video["id"],
        "filename": video["filename"],
        "status": video["status"],
        "created_at": video["created_at"]
    }

@app.get("/api/v1/videos/{video_id}/analysis")
async def get_video_analysis(video_id: str):
    """获取视频分析结果"""
    if video_id not in videos_db:
        raise HTTPException(404, "Video not found")
    
    video = videos_db[video_id]
    
    if video["status"] != "analyzed":
        return {
            "id": video_id,
            "status": video["status"],
            "message": "Video is still being processed. Please check back later."
        }
    
    return {
        "id": video_id,
        "filename": video["filename"],
        "status": "analyzed",
        "sections": video.get("analysis", {}).get("sections", []),
        "summary": video.get("analysis", {}).get("summary", "")
    }

@app.post("/api/v1/videos/{video_id}/analyze")
async def analyze_video(video_id: str):
    """触发视频分析 - 使用真实 AI"""
    if video_id not in videos_db:
        raise HTTPException(404, "Video not found")
    
    video = videos_db[video_id]
    video["status"] = "analyzing"
    
    try:
        # 1. Extract video metadata
        metadata = video_processor.extract_metadata(video["file_path"])
        
        # 2. Generate mock transcript based on video info (MVP phase)
        # In production, this would use speech-to-text
        mock_transcript = f"""
        This is an educational video titled {video['filename']}.
        Duration: {metadata.get('duration', 0)} seconds.
        The video covers fundamental concepts in the subject area.
        Key topics include introduction, core concepts, practical examples, and conclusion.
        The instructor provides clear explanations with visual aids.
        Students will learn the foundational principles and their real-world applications.
        """
        
        # 3. Call AI service for analysis
        analysis_result = await ai_service.analyze_video_content(
            transcript=mock_transcript,
            video_info=metadata
        )
        
        # 4. Store analysis result
        video["analysis"] = analysis_result
        video["metadata"] = metadata
        video["status"] = "analyzed"
        
        return {
            "id": video_id,
            "status": "analyzed",
            "message": "Video analysis completed successfully",
            "sections_count": len(analysis_result.get("sections", []))
        }
        
    except Exception as e:
        video["status"] = "error"
        video["error"] = str(e)
        raise HTTPException(500, f"Analysis failed: {str(e)}")

@app.post("/api/v1/knowledge-points/{point_id}/explain")
async def explain_knowledge_point(point_id: str, request: dict):
    """为知识点生成 AI 解释"""
    topic = request.get("topic", "Unknown Topic")
    context = request.get("context", "")
    
    try:
        explanation = await ai_service.generate_explanation(topic, context)
        return {
            "point_id": point_id,
            "topic": topic,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(500, f"Explanation generation failed: {str(e)}")

@app.post("/api/v1/knowledge-points/{point_id}/mindmap")
async def generate_mind_map(point_id: str, request: dict):
    """为知识点生成思维导图"""
    topic = request.get("topic", "Unknown Topic")
    content = request.get("content", "")
    
    try:
        mind_map = await ai_service.generate_mind_map(topic, content)
        return {
            "point_id": point_id,
            "topic": topic,
            "mind_map": mind_map
        }
    except Exception as e:
        raise HTTPException(500, f"Mind map generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
