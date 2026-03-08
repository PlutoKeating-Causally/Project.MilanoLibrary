import React, { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function VideoList() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    // MVP: 直接显示空列表，实际应该从后端获取
    setLoading(false);
  }, []);

  const fetchVideoDetails = async (videoId) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/videos/${videoId}/analysis`);
      const data = await response.json();
      if (response.ok) {
        setSelectedVideo(data);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  const getStatusEmoji = (status) => {
    const emojis = {
      'uploaded': '📤',
      'processing': '⏳',
      'analyzing': '🤖',
      'analyzed': '✅',
      'error': '❌'
    };
    return emojis[status] || '❓';
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="video-list">
      {videos.length === 0 ? (
        <div className="empty-state">
          <p>🎥 暂无视频</p>
          <p>请上传第一个视频开始体验!</p>
        </div>
      ) : (
        <div className="videos-grid">
          {videos.map((video) => (
            <div key={video.id} className="video-card">
              <div className="video-status">
                {getStatusEmoji(video.status)}
              </div>
              <h3>{video.filename}</h3>
              <p>状态: {video.status}</p>
              <p>上传时间: {new Date(video.created_at).toLocaleString()}</p>
              {video.status === 'analyzed' && (
                <button onClick={() => fetchVideoDetails(video.id)}>
                  查看分析
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {selectedVideo && (
        <div className="video-modal">
          <div className="modal-content">
            <h3>📊 分析结果: {selectedVideo.filename}</h3>
            <div className="summary">
              <h4>摘要</h4>
              <p>{selectedVideo.summary}</p>
            </div>
            
            <div className="sections">
              <h4>章节</h4>
              {selectedVideo.sections?.map((section) => (
                <div key={section.id} className="section-item">
                  <h5>{section.title}</h5>
                  <p>{section.summary}</p>
                  <p className="time">
                    {section.start_time}s - {section.end_time}s
                  </p>
                </div>
              ))}
            </div>
            
            <button onClick={() => setSelectedVideo(null)}>关闭</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default VideoList;
