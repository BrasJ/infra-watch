import axios from 'axios';
import type { Metric } from '../types/metric.ts';
import type { Alert } from '../types/alert.ts'

const api = axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: false,
});

export default api

export async function fetchHosts() {
    const response = await api.get('/hosts')
    console.log("Fetched hosts:", response.data)
    return response.data
}

export async function fetchAllMetrics(): Promise<Metric[]> {
    const res = await api.get('/metrics');
    return res.data
}

export async function fetchAlerts(): Promise<Alert[]> {
    const response = await api.get('/alerts')
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