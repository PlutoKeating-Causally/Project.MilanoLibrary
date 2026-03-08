"""
AI Service for Project.MilanoLibrary
Integrates with Google Gemini API and Kimi API for video content analysis
"""

import os
import json
from typing import List, Dict, Any
import httpx

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
KIMI_MODEL = os.getenv("KIMI_MODEL", "moonshot-v1-8k")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
KIMI_API_URL = "https://api.moonshot.cn/v1"


class AIService:
    """AI Service for video content analysis"""
    
    def __init__(self):
        self.google_api_key = GOOGLE_API_KEY
        self.kimi_api_key = KIMI_API_KEY
    
    async def analyze_video_content(self, transcript: str, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze video content using AI
        
        Args:
            transcript: Video transcript text
            video_info: Video metadata
            
        Returns:
            Analysis result with sections and summary
        """
        try:
            # Use Gemini for initial analysis
            result = await self._analyze_with_gemini(transcript)
            return result
        except Exception as e:
            print(f"AI analysis error: {e}")
            # Fallback to mock analysis if AI fails
            return self._mock_analysis(transcript)
    
    async def _analyze_with_gemini(self, transcript: str) -> Dict[str, Any]:
        """Analyze content using Google Gemini API"""
        
        prompt = f"""
        Analyze the following video transcript and provide a structured breakdown.
        
        Transcript:
        {transcript[:5000]}  # Limit to first 5000 chars for MVP
        
        Please provide:
        1. A brief overall summary (2-3 sentences)
        2. Break down into 3-5 logical sections with:
           - Section title
           - Start and end timestamps (estimate based on content flow)
           - Brief summary of each section
        
        Return the result in this JSON format:
        {{
            "summary": "overall summary",
            "sections": [
                {{
                    "title": "section title",
                    "start_time": 0,
                    "end_time": 120,
                    "summary": "section summary"
                }}
            ]
        }}
        
        Return ONLY the JSON, no markdown formatting.
        """
        
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=60.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract text from Gemini response
            if "candidates" in data and len(data["candidates"]) > 0:
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Try to parse JSON from the response
                try:
                    # Remove markdown code blocks if present
                    text_content = text_content.replace("```json", "").replace("```", "").strip()
                    result = json.loads(text_content)
                    return result
                except json.JSONDecodeError:
                    # If JSON parsing fails, return structured mock data
                    return self._parse_text_response(text_content)
            
            return self._mock_analysis(transcript)
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse non-JSON text response into structured format"""
        # Simple parsing for MVP - can be improved
        lines = text.strip().split('\n')
        
        summary = ""
        sections = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.lower().startswith('summary'):
                summary = line.split(':', 1)[1].strip() if ':' in line else ""
            elif line[0].isdigit() and '.' in line:
                # New section
                if current_section:
                    sections.append(current_section)
                title = line.split('.', 1)[1].strip()
                current_section = {
                    "title": title,
                    "start_time": len(sections) * 120,  # Estimate 2 min per section
                    "end_time": (len(sections) + 1) * 120,
                    "summary": ""
                }
            elif current_section and line:
                current_section["summary"] += line + " "
        
        if current_section:
            sections.append(current_section)
        
        return {
            "summary": summary or "Video content analysis",
            "sections": sections or self._default_sections()
        }
    
    def _mock_analysis(self, transcript: str) -> Dict[str, Any]:
        """Mock analysis for MVP testing"""
        return {
            "summary": "This video contains educational content covering fundamental concepts. The instructor explains key ideas with clear examples and visual aids.",
            "sections": [
                {
                    "title": "Introduction",
                    "start_time": 0,
                    "end_time": 120,
                    "summary": "Overview of the topic and learning objectives"
                },
                {
                    "title": "Core Concepts",
                    "start_time": 120,
                    "end_time": 420,
                    "summary": "Explanation of fundamental principles and theories"
                },
                {
                    "title": "Practical Examples",
                    "start_time": 420,
                    "end_time": 720,
                    "summary": "Real-world applications and case studies"
                },
                {
                    "title": "Summary",
                    "start_time": 720,
                    "end_time": 900,
                    "summary": "Recap of key points and conclusion"
                }
            ]
        }
    
    def _default_sections(self) -> List[Dict[str, Any]]:
        """Default sections if analysis fails"""
        return [
            {
                "title": "Part 1",
                "start_time": 0,
                "end_time": 300,
                "summary": "Introduction and background"
            },
            {
                "title": "Part 2",
                "start_time": 300,
                "end_time": 600,
                "summary": "Main content"
            }
        ]
    
    async def generate_explanation(self, topic: str, context: str) -> str:
        """Generate AI explanation for a knowledge point"""
        prompt = f"""
        Explain the following topic in a clear and educational way:
        
        Topic: {topic}
        Context: {context}
        
        Provide a concise but comprehensive explanation suitable for learning.
        """
        
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1024
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                
                return f"Explanation for {topic}: AI service temporarily unavailable."
        except Exception as e:
            return f"Explanation for {topic}: {str(e)}"
    
    async def generate_mind_map(self, topic: str, content: str) -> Dict[str, Any]:
        """Generate mind map structure for a topic"""
        prompt = f"""
        Create a mind map structure for the following topic and content.
        
        Topic: {topic}
        Content: {content}
        
        Return a JSON structure representing the mind map:
        {{
            "center": "main topic",
            "branches": [
                {{
                    "label": "branch name",
                    "children": ["sub-topic 1", "sub-topic 2"]
                }}
            ]
        }}
        
        Return ONLY the JSON.
        """
        
        url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1024
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    text = text.replace("```json", "").replace("```", "").strip()
                    return json.loads(text)
                
                return self._default_mind_map(topic)
        except Exception:
            return self._default_mind_map(topic)
    
    def _default_mind_map(self, topic: str) -> Dict[str, Any]:
        """Default mind map structure"""
        return {
            "center": topic,
            "branches": [
                {"label": "Key Concept 1", "children": ["Detail A", "Detail B"]},
                {"label": "Key Concept 2", "children": ["Detail C", "Detail D"]},
                {"label": "Applications", "children": ["Example 1", "Example 2"]}
            ]
        }


# Global instance
ai_service = AIService()
