export type SpanStatus = 'UNSET' | 'OK' | 'ERROR'

export interface Trace {
  id: number
  trace_id: string
  span_id: string
  parent_span_id: string | null
  span_name: string
  service_name: string
  start_time: string
  end_time: string | null
  duration_ms: number | null
  status: SpanStatus
  attributes: Record<string, string>
  created_at: string
}
