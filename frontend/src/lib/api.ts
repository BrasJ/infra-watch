import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export default api;

export async function fetchHosts() {
    const response = await axios.get(`${api}/hosts`)
    return response.data
}

export async function fetchAllMetrics(): Promise<Metric[]> {
    const res = await api.get('/metrics');
    return res.data
}