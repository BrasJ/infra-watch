import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Route } from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import MetricsDashboard from "./pages/Metrics.tsx";


ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
            <Route path="/metrics" element={<MetricsDashboard />} />
        </BrowserRouter>
    </React.StrictMode>
)