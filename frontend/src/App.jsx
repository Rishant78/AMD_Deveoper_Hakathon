import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_BASE_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'https://amd-deveoper-hakathon.onrender.com';

function App() {
  // Application State
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState('');
  const [status, setStatus] = useState('idle'); // idle | uploading | processing | success | error
  const [error, setError] = useState('');

  // Processing Stepper
  const [currentStep, setCurrentStep] = useState(1);
  const [steps, setSteps] = useState([
    { id: 1, label: 'Uploading video file to server', status: 'pending' },
    { id: 2, label: 'Extracting representative frames', status: 'pending' },
    { id: 3, label: 'Captioning key frames via Vision AI', status: 'pending' },
    { id: 4, label: 'Generating overall description & style rewrites', status: 'pending' },
  ]);

  // API Results
  const [result, setResult] = useState(null);
  const [activeStyle, setActiveStyle] = useState('formal');
  const [zoomFrame, setZoomFrame] = useState(null);
  const [toastMsg, setToastMsg] = useState('');

  const fileInputRef = useRef(null);

  // Auto-updating steps status when currentStep changes
  useEffect(() => {
    setSteps(prevSteps =>
      prevSteps.map(step => {
        if (step.id < currentStep) return { ...step, status: 'completed' };
        if (step.id === currentStep) return { ...step, status: 'active' };
        return { ...step, status: 'pending' };
      })
    );
  }, [currentStep]);

  // Auto-hide toast messages
  useEffect(() => {
    if (toastMsg) {
      const timer = setTimeout(() => setToastMsg(''), 3000);
      return () => clearTimeout(timer);
    }
  }, [toastMsg]);

  // Handle Drag & Drop Events
  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processSelectedFile(e.target.files[0]);
    }
  };

  const processSelectedFile = (selectedFile) => {
    // Validate file type
    if (!selectedFile.type.startsWith('video/')) {
      setError('Please select a valid video file.');
      return;
    }
    setFile(selectedFile);
    setVideoUrl(URL.createObjectURL(selectedFile));
    setError('');
  };

  // Upload and Caption Pipeline Trigger
  const startPipeline = async () => {
    if (!file) return;

    setStatus('uploading');
    setCurrentStep(1);
    setError('');

    // Setup visual simulated milestones timer for subsequent processing phases
    let stepInterval = null;

    try {
      // 1. Upload Video file to server
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error('Video upload failed. Check file dimensions or server status.');
      }

      const uploadData = await uploadResponse.json();

      // 2. Upload completed, start processing
      setStatus('processing');
      setCurrentStep(2);

      // Start timing transitions for stepper visual feedback
      // We expect the Fireworks vision API calls to take around 10-25 seconds depending on frame count
      let elapsedSeconds = 0;
      stepInterval = setInterval(() => {
        elapsedSeconds += 1;
        if (elapsedSeconds === 4) {
          setCurrentStep(3); // Transition to captioning frames
        } else if (elapsedSeconds === 15) {
          setCurrentStep(4); // Transition to summarizing and generating styles
        }
      }, 1000);

      // Trigger FastAPI unified caption pipeline
      const captionResponse = await fetch(`${API_BASE_URL}/caption`, {
        method: 'POST',
      });

      clearInterval(stepInterval);

      if (!captionResponse.ok) {
        throw new Error('Error processing captions. Check your Fireworks API key.');
      }

      const pipelineResult = await captionResponse.json();

      if (!pipelineResult.success) {
        throw new Error(pipelineResult.error || 'Failed to analyze video contents.');
      }

      // Mark all steps as complete and display results
      setCurrentStep(5);
      setResult(pipelineResult);
      setStatus('success');
    } catch (err) {
      if (stepInterval) clearInterval(stepInterval);
      setError(err.message || 'An unexpected server error occurred.');
      setStatus('error');
    }
  };

  // Reset to initial state
  const resetApp = () => {
    setFile(null);
    setVideoUrl('');
    setStatus('idle');
    setResult(null);
    setError('');
    setCurrentStep(1);
  };

  // Copy to Clipboard Helpers
  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text);
    setToastMsg(`${label} copied to clipboard! 📋`);
  };

  // Export functions
  const downloadTextFile = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleExportTXT = () => {
    if (!result) return;
    const txtContent = `AMD CAPTIVATE AI - VIDEO CAPTION REPORT
File Name: ${result.video_info?.filename || 'video.mp4'}
Duration: ${result.video_info?.duration || 0} seconds

=======================================================
OVERALL CAPTION:
${result.video_caption}

=======================================================
STYLED CAPTIONS:
Formal: 
${result.styles?.formal}

Sarcastic: 
${result.styles?.sarcastic}

Humorous-Tech: 
${result.styles?.humorous_tech}

Humorous-NonTech: 
${result.styles?.humorous_non_tech}

=======================================================
KEYFRAME TIMELINE DETAILS:
${result.frames?.map(f => `[${f.timestamp_formatted}] - ${f.caption}`).join('\n')}
`;
    downloadTextFile(txtContent, `${result.video_info?.filename || 'captions'}_report.txt`);
  };

  const handleExportJSON = () => {
    if (!result) return;
    const jsonString = JSON.stringify(result, null, 2);
    downloadTextFile(jsonString, `${result.video_info?.filename || 'captions'}_data.json`);
  };

  const handleExportSRT = () => {
    if (!result || !result.frames) return;

    // Subtitle formatter helper: converts seconds to HH:MM:SS,mmm
    const formatSRTTime = (seconds) => {
      const pad = (num, size) => ('000' + num).slice(-size);
      const hrs = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      const ms = Math.floor((seconds % 1) * 1000);
      return `${pad(hrs, 2)}:${pad(mins, 2)}:${pad(secs, 2)},${pad(ms, 3)}`;
    };

    let srtContent = '';
    const frames = result.frames;
    const duration = result.video_info?.duration || 0;

    for (let i = 0; i < frames.length; i++) {
      const start = frames[i].timestamp_seconds;
      // Set end time to next frame timestamp, or start + 4s (or video end) if last frame
      const end = i < frames.length - 1
        ? frames[i + 1].timestamp_seconds
        : Math.min(start + 4.0, duration);

      srtContent += `${i + 1}\n`;
      srtContent += `${formatSRTTime(start)} --> ${formatSRTTime(end)}\n`;
      srtContent += `${frames[i].caption || 'Keyframe event'}\n\n`;
    }

    downloadTextFile(srtContent, `${result.video_info?.filename || 'captions'}.srt`);
    setToastMsg('Subtitles downloaded as SRT! 🎬');
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1 className="brand-title">
          AMD Captivate AI <span className="brand-badge">Vision</span>
        </h1>
        <div className="model-info-pill">Qwen 3.7 Plus Vision (Serverless)</div>
      </header>

      {/* Main Panel Content */}
      <main className="main-content">
        {status === 'idle' && (
          <div className="glass-card">
            {!file ? (
              <div
                className="upload-container"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="upload-icon">📤</div>
                <h3>Upload Video File</h3>
                <p>Drag and drop your MP4, AVI, or MOV video here, or click to browse</p>
                <button className="btn-primary">Browse System Files</button>
                <input
                  type="file"
                  ref={fileInputRef}
                  className="file-input"
                  accept="video/*"
                  onChange={handleFileChange}
                />
              </div>
            ) : (
              <div className="upload-preview-container" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
                <video src={videoUrl} controls style={{ maxWidth: '100%', maxHeight: '360px', borderRadius: '8px', border: '1px solid var(--border-color)' }} />
                <div style={{ textAlign: 'center' }}>
                  <p style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{file.name}</p>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  <button className="btn-outline" onClick={() => setFile(null)}>Choose Another</button>
                  <button className="btn-primary" onClick={startPipeline}>Process Video</button>
                </div>
              </div>
            )}
          </div>
        )}

        {(status === 'uploading' || status === 'processing') && (
          <div className="glass-card processing-container">
            <div className="spinner-ring">
              <div className="spinner-outer"></div>
              <div className="spinner-inner"></div>
              <div className="spinner-logo">AI</div>
            </div>

            <div style={{ textAlign: 'center' }}>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', marginBottom: '0.5rem' }}>
                {status === 'uploading' ? 'Uploading Video Content...' : 'Analyzing Video Timeline...'}
              </h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                {status === 'uploading'
                  ? 'Transferring video file to FastAPI processing server...'
                  : 'Fireworks Vision model is parsing representative frame components...'}
              </p>
            </div>

            <div className="stepper-list">
              {steps.map(step => (
                <div key={step.id} className={`step-item ${step.status}`}>
                  <div className="step-bullet">
                    {step.status === 'completed' ? '✓' : step.id}
                  </div>
                  <div className="step-text">{step.label}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {status === 'error' && (
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', padding: '3rem 2rem' }}>
            <div style={{ fontSize: '3rem', color: 'var(--danger)' }}>⚠️</div>
            <div style={{ textAlign: 'center' }}>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', color: 'var(--danger)', marginBottom: '0.5rem' }}>Pipeline Processing Error</h3>
              <p style={{ color: 'var(--text-secondary)', maxWidth: '500px' }}>{typeof error === 'string' ? error : 'An unexpected error occurred.'}</p>
            </div>
            <button className="btn-primary" onClick={resetApp}>Try Again</button>
          </div>
        )}

        {status === 'success' && result && (
          <div className="dashboard-grid">

            {/* Sidebar Column: Video and Timeline */}
            <div className="dashboard-sidebar">

              {/* Video Info Section */}
              <div className="glass-card">
                <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.25rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                  Video Metadata
                </h3>
                {videoUrl && (
                  <video src={videoUrl} controls style={{ width: '100%', borderRadius: '8px', border: '1px solid var(--border-color)', marginBottom: '1rem' }} />
                )}
                <div className="metadata-grid">
                  <div className="metadata-item">
                    <div className="metadata-label">Duration</div>
                    <div className="metadata-value">{result.video_info?.duration || 0}s</div>
                  </div>
                  <div className="metadata-item">
                    <div className="metadata-label">FPS</div>
                    <div className="metadata-value">{result.video_info?.fps || 0}</div>
                  </div>
                  <div className="metadata-item">
                    <div className="metadata-label">Frames Read</div>
                    <div className="metadata-value">{result.video_info?.total_frames || 0}</div>
                  </div>
                  <div className="metadata-item">
                    <div className="metadata-label">Keyframes</div>
                    <div className="metadata-value">{result.frames_used || 0}</div>
                  </div>
                </div>
              </div>

              {/* Frames Timeline list */}
              <div className="glass-card">
                <div className="timeline-header">
                  <h3>Scene Timeline</h3>
                  <span className="timeline-count">{result.frames?.length || 0} frames</span>
                </div>
                <div className="timeline-scroll">
                  {result.frames?.map((frame, idx) => (
                    <div key={idx} className="timeline-card">
                      <div
                        className="timeline-thumbnail-container"
                        onClick={() => setZoomFrame(frame)}
                        title="Click to zoom frame"
                      >
                        <img
                          src={`${API_BASE_URL}${frame.url}`}
                          alt={`Frame at ${frame.timestamp_formatted}`}
                          className="timeline-thumbnail"
                        />
                        <span className="timeline-time-badge">{frame.timestamp_formatted}</span>
                      </div>
                      <div className="timeline-details">
                        <div className="timeline-time-label">T + {frame.timestamp_formatted}</div>
                        <p className="timeline-caption-text">{typeof frame.caption === 'string' ? frame.caption : 'Caption unavailable'}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Main Results Column: Overall + Styled Captions */}
            <div className="dashboard-main">

              {/* Overall Caption card */}
              <div className="glass-card summary-container">
                <div className="summary-heading">
                  <span style={{ fontSize: '1.2rem' }}>📝</span> Overall Video Summary
                </div>
                <p className="summary-text">"{typeof result.video_caption === 'string' ? result.video_caption : 'Caption unavailable'}"</p>
                <div className="card-actions">
                  <button
                    className="btn-secondary"
                    onClick={() => copyToClipboard(result.video_caption, 'Overall Summary')}
                  >
                    <span>📋</span> Copy Summary
                  </button>
                </div>
              </div>

              {/* Styles card container */}
              <div className="glass-card styles-section">
                <div className="results-header-box">
                  <h3 style={{ margin: 0 }}>Multi-Style Captioning</h3>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Rewritten by Fireworks AI</span>
                </div>

                {/* Styled tab switcher */}
                <div className="styles-tab-bar">
                  <button
                    className={`tab-btn ${activeStyle === 'formal' ? 'active' : ''}`}
                    onClick={() => setActiveStyle('formal')}
                  >
                    Formal
                  </button>
                  <button
                    className={`tab-btn ${activeStyle === 'sarcastic' ? 'active' : ''}`}
                    onClick={() => setActiveStyle('sarcastic')}
                  >
                    Sarcastic
                  </button>
                  <button
                    className={`tab-btn ${activeStyle === 'humorous_tech' ? 'active' : ''}`}
                    onClick={() => setActiveStyle('humorous_tech')}
                  >
                    Humorous-Tech
                  </button>
                  <button
                    className={`tab-btn ${activeStyle === 'humorous_non_tech' ? 'active' : ''}`}
                    onClick={() => setActiveStyle('humorous_non_tech')}
                  >
                    Humorous-NonTech
                  </button>
                </div>

                {/* Styles preview display */}
                <div className={`style-display-card ${activeStyle}`}>
                  <div className="style-card-badge">{activeStyle.replace('_', ' ')}</div>
                  <p className="style-content">
                    "{result.styles && typeof result.styles[activeStyle] === 'string' ? result.styles[activeStyle] : 'No caption loaded'}"
                  </p>
                  <div className="card-actions">
                    <button
                      className="btn-secondary"
                      onClick={() => copyToClipboard(result.styles[activeStyle], `${activeStyle.charAt(0).toUpperCase() + activeStyle.slice(1).replace('_', ' ')} caption`)}
                    >
                      <span>📋</span> Copy Caption
                    </button>
                  </div>
                </div>
              </div>

              {/* bottom export actions */}
              <div className="action-bar">
                <button className="btn-outline" onClick={resetApp}>Analyze New Video</button>
                <div className="action-bar-right">
                  <button className="btn-secondary" onClick={handleExportJSON}>
                    <span>⚙️</span> Export JSON
                  </button>
                  <button className="btn-secondary" onClick={handleExportSRT}>
                    <span>🎬</span> Export SRT Subtitles
                  </button>
                  <button className="btn-primary" onClick={handleExportTXT}>
                    <span>📥</span> Download TXT Report
                  </button>
                </div>
              </div>

            </div>

          </div>
        )}
      </main>

      {/* Frame zoom Modal */}
      {zoomFrame && (
        <div className="modal-overlay" onClick={() => setZoomFrame(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={() => setZoomFrame(null)}>×</button>
            <img
              src={`${API_BASE_URL}${zoomFrame.url}`}
              alt={`Frame at ${zoomFrame.timestamp_formatted}`}
              className="modal-image"
            />
            <div className="modal-footer">
              <div style={{ color: 'var(--primary)', fontFamily: 'var(--font-display)', fontWeight: 700, marginBottom: '0.25rem' }}>
                Keyframe Timestamp: T + {zoomFrame.timestamp_formatted}
              </div>
              <p style={{ color: 'var(--text-primary)', fontSize: '1rem', lineHeight: '1.4' }}>
                {zoomFrame.caption}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toastMsg && (
        <div className="toast-msg">
          {toastMsg}
        </div>
      )}
    </div>
  );
}

export default App;
