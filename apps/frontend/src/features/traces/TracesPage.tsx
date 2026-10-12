import { useState } from 'react'
import { findTraceById } from '../../lib/api/traces'
import { useApiQuery } from '../../lib/api/useApiQuery'
import styles from './TracesPage.module.css'

export function TracesPage() {
  const [traceIdInput, setTraceIdInput] = useState('')
  const [searchedTraceId, setSearchedTraceId] = useState<string | null>(null)

  const { data, error, isLoading } = useApiQuery(
    () => (searchedTraceId ? findTraceById(searchedTraceId) : Promise.resolve(null)),
    [searchedTraceId],
  )

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setSearchedTraceId(traceIdInput.trim() || null)
  }

  return (
    <section className={styles.container}>
      <h1>Traces</h1>

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          placeholder="trace id"
          value={traceIdInput}
          onChange={(e) => setTraceIdInput(e.target.value)}
          required
        />
        <button type="submit">Buscar spans</button>
      </form>

      {isLoading && <p>Cargando…</p>}
      {error && <p className={styles.error}>{error.message}</p>}

      {data && (
        <ul className={styles.spanList}>
          {data.items.map((span) => (
            <li key={span.id} className={styles.span}>
              <strong>{span.span_name}</strong> · {span.service_name} · {span.status}
              <br />
              <small>
                span_id={span.span_id}
                {span.parent_span_id ? ` · parent=${span.parent_span_id}` : ''}
                {span.duration_ms != null ? ` · ${span.duration_ms}ms` : ''}
              </small>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
