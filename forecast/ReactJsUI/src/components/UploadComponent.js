import React, { useState } from 'react';
import { uploadCSV } from '../services/api';

const UploadComponent = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleUpload = async () => {
    if (!file) return;
    const response = await uploadCSV(file);
    setMessage(response.message || response.error);
  };

  return ( 
<div className="component-box">
      <h2>Upload Dataset</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="btn btn-blue">Upload</button>
      {message && <p className="mt-2 text-green-600">{message}</p>}
    </div>
  );
};

export default UploadComponent;