import { useEffect, useState } from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer
} from "recharts"
import { fetchAlerts } from "../../lib/api"
import type { Alert } from "../../types/alert"

interface AlertChartPoint {
  time: string
  [host: string]: number | string
}

export default function AlertTrendChart() {
  const [data, setData] = useState<AlertChartPoint[]>([])

  useEffect(() => {
    async function loadData() {
      try {
        const alerts: Alert[] = await fetchAlerts()
        const grouped = groupAlertsByHour(alerts)
        setData(grouped)
      } catch (err) {
        console.error("Failed to load alerts for chart", err)
      }
    }

    loadData()
  }, [])

  return (
    <div className="bg-white border rounded shadow p-4">
      <h2 className="text-lg font-semibold mb-4">Alert Trend (Last 24h)</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          {getHostIdsFromData(data).map((hostId, index) => (
            <Line
              key={hostId}
              type="monotone"
              dataKey={hostId}
              stroke={getColor(index)}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

// Util: Groups alerts by hour and host
function groupAlertsByHour(alerts: Alert[]): AlertChartPoint[] {
  const now = new Date()
  const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000)

  const hourlyBuckets: Record<string, Record<number, number>> = {}

  for (const alert of alerts) {
    const created = new Date(alert.created_at)
    if (created < oneDayAgo) continue

    const hour = created.toISOString().slice(0, 13).replace("T", " ") + ":00"
    const host = alert.host_id ?? -1

    if (!hourlyBuckets[hour]) {
      hourlyBuckets[hour] = {}
    }
    hourlyBuckets[hour][host] = (hourlyBuckets[hour][host] || 0) + 1
  }

  return Object.entries(hourlyBuckets).map(([hour, hostCounts]) => ({
    time: hour,
    ...hostCounts
  }))
}

// Util: Unique list of host IDs from the data
function getHostIdsFromData(data: AlertChartPoint[]): number[] {
  const ids = new Set<number>()
  for (const entry of data) {
    for (const key in entry) {
      if (key !== "time") {
        ids.add(Number(key))
      }
    }
  }
  return Array.from(ids).sort((a, b) => a - b)
}

// Util: Returns consistent colors per index
function getColor(index: number): string {
  const colors = [
    "#2563eb", // blue-600
    "#16a34a", // green-600
    "#dc2626", // red-600
    "#f59e0b", // amber-500
    "#6b7280", // gray-500
    "#8b5cf6", // violet-500
    "#ec4899", // pink-500
  ]
  return colors[index % colors.length]
}
