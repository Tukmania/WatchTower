import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  function setTheme(dark) {
    isDark.value = dark
  }

  return { isDark, setTheme }
}, { persist: true })
