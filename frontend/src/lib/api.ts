import axios from 'axios';
import type { Metric } from '../types/metric.ts';
import type { Alert } from '../types/alert.ts'

const api = axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: false,
});

export default api

export async function fetchHosts() {
    const response = await api.get('/hosts/')
    console.log("Fetched hosts:", response.data)
    return response.data
}

export async function fetchAllMetrics(): Promise<Metric[]> {
    const res = await api.get('/metrics/');
    return res.data
}

export async function fetchAlerts(filters: {
    severity?: string;
    acknowledged?: boolean;
} = {}): Promise<Alert[]> {
    const params = new URLSearchParams()

    if (filters.severity) {
        params.append('severity', filters.severity)
    }

    if (filters.acknowledged !== undefined) {
        params.append('acknowledged', String(filters.acknowledged))
    }

    const response = await api.get(`/alerts/?${params.toString()}`)
    return response.data
}

export async function createAlert(payload: {
      snapshot_id: number
      message: string
      severity: 'info' | 'warning' | 'critical'
      type: string
      acknowledged: boolean
}) {
      const response = await api.post('/alerts/', payload)
      return response.data
}

export async function acknowledgeAlert(id: number) {
  const response = await fetch(`http://localhost:8000/alerts/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ acknowledged: true }),
  });
  if (!response.ok) throw new Error('Failed to acknowledge alert');
  return await response.json();
}


export async function deleteAlert(id: number) {
  const response = await fetch(`http://localhost:8000/alerts/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete alert');
}


export async function fetchSnapshots() {
  const response = await api.get('/snapshots/')
  return response.data
}

export async function fetchMetricsBySnapshot(snapshotId: number) {
  const res = await api.get(`/metrics/snapshot/${snapshotId}`);
  return res.data;
}

export async function fetchGroupedMetricsByHost(hostId: number){
  const res = await fetch(`http://localhost:8000/metrics/grouped/host/${hostId}`)
  return res.json()
}

export async function fetchDashboardStats() {
  const response = await api.get('/dashboard/stats')
  return response.data
}

export async function fetchRecentAlerts() {
  const response = await api.get('/dashboard/alerts/recent')
  return response.data
}

export async function fetchAlertTrends() {
  const response = await api.get('/dashboard/alerts/trends')
  return response.data
}

export async function fetchMetricInsights() {
  const response = await api.get('/dashboard/metrics/insights')
  return response.data
}
