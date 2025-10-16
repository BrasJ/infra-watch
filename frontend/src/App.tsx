import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar.tsx'
import Dashboard from './pages/Dashboard.tsx'
import Hosts from './pages/Hosts.tsx'
import Alerts from './pages/Alerts.tsx'
import MetricsDashboard from './pages/Metrics.tsx'

export default function App() {
    return (
        <div className="flex min-h-screen w-screen px-6 pl-8 bg-gray-100 text-gray-900">
            <Sidebar />
            <main className="flex-1 overflow-x-auto min-w-0">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/hosts" element={<Hosts />} />
                    <Route path="/alerts" element={<Alerts />} />
                    <Route path="/metrics" element={<MetricsDashboard />} />
                </Routes>
            </main>
        </div>
    )
}
