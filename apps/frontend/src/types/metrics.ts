export interface Metric {
  id: number
  name: string
  value: number
  tags: Record<string, string>
  recordedAt: string
  createdAt: string
}

export interface MetricCreateInput {
  name: string
  value: number
  tags: Record<string, string>
  recordedAt: string
}
