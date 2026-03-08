# API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 版本**: `/api/v1`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 认证

目前 MVP 阶段无需认证，后续版本将添加 API Key 验证。

## 端点列表

### 1. 系统端点

#### 健康检查
```http
GET /health
```

**响应:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-08T18:00:00.000000"
}
```

#### 根路径
```http
GET /
```

**响应:**
```json
{
  "message": "Welcome to Project.MilanoLibrary API",
  "version": "2.0.3",
  "status": "running",
  "ai_enabled": true
}
```

---

### 2. 视频处理

#### 上传视频
```http
POST /api/v1/videos/upload
Content-Type: multipart/form-data

file: {video_file}
```

**参数:**
- `file` (required): 视频文件 (支持 MP4, AVI, MOV, MKV)

**响应 (200 OK):**
```json
{
  "id": "video_abc123",
  "filename": "lecture.mp4",
  "status": "uploaded",
  "message": "Video uploaded successfully. Processing will start soon."
}
```

**错误响应:**
- `400`: 不支持的文件类型
- `500`: 服务器内部错误

---

#### 获取视频状态
```http
GET /api/v1/videos/{video_id}/status
```

**路径参数:**
- `video_id` (required): 视频唯一标识

**响应 (200 OK):**
```json
{
  "id": "video_abc123",
  "filename": "lecture.mp4",
  "status": "analyzed",
  "created_at": "2026-03-08T17:00:00"
}
```

**状态说明:**
- `uploaded`: 已上传
- `analyzing`: AI 分析中
- `analyzed`: 分析完成
- `error`: 处理出错

**错误响应:**
- `404`: 视频不存在

---

#### 获取视频分析结果
```http
GET /api/v1/videos/{video_id}/analysis
```

**路径参数:**
- `video_id` (required): 视频唯一标识

**响应 - 分析完成 (200 OK):**
```json
{
  "id": "video_abc123",
  "filename": "lecture.mp4",
  "status": "analyzed",
  "sections": [
    {
      "id": "sec_001",
      "title": "Introduction",
      "start_time": 0,
      "end_time": 120,
      "summary": "Course introduction and overview"
    },
    {
      "id": "sec_002",
      "title": "Core Concepts",
      "start_time": 120,
      "end_time": 600,
      "summary": "Explanation of fundamental principles"
    }
  ],
  "summary": "This video covers the fundamentals..."
}
```

**响应 - 处理中 (200 OK):**
```json
{
  "id": "video_abc123",
  "status": "analyzing",
  "message": "Video is still being processed. Please check back later."
}
```

**错误响应:**
- `404`: 视频不存在

---

#### 触发视频分析
```http
POST /api/v1/videos/{video_id}/analyze
```

**路径参数:**
- `video_id` (required): 视频唯一标识

**响应 (200 OK):**
```json
{
  "id": "video_abc123",
  "status": "analyzed",
  "message": "Video analysis completed successfully",
  "sections_count": 4
}
```

**处理流程:**
1. 提取视频元数据 (FFmpeg)
2. 生成内容转录 (MVP: mock data)
3. 调用 Gemini AI 分析
4. 生成章节划分和摘要
5. 存储分析结果

**错误响应:**
- `404`: 视频不存在
- `500`: AI 分析失败

---

### 3. 知识点交互

#### 生成 AI 解释
```http
POST /api/v1/knowledge-points/{point_id}/explain
Content-Type: application/json

{
  "topic": "Neural Networks",
  "context": "Explanation of how neural networks work"
}
```

**路径参数:**
- `point_id` (required): 知识点标识

**请求体:**
- `topic` (required): 知识主题
- `context` (required): 上下文内容

**响应 (200 OK):**
```json
{
  "point_id": "sec_001",
  "topic": "Neural Networks",
  "explanation": "Neural networks are computational models inspired by biological neural networks..."
}
```

**错误响应:**
- `500`: 解释生成失败

---

#### 生成思维导图
```http
POST /api/v1/knowledge-points/{point_id}/mindmap
Content-Type: application/json

{
  "topic": "Neural Networks",
  "content": "Neural networks consist of layers of interconnected nodes..."
}
```

**路径参数:**
- `point_id` (required): 知识点标识

**请求体:**
- `topic` (required): 知识主题
- `content` (required): 详细内容

**响应 (200 OK):**
```json
{
  "point_id": "sec_001",
  "topic": "Neural Networks",
  "mind_map": {
    "center": "Neural Networks",
    "branches": [
      {
        "label": "Architecture",
        "children": ["Input Layer", "Hidden Layers", "Output Layer"]
      },
      {
        "label": "Training",
        "children": ["Forward Propagation", "Backpropagation", "Gradient Descent"]
      },
      {
        "label": "Applications",
        "children": ["Image Recognition", "NLP", "Game Playing"]
      }
    ]
  }
}
```

**错误响应:**
- `500`: 思维导图生成失败

---

## 数据模型

### Video 对象
```json
{
  "id": "string",           // 视频唯一标识
  "filename": "string",     // 原始文件名
  "content_type": "string", // MIME 类型
  "status": "string",       // 处理状态
  "created_at": "string",   // ISO 8601 时间戳
  "analysis": {             // 分析结果 (可选)
    "summary": "string",
    "sections": [Section]
  }
}
```

### Section 对象
```json
{
  "id": "string",           // 章节标识
  "title": "string",        // 章节标题
  "start_time": 0,          // 开始时间 (秒)
  "end_time": 120,          // 结束时间 (秒)
  "summary": "string"        // 章节摘要
}
```

### MindMap 对象
```json
{
  "center": "string",       // 中心主题
  "branches": [             // 分支列表
    {
      "label": "string",    // 分支标签
      "children": ["string"] // 子节点
    }
  ]
}
```

---

## 错误处理

### 错误响应格式
```json
{
  "detail": "Error message description"
}
```

### 错误码

| 状态码 | 含义 | 常见场景 |
|--------|------|----------|
| 200 | 成功 | 请求成功处理 |
| 400 | 请求参数错误 | 文件类型不支持、参数缺失 |
| 404 | 资源不存在 | 视频 ID 不存在 |
| 422 | 处理失败 | 视频分析失败 |
| 500 | 服务器错误 | AI 服务异常、内部错误 |

---

## 前端使用示例

### 上传视频
```javascript
const formData = new FormData();
formData.append('file', videoFile);

const response = await fetch('http://localhost:8000/api/v1/videos/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.id); // 视频 ID
```

### 获取分析结果
```javascript
const response = await fetch(
  `http://localhost:8000/api/v1/videos/${videoId}/analysis`
);

const data = await response.json();
console.log(data.sections); // 章节列表
```

### 生成 AI 解释
```javascript
const response = await fetch(
  `http://localhost:8000/api/v1/knowledge-points/${sectionId}/explain`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic: section.title,
      context: section.summary
    })
  }
);

const data = await response.json();
console.log(data.explanation); // AI 生成的解释
```

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.0.3 | 2026-03-08 | 添加知识点交互 API (/explain, /mindmap) |
| 2.0.2 | 2026-03-08 | 初始版本，视频上传和分析 API |

---
*API 文档版本: 2.0.3*
*更新日期: 2026-03-08*
*作者: Michel (Causally Tech)*
