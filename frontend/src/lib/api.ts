import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export default api;

export async function fetchHosts() {
    const response = await axios.get(`${api}/hosts`)
    return response.data
}