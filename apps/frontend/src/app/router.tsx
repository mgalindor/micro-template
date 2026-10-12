import { createBrowserRouter, Navigate } from 'react-router-dom'
import { Layout } from './Layout'
import { MetricsPage } from '../features/metrics/MetricsPage'
import { TracesPage } from '../features/traces/TracesPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to="/metrics" replace /> },
      { path: 'metrics', element: <MetricsPage /> },
      { path: 'traces', element: <TracesPage /> },
    ],
  },
])
