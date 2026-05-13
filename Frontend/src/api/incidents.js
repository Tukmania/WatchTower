import api from './index.js'

export const logIncident    = (data)       => api.post('/api/incidents', data)
export const fetchIncidents = (start, end) => api.get('/api/incidents', { params: { start, end } })
export const deleteIncident = (id)         => api.delete(`/api/incidents/${id}`)
