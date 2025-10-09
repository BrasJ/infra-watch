import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetchAllMetrics, fetchMetricsBySnapshot, fetchSnapshots } from '../lib/api.ts'
import type { Metric } from '../types/metric.ts'
import { format } from 'date-fns'

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [snapshots, setSnapshots] = useState<any[]>([])
  const [selectedSnapshot, setSelectedSnapshot] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSnapshots()
      .then(setSnapshots)
      .catch(err => console.error("Failed to load snapshots", err))
  }, [])

  useEffect(() => {
    if (selectedSnapshot !== null) {
      setLoading(true)
      fetchMetricsBySnapshot(selectedSnapshot)
        .then(setMetrics)
        .catch(err => console.error("Failed to load metrics", err))
        .finally(() => setLoading(false))
    }
  }, [selectedSnapshot])

  const groupByHost = (metricField: keyof Metric) => {
    const grouped: Record<number, { timestamp: string; value: number }[]> = {}
    metrics.forEach(metric => {
      if (!grouped[metric.host_id]) grouped[metric.host_id] = []
      grouped[metric.host_id].push({
        timestamp: format(new Date(metric.created_at), 'HH:mm:ss'),
        value: metric[metricField] as number,
      })
    })
    return grouped
  }

  const renderChart = (title: string, metricField: keyof Metric, color: string) => {
    const dataByHost = groupByHost(metricField)
    return (
      <div className="mb-10">
        <h2 className="text-xl font-semibold mb-2">{title}</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            {Object.entries(dataByHost).map(([hostId, data], index) => (
              <Line
                key={hostId}
                dataKey="value"
                data={data}
                name={`Host ${hostId}`}
                type="monotone"
                stroke={`hsl(${(index * 50) % 360}, 70%, 50%)`}
                dot={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    )
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Metrics Dashboard</h1>

      <div className="mb-6">
        <label className="block font-semibold mb-1">Select Snapshot:</label>
        <select
          className="border p-2 rounded"
          value={selectedSnapshot ?? ''}
          onChange={(e) => {
            const value = Number(e.target.value)
            setSelectedSnapshot(isNaN(value) ? null : value)
          }}
        >
          <option value="">-- Select Snapshot --</option>
          {snapshots.map((snap) => (
            <option key={snap.id} value={snap.id}>
              Snapshot {snap.id} - Host {snap.host_id}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Loading metrics...</p>
      ) : (
        selectedSnapshot && metrics.length > 0 ? (
          <>
            {renderChart('CPU Usage (%)', 'cpu_usage', '#3b82f6')}
            {renderChart('Memory Usage (%)', 'memory_usage', '#10b981')}
            {renderChart('Disk Usage (%)', 'disk_usage', '#f59e0b')}
          </>
        ) : selectedSnapshot ? (
          <p>No metrics found for this snapshot.</p>
        ) : null
      )}
    </div>
  )
}