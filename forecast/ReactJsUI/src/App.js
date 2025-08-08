
import React from 'react';
import UploadComponent from './components/UploadComponent';
import ForecastComponent from './components/ForecastComponent';
import MenuComponent from './components/MenuComponent';
import './styles/global.css';
function App() {
  return ( 
     <div className="p-6">
      <MenuComponent />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
        <UploadComponent />
        <ForecastComponent />
      </div>
    </div>
  );
}

export default App;