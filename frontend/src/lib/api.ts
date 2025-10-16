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

export async function acknowledgeAlert(alertId: number): Promise<Alert> {
    const response = await api.put('/alerts/${alertId}', {
        acknowledged: true,
    })
    return response.data
}

export async function deleteAlert(alertId: number): Promise<void> {
    await api.delete('/alerts/${alertId}')
}

export async function fetchSnapshots() {
  const response = await api.get('/snapshots/')
  return response.data
}

export async function fetchMetricsBySnapshot(snapshotId: number) {
  const res = await api.get(`/metrics/snapshot/${snapshotId}`);
  return res.data;
}

export async function fetchGroupedMetricsByHost(): Promise<Metric[]> {
  const res = await fetch("http://localhost:8000/metrics/grouped/host")
  if (!res.ok) throw new Error("Failed to fetch grouped metrics")
  return res.json()
}
