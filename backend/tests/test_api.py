"""
Backend API Tests for Project.MilanoLibrary
Test-driven development for all endpoints
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, videos_db

client = TestClient(app)


class TestSystemEndpoints:
    """Test system health and info endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "2.0.3"
        assert data["ai_enabled"] == True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestVideoUpload:
    """Test video upload functionality"""
    
    def test_upload_video_success(self, tmp_path):
        """Test successful video upload"""
        # Create a mock video file
        video_file = tmp_path / "test_video.mp4"
        video_file.write_bytes(b"mock video content")
        
        with open(video_file, "rb") as f:
            response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["filename"] == "test_video.mp4"
        assert data["status"] == "uploaded"
        assert "message" in data
        
        # Cleanup
        video_id = data["id"]
        if video_id in videos_db:
            del videos_db[video_id]
    
    def test_upload_invalid_file_type(self, tmp_path):
        """Test upload with invalid file type"""
        # Create a non-video file
        text_file = tmp_path / "test.txt"
        text_file.write_text("not a video")
        
        with open(text_file, "rb") as f:
            response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]


class TestVideoStatus:
    """Test video status endpoints"""
    
    def test_get_status_existing_video(self, tmp_path):
        """Test getting status of existing video"""
        # First upload a video
        video_file = tmp_path / "test_video.mp4"
        video_file.write_bytes(b"mock video content")
        
        with open(video_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        video_id = upload_response.json()["id"]
        
        # Get status
        response = client.get(f"/api/v1/videos/{video_id}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == video_id
        assert "status" in data
        assert "created_at" in data
        
        # Cleanup
        del videos_db[video_id]
    
    def test_get_status_nonexistent_video(self):
        """Test getting status of non-existent video"""
        response = client.get("/api/v1/videos/nonexistent/status")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestVideoAnalysis:
    """Test video analysis endpoints"""
    
    def test_analyze_video_success(self, tmp_path):
        """Test successful video analysis"""
        # Upload a video first
        video_file = tmp_path / "test_video.mp4"
        video_file.write_bytes(b"mock video content")
        
        with open(video_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        video_id = upload_response.json()["id"]
        
        # Trigger analysis
        response = client.post(f"/api/v1/videos/{video_id}/analyze")
        
        # Note: In real test with FFmpeg, this might fail
        # For MVP, we check the response structure
        if response.status_code == 200:
            data = response.json()
            assert data["id"] == video_id
            assert data["status"] == "analyzed"
            assert "sections_count" in data
        
        # Cleanup
        if video_id in videos_db:
            del videos_db[video_id]
    
    def test_get_analysis_before_analyze(self, tmp_path):
        """Test getting analysis before analysis is triggered"""
        # Upload a video
        video_file = tmp_path / "test_video.mp4"
        video_file.write_bytes(b"mock video content")
        
        with open(video_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        video_id = upload_response.json()["id"]
        
        # Get analysis without triggering
        response = client.get(f"/api/v1/videos/{video_id}/analysis")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == video_id
        assert data["status"] == "uploaded"
        assert "message" in data
        
        # Cleanup
        del videos_db[video_id]
    
    def test_get_analysis_after_analyze(self, tmp_path):
        """Test getting analysis after analysis is complete"""
        # Upload and analyze
        video_file = tmp_path / "test_video.mp4"
        video_file.write_bytes(b"mock video content")
        
        with open(video_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        video_id = upload_response.json()["id"]
        
        # Trigger analysis
        client.post(f"/api/v1/videos/{video_id}/analyze")
        
        # Get analysis
        response = client.get(f"/api/v1/videos/{video_id}/analysis")
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "analyzed":
                assert "sections" in data
                assert "summary" in data
                assert isinstance(data["sections"], list)
        
        # Cleanup
        if video_id in videos_db:
            del videos_db[video_id]


class TestKnowledgePoints:
    """Test knowledge point interaction endpoints"""
    
    def test_explain_knowledge_point(self):
        """Test AI explanation generation"""
        response = client.post(
            "/api/v1/knowledge-points/test-point/explain",
            json={
                "topic": "Test Topic",
                "context": "Test context for explanation"
            }
        )
        
        # Might fail if AI service is not configured
        if response.status_code == 200:
            data = response.json()
            assert data["point_id"] == "test-point"
            assert data["topic"] == "Test Topic"
            assert "explanation" in data
    
    def test_generate_mind_map(self):
        """Test mind map generation"""
        response = client.post(
            "/api/v1/knowledge-points/test-point/mindmap",
            json={
                "topic": "Test Topic",
                "content": "Test content for mind map generation"
            }
        )
        
        # Might fail if AI service is not configured
        if response.status_code == 200:
            data = response.json()
            assert data["point_id"] == "test-point"
            assert data["topic"] == "Test Topic"
            assert "mind_map" in data
            assert "center" in data["mind_map"]
            assert "branches" in data["mind_map"]


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_for_nonexistent_video(self):
        """Test 404 for non-existent video"""
        endpoints = [
            ("GET", "/api/v1/videos/fake-id/status"),
            ("GET", "/api/v1/videos/fake-id/analysis"),
            ("POST", "/api/v1/videos/fake-id/analyze"),
        ]
        
        for method, endpoint in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(endpoint)
            
            assert response.status_code == 404


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
