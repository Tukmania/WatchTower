import { ref } from 'vue'
import { logEvent, undoLastEvent, fetchRecentEvents } from '../api/events.js'
import { useEventStore } from '../stores/eventStore.js'
import { useCountsStore } from '../stores/countsStore.js'

export function useEventLogger() {

  const isLoading  = ref(false)
  const error      = ref(null)
  const lastLogged = ref(null)  // holds the last successfully logged event

  // ── Core logging function ─────────────────────────────────────────────────
  // This is what every TallyButton calls
  async function log(eventType, subtype, location, locationCategory) {
    isLoading.value = true
    error.value     = null

    try {
      const response = await logEvent({
        event_type:        eventType,
        subtype:           subtype,
        location:          location,
        location_category: locationCategory
      })

      const savedEvent = response.data

      // Store the last logged event so TallyButton can show flash feedback
      lastLogged.value = savedEvent

      // Push to event store immediately — no waiting for a poll
      const eventStore = useEventStore()
      eventStore.prependEvent(savedEvent)

      // Refresh live counts immediately after every log
      const countsStore = useCountsStore()
      await countsStore.refreshCounts()

      return { success: true, event: savedEvent }

    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to log event. Try again.'
      console.error('useEventLogger error:', err)
      return { success: false, error: error.value }

    } finally {
      isLoading.value = false
    }
  }

  // ── Undo last event ───────────────────────────────────────────────────────
  async function undo() {
    isLoading.value = true
    error.value     = null

    try {
      const response = await undoLastEvent()
      const result   = response.data

      if (result.success) {
        // Remove from event store
        const eventStore = useEventStore()
        eventStore.removeLastEvent()

        // Refresh counts after undo
        const countsStore = useCountsStore()
        await countsStore.refreshCounts()

        lastLogged.value = null

        return { success: true, undone: result.undone }
      } else {
        return { success: false, message: result.message }
      }

    } catch (err) {
      error.value = err.response?.data?.message || 'Undo failed. Try again.'
      console.error('useEventLogger undo error:', err)
      return { success: false, error: error.value }

    } finally {
      isLoading.value = false
    }
  }

  // ── Refresh recent events ─────────────────────────────────────────────────
  async function refreshEvents() {
    try {
      const response   = await fetchRecentEvents()
      const eventStore = useEventStore()
      eventStore.setEvents(response.data)
    } catch (err) {
      console.error('Failed to refresh events:', err)
    }
  }

  return {
    // State
    isLoading,
    error,
    lastLogged,

    // Actions
    log,
    undo,
    refreshEvents
  }
}