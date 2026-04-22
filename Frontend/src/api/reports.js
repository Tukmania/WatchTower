import api from './index.js'

export const downloadReport = async (date) => {
  const response = await api.get('/api/report', {
    params: { date },
    responseType: 'blob'
  })

  // Trigger browser file download
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `CCTV_Report_${date}.xlsx`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}