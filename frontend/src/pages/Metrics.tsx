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

  const groupBySnapshot = (metricName: string) => {
    const grouped: Record<number, { timestamp: string; value: number }[]> = {}
    metrics
      .filter(metric => metric.name === metricName)
      .forEach(metric => {
        console.log("metric object", metric)
        const groupKey = metric.snapshot_id
        if (!grouped[groupKey]) grouped[groupKey] = []
        grouped[groupKey].push({
          timestamp: format(new Date(metric.created_at), 'HH:mm:ss'),
          value: metric.value,
        })
        //grouped[groupKey].sort((a, b) => a.timestamp.localecompare(b.timestamp))
      })
    return grouped
  }

  const renderChart = (title: string, metricName: string) => {
    const dataBySnapshot = groupBySnapshot(metricName)
    return Object.entries(dataBySnapshot).map(([snapshotId, data], index) => {
      const values = data.map(point => point.value)
      const average = (values.reduce((sum, v) => sum + v, 0) / values.length).toFixed(2)
      const min = Math.min(...values).toFixed(2)
      const max = Math.max(...values).toFixed(2)

      return (
          <div className="mb-10">
            <h2 className="text-xl font-semibold mb-2">{title}</h2>
            <ResponsiveContainer width="100%" height={300} key={snapshotId}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="timestamp"/>
                <YAxis domain={[0, 100]}/>
                <Tooltip/>
                <Legend/>
                <Line
                    dataKey="value"
                    name={`Snapshot ${snapshotId}`}
                    type="monotone"
                    stroke={`hsl(${(index * 50) % 360}, 70%, 50%)`}
                    dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="text-sm text-gray-600 mt-2">
              <span className="mr-4">Average: <strong>{average}%</strong></span><br />
              <span className="mr-4">Min: <strong>{min}%</strong></span><br />
              <span className="mr-4">Max: <strong>{max}%</strong></span><br />
            </div>
          </div>
      )
    })
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