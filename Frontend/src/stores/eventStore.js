import { defineStore } from 'pinia'
import { fetchRecentEvents } from '../api/events.js'

export const useEventStore = defineStore('events', {
  state: () => ({
    recentEvents: []
  }),

  actions: {
    // Called immediately after a button click — no API wait
    prependEvent(event) {
      this.recentEvents.unshift(event)

      // Keep the list trimmed to 20 items max
      if (this.recentEvents.length > 20) {
        this.recentEvents = this.recentEvents.slice(0, 20)
      }
    },

    // Called after undo
    removeLastEvent() {
      if (this.recentEvents.length > 0) {
        this.recentEvents.shift()
      }
    },

    // Called on initial load and refresh
    setEvents(events) {
      this.recentEvents = events
    },

    // Full fetch from API
    async fetchRecent() {
      try {
        const response = await fetchRecentEvents()
        this.recentEvents = response.data
      } catch (err) {
        console.error('Failed to fetch recent events:', err)
      }
    }
  }
})