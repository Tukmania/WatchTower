import { ref }            from 'vue'
import { logEvent, undoLastEvent, fetchRecentEvents } from '../api/events.js'
import { useEventStore }  from '../stores/eventStore.js'
import { useCountsStore } from '../stores/countsStore.js'

export function useEventLogger() {
  const isLoading  = ref(false)
  const error      = ref(null)
  const lastLogged = ref(null)

  async function log(eventType, subtype, location, locationCategory) {
    isLoading.value = true
    error.value     = null

    try {
      const response   = await logEvent({
        event_type:        eventType,
        subtype:           subtype,
        location:          location,
        location_category: locationCategory
      })

      const savedEvent    = response.data
      lastLogged.value    = savedEvent

      const eventStore  = useEventStore()
      const countsStore = useCountsStore()

      eventStore.prependEvent(savedEvent)
      await countsStore.refreshCounts()
      await countsStore.refreshHourly()

      return { success: true, event: savedEvent }

    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to log event.'
      console.error('useEventLogger error:', err)
      return { success: false, error: error.value }

    } finally {
      isLoading.value = false
    }
  }

  async function undo() {
    isLoading.value = true
    error.value     = null

    try {
      const response = await undoLastEvent()
      const result   = response.data
      const eventStore  = useEventStore()
      const countsStore = useCountsStore()

      if (result.success) {
        eventStore.removeLastEvent()
        await countsStore.refreshCounts()
        await countsStore.refreshHourly()
        lastLogged.value = null

        // Trigger the global UndoToast
        eventStore.setUndoResult({
          success: true,
          message: `${result.undone?.event_type || 'Event'} at 
                    ${result.undone?.location || ''} undone`
        })

        return { success: true, undone: result.undone }

      } else {
        eventStore.setUndoResult({
          success: false,
          message: result.message || 'Nothing to undo'
        })
        return { success: false, message: result.message }
      }

    } catch (err) {
      const eventStore = useEventStore()
      eventStore.setUndoResult({
        success: false,
        message: 'Undo failed. Please try again.'
      })
      console.error('Undo error:', err)
      return { success: false }

    } finally {
      isLoading.value = false
    }
  }

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
    isLoading,
    error,
    lastLogged,
    log,
    undo,
    refreshEvents
  }
}