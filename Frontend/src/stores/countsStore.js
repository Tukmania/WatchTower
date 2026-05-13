import { defineStore } from 'pinia'
import { fetchCounts, fetchHourlyCounts } from '../api/counts.js'

function localDateString() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}

export const useCountsStore = defineStore('counts', {
  state: () => ({
    terminalCounts: {},
    shopCounts:     {},
    summary:        {},
    blockSummary:   {},
    currentBlock:   '',
    hourlyData:     {},
    isLoading:      false,
    pollingTimer:   null
  }),

  actions: {
    // Called after every button click and on undo
    async refreshCounts() {
      try {
        const today    = localDateString()
        const response = await fetchCounts(today)
        const data     = response.data

        this.terminalCounts = data.terminals     || {}
        this.shopCounts     = data.shops         || {}
        this.summary        = data.summary       || {}
        this.blockSummary   = data.block_summary || {}
        this.currentBlock   = data.current_block || ''

      } catch (err) {
        console.error('Failed to refresh counts:', err)
      }
    },

    async refreshHourly() {
      try {
        const today = localDateString()
        const res   = await fetchHourlyCounts(today)
        this.hourlyData = res.data
      } catch (err) {
        console.error('Failed to refresh hourly counts:', err)
      }
    },

    // Start auto polling every 10 seconds as a safety net
    startPolling() {
      this.refreshCounts()
      this.refreshHourly()
      this.pollingTimer = setInterval(() => {
        this.refreshCounts()
        this.refreshHourly()
      }, 10000)
    },

    // Stop polling when app is closed or hidden
    stopPolling() {
      if (this.pollingTimer) {
        clearInterval(this.pollingTimer)
        this.pollingTimer = null
      }
    }
  },

  getters: {
    // Easy access to a single terminal's counts
    getTerminalCounts: (state) => (terminalName) => {
      return state.terminalCounts[terminalName] || {
        bag_wrap:     0,
        box_wrap:     0,
        foot_traffic: 0
      }
    },

    // Easy access to a single shop's counts
    getShopCounts: (state) => (shopName) => {
      return state.shopCounts[shopName] || {
        interaction: 0,
        walkin:      0,
        receipt:     0
      }
    },

    // Summary totals for right panel
    totalBagWraps:    (state) => state.summary.bag_wraps    || 0,
    totalBoxWraps:    (state) => state.summary.box_wraps    || 0,
    totalFootTraffic: (state) => state.summary.foot_traffic || 0,
    totalInteractions:(state) => state.summary.interactions || 0,
    totalWalkins:     (state) => state.summary.walkins      || 0,
    totalReceipts:    (state) => state.summary.receipts     || 0
  }
})