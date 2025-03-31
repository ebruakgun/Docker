import React from 'react';
import ReactDOM from 'react-dom/client';  // 'react-dom/client' ile import ediyoruz

import App from './App';

// React 18 için createRoot kullanımı
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
