import { ref }            from 'vue'
import { downloadReport } from '../api/reports.js'

export function useReportExport() {
  const isGenerating = ref(false)
  const error        = ref(null)
  const success      = ref(false)

  async function generate(start, end) {
    isGenerating.value = true
    error.value        = null
    success.value      = false

    try {
      await downloadReport(start, end)
      success.value = true
      setTimeout(() => { success.value = false }, 3000)
      return { success: true }

    } catch (err) {
      error.value = 'Failed to generate report. Check that events exist for this interval.'
      console.error('Report export error:', err)
      return { success: false, error: error.value }

    } finally {
      isGenerating.value = false
    }
  }

  return { isGenerating, error, success, generate }
}
