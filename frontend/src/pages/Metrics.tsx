import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetchGroupedMetricsByHost, fetchHosts } from '../lib/api.ts'
import type { Metric } from '../types/metric.ts'
import type { Host } from '../types/host.ts'
import usePageMetadata from '../hooks/usePageMetadata'

export default function MetricsDashboard() {
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [hosts, setHosts] = useState<Host[]>([])
  const [selectedHost, setSelectedHost] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  usePageMetadata(
    'Infra-Watch | Metrics',
    'Visualize CPU, memory, and disk performance metrics over time.'
  )

  useEffect(() => {
    setError(null)
    fetchHosts()
      .then(setHosts)
      .catch(err => {
        console.error("Failed to load hosts", err)
        setError("Unable to load hosts. Please try again later.")
      })
  }, [])

  useEffect(() => {
    if (selectedHost !== null) {
      setLoading(true)
      setError(null)
      fetchGroupedMetricsByHost(selectedHost)
        .then(setMetrics)
        .catch(err => {
          console.error("Failed to load metrics", err)
          setError("Unable to load metrics for this host.")
        })
        .finally(() => setLoading(false))
    }
  }, [selectedHost])

  const groupByHostMetricForSnapshotLines = (metricName: string) => {
    const grouped: Record<number, Record<string, Record<string, number>>> = {}

    metrics
      .filter(m => m.name === metricName && (selectedHost === null || m.host_id === selectedHost))
      .forEach(m => {
        const hostId = m.host_id
        const date = new Date(m.created_at)
        const minutes = date.getHours() * 60 + date.getMinutes()
        const snapshotKey = `snapshot_${m.snapshot_id}`

        if (!grouped[hostId]) grouped[hostId] = {}
        if (!grouped[hostId][minutes]) grouped[hostId][minutes] = {}
        grouped[hostId][minutes][snapshotKey] = m.value
      })

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
    const filteredData =
      selectedHost && dataByHost[selectedHost]
        ? { [selectedHost]: dataByHost[selectedHost] }
        : dataByHost

    if (!filteredData || Object.keys(filteredData).length === 0) {
      return (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">{title}</h2>
          <p className="text-gray-600">No data available for this metric.</p>
        </div>
      )
    }

    return Object.entries(filteredData).map(([hostId, chartData]) => {
      if (!chartData || chartData.length === 0) {
        return (
          <div key={hostId} className="mb-6">
            <h2 className="text-xl font-semibold mb-2">
              {title} — Host {hostId}
            </h2>
            <p className="text-gray-600">No chart data available.</p>
          </div>
        )
      }

      const snapshotKeys = Object.keys(chartData[0]).filter(key => key !== 'minutes')

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
              {host.hostname ? host.hostname : `Host ${host.id}`}
            </option>
          ))}
        </select>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}

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
