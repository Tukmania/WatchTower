import { defineStore } from 'pinia'

const STORAGE_KEY = 'watchtower_location_status'

function load() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') }
  catch { return {} }
}

export const useStatusStore = defineStore('status', {
  state: () => ({
    // { 'TERMINAL 1A': false } means offline; absent or true means online
    statuses: load()
  }),

  getters: {
    isOnline: (state) => (name) => state.statuses[name] !== false
  },

  actions: {
    toggle(name) {
      this.statuses[name] = !this.isOnline(name)
      this._save()
    },
    _save() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.statuses))
    }
  }
})
