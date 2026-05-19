import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
test: {

  //jsdom as a fake browser environment
  environment: 'jsdom',

  //Make the test helper functions globally available in all test files without needing to import them
  globals: true,

  //Run this file before every test file
  //Used to setup Vue Test Utils Globally
  setupFiles: ['./src/tests/setup.js'],

  //where to look for test files
   include: ['src/tests/**/*.test.js'],

   //coverage configuration
     coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include:  ['src/**/*.{vue,js}'],
      exclude:  ['src/tests/**', 'src/main.js']
    }

}


})
