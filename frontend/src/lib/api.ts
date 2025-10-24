import axios from "axios";
import type { Metric } from "../types/metric.ts";
import type { Alert } from "../types/alert.ts";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: false,
});

export default api;

export async function fetchHosts() {
  const response = await api.get("/hosts/");
  console.log("Fetched hosts:", response.data);
  return response.data;
}

export async function fetchAllMetrics(): Promise<Metric[]> {
  const res = await api.get("/metrics/");
  return res.data;
}

export async function fetchMetricsBySnapshot(snapshotId: number) {
  const res = await api.get(`/metrics/snapshot/${snapshotId}`);
  return res.data;
}

export async function fetchGroupedMetricsByHost(hostId: number) {
  const res = await api.get(`/metrics/grouped/host/${hostId}`);
  return res.data;
}

export async function fetchSnapshots() {
  const res = await api.get("/snapshots/");
  return res.data;
}

export async function fetchAlerts(filters: {
  severity?: string;
  acknowledged?: boolean;
} = {}): Promise<Alert[]> {
  const params = new URLSearchParams();

  if (filters.severity) params.append("severity", filters.severity);
  if (filters.acknowledged !== undefined)
    params.append("acknowledged", String(filters.acknowledged));

  const res = await api.get(`/alerts/?${params.toString()}`);
  return res.data;
}

export async function createAlert(payload: {
  snapshot_id: number;
  message: string;
  severity: "info" | "warning" | "critical";
  type: string;
  acknowledged: boolean;
}) {
  const res = await api.post("/alerts/", payload);
  return res.data;
}

export async function acknowledgeAlert(id: number) {
  const res = await api.patch(`/alerts/${id}`, { acknowledged: true });
  return res.data;
}

export async function deleteAlert(id: number) {
  const res = await api.delete(`/alerts/${id}`);
  return res.data;
}

export async function fetchDashboardStats() {
  const res = await api.get("/dashboard/stats");
  return res.data;
}

export async function fetchRecentAlerts() {
  const res = await api.get("/dashboard/alerts/recent");
  return res.data;
}

export async function fetchAlertTrends() {
  const res = await api.get("/dashboard/alerts/trends");
  return res.data;
}

export async function fetchMetricInsights() {
  const res = await api.get("/dashboard/metrics/insights");
  return res.data;
}
