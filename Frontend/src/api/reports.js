import api from './index.js'

export async function downloadReport(start, end) {
  const response = await api.get('/api/report', {
    params:       { start, end },
    responseType: 'blob'
  })

  const safe = (s) => s.replace('T', '_').replace(':', '').replace(':', '')
  const filename = `CCTV_Report_${safe(start)}_to_${safe(end)}.xlsx`

  const url  = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href  = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
