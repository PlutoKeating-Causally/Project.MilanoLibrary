import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function VideoUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // 验证文件类型
      const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setMessage('❌ 只支持 MP4, AVI, MOV, MKV 格式');
        return;
      }
      setFile(selectedFile);
      setMessage('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('❌ 请选择视频文件');
      return;
    }

    setUploading(true);
    setMessage('📤 正在上传...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/v1/videos/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ 上传成功! ID: ${data.id}`);
        setFile(null);
        onUploadSuccess();
        
        // 自动触发分析
        setTimeout(() => {
          analyzeVideo(data.id);
        }, 1000);
      } else {
        setMessage(`❌ 上传失败: ${data.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setMessage(`❌ 上传失败: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const analyzeVideo = async (videoId) => {
    setMessage('🤖 AI 正在分析视频...');
    try {
      const response = await fetch(`${API_URL}/api/v1/videos/${videoId}/analyze`, {
        method: 'POST',
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('✅ 分析完成!');
        onUploadSuccess();
      }
    } catch (error) {
      console.error('Analysis error:', error);
    }
  };

  return (
    <div className="video-upload">
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          disabled={uploading}
        />
        {file && (
          <p className="file-info">
            已选择: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
          </p>
        )}
        <button type="submit" disabled={uploading || !file}>
          {uploading ? '上传中...' : '上传并分析'}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default VideoUpload;
