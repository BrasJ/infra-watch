import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar.tsx'
import Dashboard from './pages/Dashboard.tsx'
import Hosts from './pages/Hosts.tsx'
import Alerts from './pages/Alerts.tsx'

export default function App() {
    return (
        <div className="flex h-screen bg-gray-100 text-gray-900">
            <Sidebar />
            <div className="flex-1 p-6 overflow-y-auto">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/hosts" element={<Hosts />} />
                    <Route path="/alerts" element={<Alerts />} />
                </Routes>
            </div>
        </div>
    )
}
