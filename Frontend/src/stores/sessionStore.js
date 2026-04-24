import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    operatorName: 'Operator',
    shiftDate:    new Date().toISOString().split('T')[0],
    shiftStart:   null
  }),

  actions: {
    setOperatorName(name) {
      this.operatorName = name || 'Operator'
    },

    setShiftDate(date) {
      this.shiftDate = date
    },

    startShift() {
      this.shiftStart = new Date().toISOString()
    }
  },

  getters: {
    // Formatted date for display in topbar e.g. "Mon, 28 Nov 2025"
    formattedDate: (state) => {
      return new Date(state.shiftDate).toLocaleDateString('en-GB', {
        weekday: 'short',
        day:     '2-digit',
        month:   'short',
        year:    'numeric'
      })
    },

    // How long the shift has been running
    shiftDuration: (state) => {
      if (!state.shiftStart) return null
      const start   = new Date(state.shiftStart)
      const now     = new Date()
      const minutes = Math.floor((now - start) / 60000)
      const hours   = Math.floor(minutes / 60)
      const mins    = minutes % 60
      return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}`
    }
  },

  // Persist operator name across page refreshes
  persist: true
})