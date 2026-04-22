import api from './index.js'

export const fetchCounts = (date) => {
  return api.get('/api/counts', { params: { date } })
}

export const fetchTrend = (date) => {
  return api.get('/api/events/trend', { params: { date } })
}