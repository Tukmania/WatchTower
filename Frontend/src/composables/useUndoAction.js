import { ref }            from 'vue'
import { undoLastEvent }  from '../api/events.js'
import { useEventStore }  from '../stores/eventStore.js'
import { useCountsStore } from '../stores/countsStore.js'

export function useUndoAction() {
  const isLoading   = ref(false)
  const lastUndone  = ref(null)
  const error       = ref(null)
  const message     = ref('')
  const success     = ref(false)

  async function undo() {
    isLoading.value = true
    error.value     = null
    message.value   = ''
    success.value   = false

    try {
      const response = await undoLastEvent()
      const result   = response.data

      if (result.success) {
        lastUndone.value = result.undone

        // Remove from event store immediately
        const eventStore = useEventStore()
        eventStore.removeLastEvent()

        // Refresh counts to reflect the removal
        const countsStore = useCountsStore()
        await countsStore.refreshCounts()

        message.value = `Undone: ${result.undone?.event_type || 'event'} 
                         at ${result.undone?.location || ''}`
        success.value = true

        return { success: true, undone: result.undone }

      } else {
        message.value = result.message || 'Nothing to undo'
        success.value = false
        return { success: false, message: message.value }
      }

    } catch (err) {
      error.value   = 'Undo failed. Please try again.'
      message.value = error.value
      success.value = false
      console.error('Undo error:', err)
      return { success: false, error: error.value }

    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    lastUndone,
    error,
    message,
    success,
    undo
  }
}