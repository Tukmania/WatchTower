import api from './index.js'

export const logEvent = (eventData) => {
  return api.post('/api/log', eventData)
}

export const undoLastEvent = () => {
  return api.post('/api/undo')
}

export const fetchRecentEvents = () => {
  return api.get('/api/events/recent')
}