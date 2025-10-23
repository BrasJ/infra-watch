import { useEffect, useState } from "react"
import { fetchHosts, fetchSnapshots, fetchMetrics } from "../../lib/api"
import type { Host } from "../../types/host"
import type { Snapshot } from "../../types/snapshot"
import type { Metric } from "../../types/metric"

export default function SystemStatsRow() {
  const [hostCount, setHostCount] = useState(0)
  const [snapshots24h, setSnapshots24h] = useState(0)
  const [metrics24h, setMetrics24h] = useState(0)

  useEffect(() => {
    const now = new Date()
    const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000)

    async function loadData() {
      try {
        const [hosts, snapshots, metrics]: [Host[], Snapshot[], Metric[]] = await Promise.all([
          fetchHosts(),
          fetchSnapshots(),
          fetchMetrics(),
        ])

        setHostCount(hosts.length)

        const recentSnapshots = snapshots.filter(
          (snap) => new Date(snap.created_at) >= oneDayAgo
        )
        setSnapshots24h(recentSnapshots.length)

        const recentMetrics = metrics.filter(
          (metric) => new Date(metric.created_at) >= oneDayAgo
        )
        setMetrics24h(recentMetrics.length)
      } catch (err) {
        console.error("Failed to load system stats:", err)
      }
    }

    loadData()
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div className="bg-white border rounded shadow p-4">
        <h2 className="text-sm text-gray-500 mb-1">Total Hosts</h2>
        <p className="text-2xl font-bold text-gray-800">{hostCount}</p>
      </div>
      <div className="bg-white border rounded shadow p-4">
        <h2 className="text-sm text-gray-500 mb-1">Snapshots (24h)</h2>
        <p className="text-2xl font-bold text-gray-800">{snapshots24h}</p>
      </div>
      <div className="bg-white border rounded shadow p-4">
        <h2 className="text-sm text-gray-500 mb-1">Metrics Recorded (24h)</h2>
        <p className="text-2xl font-bold text-gray-800">{metrics24h}</p>
      </div>
    </div>
  )
}
