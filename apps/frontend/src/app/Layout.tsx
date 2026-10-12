import { NavLink, Outlet } from 'react-router-dom'
import styles from './Layout.module.css'

export function Layout() {
  return (
    <div className={styles.container}>
      <nav className={styles.nav}>
        <NavLink to="/metrics" className={({ isActive }) => (isActive ? styles.active : '')}>
          Metrics
        </NavLink>
        <NavLink to="/traces" className={({ isActive }) => (isActive ? styles.active : '')}>
          Traces
        </NavLink>
      </nav>
      <Outlet />
    </div>
  )
}
