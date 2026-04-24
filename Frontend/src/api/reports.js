import api from './index.js'

export async function downloadReport(date) {
  const response = await api.get('/api/report', {
    params:       { date },
    responseType: 'blob'   // tells Axios to treat the response as a file
  })

  // Build a temporary download link and click it
  const url      = window.URL.createObjectURL(new Blob([response.data]))
  const link     = document.createElement('a')
  link.href      = url
  link.setAttribute('download', `CCTV_Report_${date}.xlsx`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}