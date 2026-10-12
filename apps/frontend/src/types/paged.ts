export interface PagedResult<T> {
  items: T[]
  total_items: number
  page: number
  size: number
}
