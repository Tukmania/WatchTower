import { ref }            from 'vue'
import { downloadReport } from '../api/reports.js'

export function useReportExport() {
  const isGenerating = ref(false)
  const error        = ref(null)
  const success      = ref(false)

  async function generate(date) {
    isGenerating.value = true
    error.value        = null
    success.value      = false

    try {
      await downloadReport(date)
      success.value = true

      // Reset success flag after 3 seconds
      setTimeout(() => { success.value = false }, 3000)

      return { success: true }

    } catch (err) {
      error.value = 'Failed to generate report. Make sure there are events logged for this date.'
      console.error('Report export error:', err)
      return { success: false, error: error.value }

    } finally {
      isGenerating.value = false
    }
  }

  return {
    isGenerating,
    error,
    success,
    generate
  }
}