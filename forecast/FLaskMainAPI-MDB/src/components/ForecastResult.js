// src/components/ForecastResult.js
import React from 'react';
import '../styles/images.css';

const ForecastResult = ({ productId, metrics }) => {
  if (!productId || !metrics) return null;

  const lineChart = `http://localhost:5000/forecast_outputs/${productId}_line_chart.png`;
  const barChart = `http://localhost:5000/forecast_outputs/${productId}_bar_chart.png`;
  const heatmap = `http://localhost:5000/forecast_outputs/${productId}_heatmap.png`;

  return (
    <div className="component-box-results">
      <h3 className="text-md font-bold">Accuracy Metrics</h3>
      <p>MAE: {metrics.mae}</p>
      <p>MSE: {metrics.mse}</p>
      <p>R² Score: {metrics.r2_score}</p>

      {/* <h3 className="text-md font-bold mt-4">Graphs</h3>
      <img alt="Line Chart" className="rounded mb-2" src={lineChart} />
      <img alt="Bar Chart" className="rounded mb-2" src={barChart} />
      <img alt="Heatmap" className="rounded" src={heatmap} />
      <h3 className="text-xl font-semibold text-gray-800 mt-6 mb-4 border-b pb-2">Forecast Graphs</h3> */}

<div className="image-grid">
  {[{ src: lineChart, label: 'Line Chart' },
    { src: barChart, label: 'Bar Chart' },
    { src: heatmap, label: 'Heatmap' }].map((img, idx) => (
    <div
      key={idx}
      className="image-card"
      onClick={() => window.open(img.src, '_blank')}
    >
      <img src={img.src} alt={img.label} />
      <p className="image-label">{img.label}</p>
    </div>
  ))}
</div>
    </div>
  );
};

export default ForecastResult;
