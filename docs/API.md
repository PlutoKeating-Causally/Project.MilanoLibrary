# API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 版本**: `/api/v1`
- **文档**: `/docs` (Swagger UI)

## 认证

所有 API 请求需要在 Header 中携带：
```
Authorization: Bearer {api_key}
```

## 端点列表

### 1. 视频处理

#### 上传视频
```http
POST /api/v1/videos/upload
Content-Type: multipart/form-data

file: {video_file}
```

**响应:**
```json
{
  "id": "video_123",
  "filename": "lecture.mp4",
  "status": "processing",
  "created_at": "2026-03-08T17:00:00Z"
}
```

#### 获取视频状态
```http
GET /api/v1/videos/{video_id}/status
```

#### 获取视频分析结果
```http
GET /api/v1/videos/{video_id}/analysis
```

**响应:**
```json
{
  "video_id": "video_123",
  "sections": [
    {
      "id": "sec_001",
      "title": "Introduction",
      "start_time": 0,
      "end_time": 120,
      "summary": "Course introduction",
      "key_points": ["point_1", "point_2"]
    }
  ]
}
```

### 2. 知识点交互

#### 获取知识点详情
```http
GET /api/v1/knowledge-points/{point_id}
```

**响应:**
```json
{
  "id": "point_001",
  "title": "Neural Networks",
  "content": "...",
  "video_clip": {
    "start": 300,
    "end": 305,
    "url": "/clips/point_001.mp4"
  },
  "mind_map": {...},
  "ai_explanation": "..."
}
```

#### 获取 AI 解释
```http
POST /api/v1/knowledge-points/{point_id}/explain
{
  "question": "What is backpropagation?"
}
```

#### 生成思维导图
```http
POST /api/v1/knowledge-points/{point_id}/mindmap
```

### 3. 报告生成

#### 生成学习报告
```http
POST /api/v1/reports/generate
{
  "video_id": "video_123",
  "format": "html"  // or "pdf"
}
```

---

## 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 422 | 处理失败 |
| 500 | 服务器错误 |

---
*API 设计: Michel*
*日期: 2026-03-08*
