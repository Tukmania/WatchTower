import { defineStore } from 'pinia'
import { fetchCounts } from '../api/counts.js'

export const useCountsStore = defineStore('counts', {
  state: () => ({
    terminalCounts: {},
    shopCounts:     {},
    summary:        {},
    blockSummary:   {},
    currentBlock:   '',
    isLoading:      false,
    pollingTimer:   null
  }),

  actions: {
    // Called after every button click and on undo
    async refreshCounts() {
      try {
        const today    = new Date().toISOString().split('T')[0]
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

    // Start auto polling every 10 seconds as a safety net
    startPolling() {
      this.refreshCounts()
      this.pollingTimer = setInterval(() => {
        this.refreshCounts()
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