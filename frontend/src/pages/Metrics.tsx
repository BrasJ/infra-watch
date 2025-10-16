import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import {fetchAllMetrics, fetchGroupedMetricsByHost, fetchMetricsBySnapshot, fetchSnapshots} from '../lib/api.ts'
import type { Metric } from '../types/metric.ts'
import { format } from 'date-fns'

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [snapshots, setSnapshots] = useState<any[]>([])
  const [selectedSnapshot, setSelectedSnapshot] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedHost, setSelectedHost] = useState<number | null>(null)
  const [selectedSnapshots, setSelectedSnapshots] = useState<number[]>([])

  useEffect(() => {
    fetchSnapshots()
      .then(setSnapshots)
      .catch(err => console.error("Failed to load snapshots", err))
  }, [])

  useEffect(() => {
      setLoading(true)
      fetchGroupedMetricsByHost()
        .then((data) => {
            console.log("Fetched metrics:", data)
            setMetrics(data)
        })
        .catch(err => console.error("Failed to load metrics", err))
        .finally(() => setLoading(false))
  }, [])

  const groupByHostMetricForSnapshotLines = (metricName: string) => {
  const grouped: Record<
    number,
    Record<string, Record<string, number>>
  > = {}

  metrics
    .filter(m => m.name === metricName)
    .forEach(m => {
      const hostId = m.host_id
      const date = new Date(m.created_at)
      const minutes = date.getHours() * 60 + date.getMinutes()
      const snapshotKey = `snapshot_${m.snapshot_id}`

      if (!grouped[hostId]) grouped[hostId] = {}
      if (!grouped[hostId][minutes]) grouped[hostId][minutes] = {}
      grouped[hostId][minutes][snapshotKey] = m.value
    })

  // Convert each host’s grouped data into chart-compatible arrays
  const chartDataPerHost: Record<number, any[]> = {}

  Object.entries(grouped).forEach(([hostId, minuteMap]) => {
    const rows = Object.entries(minuteMap).map(([minutes, snapshotMap]) => ({
      minutes: Number(minutes),
      ...snapshotMap
    }))
    chartDataPerHost[Number(hostId)] = rows
  })

  return chartDataPerHost
}


  const renderChart = (title: string, metricName: string) => {
  const dataByHost = groupByHostMetricForSnapshotLines(metricName)

  return Object.entries(dataByHost).map(([hostId, chartData]) => {
    const snapshotKeys = Object.keys(chartData[0] || {}).filter(key => key !== 'minutes')
      console.log("Snapshot keys:", snapshotKeys)
      console.log("Chart data:", chartData)

    return (
      <div key={hostId} className="mb-12">
        <h2 className="text-xl font-semibold mb-2">
          {title} — Host {hostId}
        </h2>
        <div className="h-[300px]">
          <ResponsiveContainer width="95%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                  dataKey="minutes"
                  type="number"
                  domain={[0, 1440]}
                  ticks={[...Array(25).keys()].map(h => h * 60)}
                  tickFormatter={(value) => `${String(value / 60).padStart(2, '0')}:00`}
                  label={{ value: "Time of Day", position: "insideBottomRight", offset: -5 }}
              />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              {snapshotKeys.map((key, i) => (
                <Line
                  key={key}
                  dataKey={key}
                  name={`Snapshot ${key.split('_')[1]}`}
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
  })
}

  return (
    <div className="w-full min-w-0">
      <h1 className="text-2xl font-bold mb-6">Metrics Dashboard</h1>
      {loading ? (
        <p>Loading metrics...</p>
      ) : metrics.length > 0 ? (
        <>
            {renderChart('CPU Usage (%)', 'cpu_usage')}
            {renderChart('Memory Usage (%)', 'memory_usage')}
            {renderChart('Disk Usage (%)', 'disk_usage')}
        </>
      ) : (
        <p>No metrics found.</p>
    )}
    </div>
  )
}