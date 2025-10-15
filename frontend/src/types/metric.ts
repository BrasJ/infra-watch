export interface Metric {
    value: number;
    id: number
    snapshot_id: number
    host_id: number
    name: string
    //cpu_usage: number
    //memory_usage: number
    //disk_usage: number
    created_at: string
}