import { defineStore }       from 'pinia'
import { fetchRecentEvents } from '../api/events.js'

export const useEventStore = defineStore('events', {
  state: () => ({
    recentEvents:   [],
    isLoading:      false,
    lastUndoResult: null   // ← watched by App.vue to trigger UndoToast
  }),

  actions: {
    prependEvent(event) {
      this.recentEvents.unshift(event)
      if (this.recentEvents.length > 50) {
        this.recentEvents = this.recentEvents.slice(0, 50)
      }
    },

    removeLastEvent() {
      if (this.recentEvents.length > 0) {
        this.recentEvents.shift()
      }
    },

    setEvents(events) {
      this.recentEvents = events
    },

    // Called by useEventLogger after undo — triggers toast in App.vue
    setUndoResult(result) {
      this.lastUndoResult = { ...result, ts: Date.now() }
    },

    async fetchRecent() {
      this.isLoading = true
      try {
        const response    = await fetchRecentEvents()
        this.recentEvents = response.data
      } catch (err) {
        console.error('Failed to fetch recent events:', err)
      } finally {
        this.isLoading = false
      }
    }
  },

  getters: {
    lastTen:   (state) => state.recentEvents.slice(0, 10),
    allEvents: (state) => state.recentEvents
  }
})