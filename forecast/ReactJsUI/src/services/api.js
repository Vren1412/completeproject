const API_URL = 'http://localhost:5000';

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });
  return await response.json();
};

export const getForecast = async (productId) => {
  const response = await fetch(`${API_URL}/forecast`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId })
  });
  return await response.json();
};
