import { useEffect, useState } from 'react'
import { fetchDashboardStats, fetchRecentAlerts, fetchAlertTrends, fetchMetricInsights } from '../lib/api'
import type { Alert, HostMetrics } from '../types'
import MetricBarChart from '../components/charts/MetricBarChart'

export default function DashboardOverview() {
  const [stats, setStats] = useState({
    totalHosts: 0,
    snapshotsLast24h: 0,
    metricsLast24h: 0,
  })
  const [recentAlerts, setRecentAlerts] = useState<Alert[]>([])
  const [alertTrends, setAlertTrends] = useState<any[]>([])
  const [metricInsights, setMetricInsights] = useState<HostMetrics[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [summary, alerts, trends, insights] = await Promise.all([
          fetchDashboardStats(),
          fetchRecentAlerts(),
          fetchAlertTrends(),
          fetchMetricInsights(),
        ])
        setStats(summary)
        setRecentAlerts(alerts)
        setAlertTrends(trends)
        setMetricInsights(insights)
      } catch (err) {
        console.error("Error loading dashboard:", err)
      } finally {
        setLoading(false)
      }
    }
    loadDashboard()
  }, [])

  return (
    <div className="w-full min-w-0 p-6">
      <h1 className="text-2xl font-bold mb-6">System Overview</h1>

      {/* High Level Summary */}
      <div className="flex flex-wrap md:flex-nowrap gap-4 mb-6">
        <div className="flex-1 p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
          <h2 className="text-sm text-gray-500">Total Hosts</h2>
          <p className="text-xl font-semibold">{stats.totalHosts}</p>
        </div>
        <div className="flex-1 p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
          <h2 className="text-sm text-gray-500">Snapshots (24h)</h2>
          <p className="text-xl font-semibold">{stats.snapshotsLast24h}</p>
        </div>
        <div className="flex-1 p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
          <h2 className="text-sm text-gray-500">Metrics (24h)</h2>
          <p className="text-xl font-semibold">{stats.metricsLast24h}</p>
        </div>
      </div>

      {/* Alerts Overview */}
      <div className="w-full min-w-0 max-w-[95%] mb-10">
        <h2 className="text-lg font-bold mb-4">Recent Alerts</h2>
        <div className="overflow-x-auto mb-6">
          <table className="min-w-full border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Time</th>
                <th className="px-4 py-2 text-left">Host</th>
                <th className="px-4 py-2 text-left">Message</th>
                <th className="px-4 py-2 text-left">Severity</th>
              </tr>
            </thead>
            <tbody>
              {recentAlerts.map(alert => (
                <tr key={alert.id} className="border-t">
                  <td className="px-4 py-2">{new Date(alert.created_at).toLocaleString()}</td>
                  <td className="px-4 py-2">{alert.host_id || '-'}</td>
                  <td className="px-4 py-2">{alert.message}</td>
                  <td className={`px-4 py-2 font-medium ${
                    alert.severity === 'critical' ? 'text-red-500' :
                    alert.severity === 'warning' ? 'text-yellow-500' : 'text-blue-500'}`}>{alert.severity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Insights Panel */}
      <div className="w-full min-w-0">
        <h2 className="text-lg font-bold mb-4">Insights</h2>
        <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[250px] max-w-[32%]">
                <MetricBarChart metricName="cpu_usage" title="CPU Usage (24h)" />
            </div>
            <div className="flex-1 min-w-[250px] max-w-[32%]">
                <MetricBarChart metricName="memory_usage" title="Memory Usage (24h)" />
            </div>
            <div className="flex-1 min-w-[250px] max-w-[32%]">
                <MetricBarChart metricName="disk_usage" title="Disk Usage (24h)" />
            </div>
        </div>
      </div>
    </div>
  )
}