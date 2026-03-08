import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function KnowledgePoint({ section, videoId }) {
  const [showDetails, setShowDetails] = useState(false);
  const [explanation, setExplanation] = useState('');
  const [mindMap, setMindMap] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('video');

  const handleGetExplanation = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/knowledge-points/${section.id}/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: section.title,
          context: section.summary
        })
      });
      const data = await response.json();
      setExplanation(data.explanation);
      setActiveTab('explanation');
    } catch (error) {
      setExplanation('获取解释失败，请稍后重试');
    }
    setLoading(false);
  };

  const handleGetMindMap = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/knowledge-points/${section.id}/mindmap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: section.title,
          content: section.summary
        })
      });
      const data = await response.json();
      setMindMap(data.mind_map);
      setActiveTab('mindmap');
    } catch (error) {
      console.error('Mind map error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="knowledge-point">
      <div 
        className="knowledge-header"
        onClick={() => setShowDetails(!showDetails)}
      >
        <h4>{section.title}</h4>
        <span className="time">{section.start_time}s - {section.end_time}s</span>
        <span className="toggle">{showDetails ? '▼' : '▶'}</span>
      </div>
      
      <p className="summary">{section.summary}</p>
      
      {showDetails && (
        <div className="knowledge-details">
          <div className="tabs">
            <button 
              className={activeTab === 'video' ? 'active' : ''}
              onClick={() => setActiveTab('video')}
            >
              🎬 视频片段
            </button>
            <button 
              className={activeTab === 'explanation' ? 'active' : ''}
              onClick={handleGetExplanation}
              disabled={loading}
            >
              🤖 AI解释
            </button>
            <button 
              className={activeTab === 'mindmap' ? 'active' : ''}
              onClick={handleGetMindMap}
              disabled={loading}
            >
              🧠 思维导图
            </button>
          </div>
          
          <div className="tab-content">
            {activeTab === 'video' && (
              <div className="video-clip">
                <p>📹 视频片段: {section.start_time}s - {section.end_time}s</p>
                <p className="hint">(视频播放器将在后续版本添加)</p>
              </div>
            )}
            
            {activeTab === 'explanation' && (
              <div className="ai-explanation">
                {loading ? (
                  <p>🤖 AI 正在生成解释...</p>
                ) : (
                  <div className="explanation-text">
                    {explanation}
                  </div>
                )}
              </div>
            )}
            
            {activeTab === 'mindmap' && (
              <div className="mind-map">
                {loading ? (
                  <p>🧠 正在生成思维导图...</p>
                ) : mindMap ? (
                  <div className="mind-map-visual">
                    <h5>{mindMap.center}</h5>
                    <div className="branches">
                      {mindMap.branches?.map((branch, idx) => (
                        <div key={idx} className="branch">
                          <strong>{branch.label}</strong>
                          <ul>
                            {branch.children?.map((child, cidx) => (
                              <li key={cidx}>{child}</li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p>点击上方按钮生成思维导图</p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default KnowledgePoint;
