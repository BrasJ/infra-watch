import { useEffect, useState } from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts"
import { fetchMetrics } from "../../lib/api"
import type { Metric } from "../../types/metric"

interface HostMetricAggregate {
  host_id: number
  hostname: string
  avg: number
  max: number
}

interface ChartEntry {
  name: string
  avg: number
  max: number
}

interface MetricBarChartProps {
  metricName: "cpu_usage" | "memory_usage" | "disk_usage"
  title: string
}

export default function MetricBarChart({ metricName, title }: MetricBarChartProps) {
  const [data, setData] = useState<ChartEntry[]>([])

  useEffect(() => {
    async function load() {
      try {
        const raw: Metric[] = await fetchMetrics()
        const now = new Date()
        const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000)

        const filtered = raw.filter(
          (m) => m.name === metricName && new Date(m.created_at) >= oneDayAgo
        )

        const grouped: Record<number, Metric[]> = {}
        for (const m of filtered) {
          if (!grouped[m.host_id]) grouped[m.host_id] = []
          grouped[m.host_id].push(m)
        }

        const entries: ChartEntry[] = Object.entries(grouped).map(([hostId, metrics]) => {
          const hostName = metrics[0].hostname || `Host ${hostId}`
          const values = metrics.map(m => m.value)
          const avg = values.reduce((a, b) => a + b, 0) / values.length
          const max = Math.max(...values)

          return {
            name: hostName,
            avg: parseFloat(avg.toFixed(2)),
            max: max
          }
        })

        setData(entries)
      } catch (err) {
        console.error("Failed to load metric chart data", err)
      }
    }

    load()
  }, [metricName])

  return (
    <div className="bg-white border rounded shadow p-4">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="avg" fill="#60a5fa" name="Avg (24h)" />
          <Bar dataKey="max" fill="#ef4444" name="Max (24h)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
