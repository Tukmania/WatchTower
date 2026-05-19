import { config } from '@vue/test-utils'
import { createPinia } from 'pinia'

// Make Pinia available in all tests automatically
// Without this, any component using a store would crash
config.global.plugins = [createPinia()]