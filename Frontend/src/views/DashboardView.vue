<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold text-gray-800">
      CCTV Monitoring Dashboard
    </h1>

    <div class="mt-6 p-4 rounded-lg border" :class="statusClass">
      <p class="font-semibold">Backend Status: {{ status }}</p>
      <p class="text-sm mt-1 text-gray-600">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/index.js'

const status  = ref('Checking...')
const message = ref('')
const statusClass = ref('bg-yellow-50 border-yellow-300')

onMounted(async () => {
  try {
    const response = await api.get('/')
    status.value     = '✅ Connected'
    message.value    = response.data.message
    statusClass.value = 'bg-green-50 border-green-300'
  } catch (error) {
    status.value     = '❌ Cannot reach backend'
    message.value    = 'Make sure Flask is running on port 5000'
    statusClass.value = 'bg-red-50 border-red-300'
  }
})
</script>