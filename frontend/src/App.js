import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import VideoList from './components/VideoList';
import './App.css';

function App() {
  const [refreshList, setRefreshList] = useState(false);

  const handleUploadSuccess = () => {
    setRefreshList(!refreshList);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📚 Project.MilanoLibrary</h1>
        <p>AI 驱动的视频学习平台</p>
      </header>

      <main className="App-main">
        <section className="upload-section">
          <h2>上传视频</h2>
          <VideoUpload onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="videos-section">
          <h2>视频列表</h2>
          <VideoList key={refreshList} />
        </section>
      </main>

      <footer className="App-footer">
        <p>© 2026 Causally Tech - Project.MilanoLibrary V2</p>
      </footer>
    </div>
  );
}

export default App;
