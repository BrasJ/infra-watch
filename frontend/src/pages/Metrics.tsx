import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetchGroupedMetricsByHost, fetchHosts } from '../lib/api.ts'
import type { Metric } from '../types/metric.ts'
import type { Host } from '../types/host.ts'
import usePageMetadata from '../hooks/usePageMetadata';

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [hosts, setHosts] = useState<Host[]>([])
  const [selectedHost, setSelectedHost] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  usePageMetadata(
    'Infra-Watch | Metrics',
    'Visualize CPU, memory, and disk performance metrics over time.'
  );

  useEffect(() => {
    fetchHosts()
      .then(setHosts)
      .catch(err => console.error("Failed to load hosts", err))
  }, [])

  useEffect(() => {
    if (selectedHost !== null) {
      setLoading(true)
      fetchGroupedMetricsByHost(selectedHost)
        .then(setMetrics)
        .catch(err => console.error("Failed to load metrics", err))
        .finally(() => setLoading(false))
    }
  }, [selectedHost])

  const groupByHostMetricForSnapshotLines = (metricName: string) => {
    const grouped: Record<number, Record<number, number>> = {}

    metrics
      .filter(m => m.name === metricName && (selectedHost === null || m.host_id === selectedHost))
      .forEach(m => {
        const date = new Date(m.created_at)
        const minutes = date.getHours() * 60 + date.getMinutes()

        if (!grouped[m.snapshot_id]) grouped[m.snapshot_id] = {}
        grouped[m.snapshot_id][minutes] = m.value
      })

    const chartDataPerSnapshot: Record<number, any[]> = {}
    Object.entries(grouped).forEach(([snapshotId, minuteMap]) => {
      const rows = Object.entries(minuteMap)
        .map(([minutes, value]) => ({
          minutes: Number(minutes),
          value,
        }))
        .sort((a, b) => a.minutes - b.minutes)
      chartDataPerSnapshot[Number(snapshotId)] = rows
    })

    return chartDataPerSnapshot
  }

  const renderChart = (title: string, metricName: string) => {
    const dataBySnapshot = groupByHostMetricForSnapshotLines(metricName)
    const snapshotKeys = Object.keys(dataBySnapshot)

    if (snapshotKeys.length === 0) {
      return (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">{title}</h2>
          <p className="text-gray-600">No data available for this metric.</p>
        </div>
      )
    }

    return (
      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-2">{title}</h2>
        <div className="h-[300px]">
          <ResponsiveContainer width="95%" height="100%">
            <LineChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                domain={[0, 1440]}
                ticks={[...Array(25).keys()].map(h => h * 60)}
                tickFormatter={(v) => `${String(v / 60).padStart(2, '0')}:00`}
                label={{ value: "Time of Day", position: "insideBottomRight", offset: -5 }}
              />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />

              {snapshotKeys.map((sid, i) => (
                <Line
                  key={sid}
                  data={dataBySnapshot[Number(sid)]}
                  dataKey="value"
                  name={`Snapshot ${sid}`}
                  type="monotone"
                  stroke={`hsl(${(i * 60) % 360}, 70%, 50%)`}
                  dot={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full min-w-0">
      <h1 className="text-2xl font-bold mb-4">Metrics Dashboard</h1>
      <div className="mb-6">
        <label className="block font-semibold mb-1">Select Host:</label>
        <select
          className="border p-2 rounded"
          value={selectedHost ?? ''}
          onChange={(e) => {
            const value = Number(e.target.value)
            setSelectedHost(isNaN(value) ? null : value)
          }}
        >
          <option value="">-- Select Host --</option>
          {hosts.map(host => (
            <option key={host.id} value={host.id}>
              {host.hostname}
            </option>
          ))}
        </select>
      </div>

      {selectedHost && (
        <>
          {loading ? (
            <p className="text-gray-500 mb-4">Loading metrics...</p>
          ) : (
            <>
              {renderChart('CPU Usage (%)', 'cpu_usage')}
              {renderChart('Memory Usage (%)', 'memory_usage')}
              {renderChart('Disk Usage (%)', 'disk_usage')}
            </>
          )}
        </>
      )}
    </div>
  )
}
