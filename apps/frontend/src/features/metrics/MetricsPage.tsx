import { useState } from 'react'
import { createMetric, listMetrics } from '../../lib/api/metrics'
import { useApiQuery } from '../../lib/api/useApiQuery'
import styles from './MetricsPage.module.css'

const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000

function parseTags(raw: string): Record<string, string> {
  const tags: Record<string, string> = {}
  for (const entry of raw.split(',').map((s) => s.trim()).filter(Boolean)) {
    const [key, value] = entry.split(':')
    if (key && value) tags[key] = value
  }
  return tags
}

export function MetricsPage() {
  const [refreshKey, setRefreshKey] = useState(0)
  const [name, setName] = useState('')
  const [value, setValue] = useState('')
  const [tagsInput, setTagsInput] = useState('env:dev')
  const [submitError, setSubmitError] = useState<string | null>(null)

  const { data, error, isLoading } = useApiQuery(
    () =>
      listMetrics({
        startDate: new Date(Date.now() - THIRTY_DAYS_MS).toISOString(),
        endDate: new Date().toISOString(),
      }),
    [refreshKey],
  )

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setSubmitError(null)
    try {
      await createMetric({
        name,
        value: Number(value),
        tags: parseTags(tagsInput),
        recordedAt: new Date().toISOString(),
      })
      setName('')
      setValue('')
      setRefreshKey((key) => key + 1)
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Error al crear la métrica')
    }
  }

  return (
    <section className={styles.container}>
      <h1>Metrics</h1>

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          placeholder="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          placeholder="value"
          type="number"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          required
        />
        <input
          placeholder="tags (key:value, key:value)"
          value={tagsInput}
          onChange={(e) => setTagsInput(e.target.value)}
        />
        <button type="submit">Crear métrica</button>
      </form>
      {submitError && <p className={styles.error}>{submitError}</p>}

      {isLoading && <p>Cargando…</p>}
      {error && <p className={styles.error}>{error.message}</p>}

      {data && (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Valor</th>
              <th>Tags</th>
              <th>Registrado en</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((metric) => (
              <tr key={metric.id}>
                <td>{metric.name}</td>
                <td>{metric.value}</td>
                <td>
                  {Object.entries(metric.tags)
                    .map(([k, v]) => `${k}:${v}`)
                    .join(', ')}
                </td>
                <td>{new Date(metric.recordedAt).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
