// src/types/alert.ts
export type Alert = {
    id: number
    message: string
    severity: 'info' | 'warning' | 'critical'
    acknowledged: boolean
    snapshot_id: number
    type: string
    created_at: string
}
