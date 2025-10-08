import { useEffect, useState } from 'react'
import { fetchAlerts, acknowledgeAlert, deleteAlert } from '../lib/api'
import type { Alert } from '../types/alert'

export default function Alerts() {
    const [alerts, setAlerts] = useState<Alert[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchAlerts()
            .then(data => setAlerts(data))
            .catch(err => console.error("Failed to fetch alerts:", err))
            .finally(() => setLoading(false))
    }, [])

    const handleAcknowledge = async (id: number) => {
        try {
            const updated = await acknowledgeAlert(id)
            setAlerts(prev => prev.map(a => a.id === id ? updated : a))
        } catch (e) {
            console.error("Failed to acknowledge alert", e)
        }
    }

    const handleDelete = async (id: number) => {
        try {
            await deleteAlert(id)
            setAlerts(prev => prev.filter(a => a.id !== id))
        } catch (e) {
            console.error("Failed to delete alert", e)
        }
    }

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">System Alerts</h1>
            {loading ? (
                <p>Loading alerts...</p>
            ) : (
                <table className="min-w-full border border-gray-300">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="px-4 py-2 text-left">Message</th>
                            <th className="px-4 py-2 text-left">Severity</th>
                            <th className="px-4 py-2 text-left">Type</th>
                            <th className="px-4 py-2 text-left">Ack</th>
                            <th className="px-4 py-2 text-left">Created</th>
                            <th className="px-4 py-2 text-left">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alerts.map(alert => (
                            <tr key={alert.id} className="border-t">
                                <td className="px-4 py-2">{alert.message}</td>
                                <td className="px-4 py-2">{alert.severity}</td>
                                <td className="px-4 py-2">{alert.type}</td>
                                <td className="px-4 py-2">
                                    {alert.acknowledged ? '✅' : '❌'}
                                </td>
                                <td className="px-4 py-2">
                                    {new Date(alert.created_at).toLocaleString()}
                                </td>
                                <td className="px-4 py-2 space-x-2">
                                    {!alert.acknowledged && (
                                        <button
                                            className="text-blue-600 hover:underline"
                                            onClick={() => handleAcknowledge(alert.id)}
                                        >
                                            Acknowledge
                                        </button>
                                    )}
                                    <button
                                        className="text-red-600 hover:underline"
                                        onClick={() => handleDelete(alert.id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    )
}
