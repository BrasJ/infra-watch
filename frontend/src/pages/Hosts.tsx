import { useEffect, useState } from 'react'
import { Host } from '../types/host'
import { fetchHosts } from '../lib/api.ts'

export default function Hosts() {
    const [hosts, setHosts] = useState<Host[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchHosts()
            .then(data => setHosts(data))
            .catch(err => console.error("Failed to fetch hosts:", err))
            .finally(() => setLoading(false))
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Registered Hosts</h1>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <>
                    <div className="overflow-x-auto">
                        <table className="min-w-full border border-gray-300">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="px-4 py-2 text-left">Hostname</th>
                                    <th className="px-4 py-2 text-left">IP Address</th>
                                    <th className="px-4 py-2 text-left">OS</th>
                                    <th className="px-4 py-2 text-left">Status</th>
                                    <th className="px-4 py-2 text-left">Created</th>
                                </tr>
                            </thead>
                            <tbody>
                            {hosts.map(host => (
                                    <tr key={host.id} className="border-t">
                                        <td className="px-4 py-2">{host.hostname}</td>
                                        <td className="px-4 py-2">{host.ip_address}</td>
                                        <td className="px-4 py-2">{host.os || '-'}</td>
                                        <td className="px-4 py-2">{host.status}</td>
                                        <td className="px-4 py-2">{new Date(host.created_at).toLocaleString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {hosts.map((host) => (
                            <div key={host.id} className="border rounded-lg p-4 shadow">
                                <h2 className="text-lg font-semibold">{host.hostname}</h2>
                                <p className="text-sm text-gray-500">{host.ip_address}</p>
                                <p className="text-xs text-gray-400 mt-2">{new Date(host.created_at).toLocaleString()}</p>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    )
}