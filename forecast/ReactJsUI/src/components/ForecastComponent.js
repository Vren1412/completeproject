// src/components/ForecastComponent.js
import React, { useState } from 'react';
import { getForecast } from '../services/api';
import ForecastResult from './ForecastResult';

const ForecastComponent = () => {
  const [productId, setProductId] = useState('');
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState('');

  const handleForecast = async () => {
    const response = await getForecast(productId);
    if (response.error) return setError(response.error);
    setMetrics(response.metrics);
    setError('');
  };

  return (
    <div className="component-box">
      <h2 className="text-lg font-semibold mb-2">Forecast Product Sales</h2>
      <input
        type="text"
        placeholder="Enter Product ID"
        value={productId}
        onChange={(e) => setProductId(e.target.value)}
        
      />
      <button onClick={handleForecast} className="btn btn-green">Run Forecast</button>

      {error && <p className="mt-2 text-red-500">{error}</p>}

      {/* Inject Forecast Result */}
      <ForecastResult productId={productId} metrics={metrics} />
    </div>
  );
};

export default ForecastComponent;
