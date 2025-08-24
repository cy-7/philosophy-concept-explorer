import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [concepts, setConcepts] = useState([]);
  const [selectedConcept, setSelectedConcept] = useState('');
  const [explanations, setExplanations] = useState({});
  const [chartImage, setChartImage] = useState(null);
  const [chartLoading, setChartLoading] = useState(false);
  const [llmStatus, setLlmStatus] = useState({ llm_available: false, status: 'offline' });
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [useAI, setUseAI] = useState(true);

  useEffect(() => {
    fetchConcepts();
    checkLLMStatus();
  }, []);

  const fetchConcepts = async () => {
    try {
      const response = await fetch('/api/concepts');
      const data = await response.json();
      setConcepts(data.concepts);
      if (data.concepts.length > 0) {
        setSelectedConcept(data.concepts[0]);
      }
    } catch (error) {
      console.error('获取概念列表失败:', error);
      // 使用测试数据
      setConcepts(['自由', '理性', '意识', '正义', '真理']);
      setSelectedConcept('自由');
    }
  };

  const checkLLMStatus = async () => {
    try {
      const response = await fetch('/api/llm_status');
      const data = await response.json();
      setLlmStatus(data);
    } catch (error) {
      console.error('检查LLM状态失败:', error);
      setLlmStatus({ llm_available: false, status: 'error' });
    }
  };

  const handleConceptChange = async (concept) => {
    setSelectedConcept(concept);
    setChartImage(null);
    setAiAnalysis(null);
    
    if (concept) {
      await fetchExplanations(concept);
      await fetchSemanticShiftChart(concept);
    }
  };

  const fetchExplanations = async (concept) => {
    try {
      const response = await fetch(`/api/explain/${concept}?use_ai=${useAI}`);
      const data = await response.json();
      setExplanations(data.explanations || {});
      
      if (data.ai_generated && data.semantic_shift) {
        setAiAnalysis(data.semantic_shift);
      }
    } catch (error) {
      console.error('获取概念解释失败:', error);
      // 使用测试数据
      setExplanations({
        'Ancient Greece': `${concept}在古希腊时期的基本含义和特点。`,
        'Medieval': `${concept}在中世纪时期的发展变化。`,
        'Modern': `${concept}在近代的现代转向。`,
        'Contemporary': `${concept}在当代的最新发展。`
      });
    }
  };

  const fetchSemanticShiftChart = async (concept) => {
    if (!concept) return;
    
    setChartLoading(true);
    try {
      const response = await fetch(`/api/semantic_shift/${concept}?use_ai=${useAI}`);
      if (response.ok) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setChartImage(imageUrl);
      } else {
        console.error('获取图表失败:', response.status);
      }
    } catch (error) {
      console.error('获取语义漂移图表失败:', error);
    } finally {
      setChartLoading(false);
    }
  };

  const performAIAnalysis = async () => {
    if (!selectedConcept) return;
    
    setAiLoading(true);
    try {
      // 显示详细的加载提示
      alert(`开始AI分析概念: ${selectedConcept}\n\n注意：当前使用CPU模式\n\n首次分析可能需要5-10分钟，请耐心等待。\n\n分析完成后结果会自动保存，下次查询会更快。\n\n要启用GPU加速，需要重新编译LLaMA.cpp支持CUDA。`);
      
      const response = await fetch(`/api/ai_analyze/${selectedConcept}`);
      const data = await response.json();
      
      if (data.success) {
        setAiAnalysis(data.data);
        // 重新获取图表（使用AI数据）
        await fetchSemanticShiftChart(selectedConcept);
        // 重新获取解释
        await fetchExplanations(selectedConcept);
        alert(`AI分析完成！概念 "${selectedConcept}" 的语义漂移分析已生成。`);
      } else {
        alert(`AI分析失败: ${data.error}`);
      }
    } catch (error) {
      console.error('AI分析失败:', error);
      alert('AI分析请求失败，请检查网络连接或LLM服务状态');
    } finally {
      setAiLoading(false);
    }
  };

  const toggleAI = () => {
    setUseAI(!useAI);
    if (selectedConcept) {
      handleConceptChange(selectedConcept);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Philosophy Concept Explorer</h1>
        <div className="llm-status">
          <span className={`status-indicator ${llmStatus.status}`}>
            LLM: {llmStatus.status.toUpperCase()}
          </span>
          <button onClick={checkLLMStatus} className="refresh-btn">
            🔄
          </button>
        </div>
      </header>

      <main className="App-main">
        <div className="control-panel">
          <div className="concept-selector">
            <label htmlFor="concept-select">选择哲学概念:</label>
            <select
              id="concept-select"
              value={selectedConcept}
              onChange={(e) => handleConceptChange(e.target.value)}
            >
              {concepts.map((concept) => (
                <option key={concept} value={concept}>
                  {concept}
                </option>
              ))}
            </select>
          </div>

          <div className="ai-controls">
            <label className="ai-toggle">
              <input
                type="checkbox"
                checked={useAI}
                onChange={toggleAI}
              />
              使用AI分析
            </label>
            
            {useAI && llmStatus.llm_available && (
              <button
                onClick={performAIAnalysis}
                disabled={aiLoading}
                className="ai-analyze-btn"
              >
                {aiLoading ? 'AI分析中...' : '🔄 重新AI分析'}
              </button>
            )}
          </div>
        </div>

        {selectedConcept && (
          <div className="content-area">
            <div className="explanations-section">
              <h2>概念解释: {selectedConcept}</h2>
              <div className="explanations-grid">
                {Object.entries(explanations).map(([era, explanation]) => (
                  <div key={era} className="era-explanation">
                    <h3>{era}</h3>
                    <p>{explanation}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="chart-section">
              <h2>语义漂移分析</h2>
              <div className="chart-container">
                {chartLoading ? (
                  <div className="chart-loading">生成图表中...</div>
                ) : chartImage ? (
                  <img
                    src={chartImage}
                    alt={`${selectedConcept} 语义漂移图表`}
                    className="chart-image"
                  />
                ) : (
                  <div className="chart-placeholder">
                    图表功能开发中...
                  </div>
                )}
              </div>
            </div>

            {aiAnalysis && aiAnalysis.ai_generated && (
              <div className="ai-insights-section">
                <h2>AI分析洞察</h2>
                <div className="ai-insights">
                  <div className="insight-item">
                    <h3>整体趋势</h3>
                    <p>{aiAnalysis.overall_trend}</p>
                  </div>
                  <div className="insight-item">
                    <h3>关键洞察</h3>
                    <ul>
                      {aiAnalysis.key_insights?.map((insight, index) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                  {aiAnalysis.philosophers && (
                    <div className="insight-item">
                      <h3>代表性哲学家</h3>
                      <div className="philosophers-grid">
                        {Object.entries(aiAnalysis.philosophers).map(([era, philosophers]) => (
                          <div key={era} className="era-philosophers">
                            <h4>{era}</h4>
                            <p>{philosophers.join(', ')}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
