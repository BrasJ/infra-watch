import axios from 'axios';
import type { Metric } from '../types/metric.ts';

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