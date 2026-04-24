<template>
  <div class="live-clock">
    <span class="live-clock__time">{{ time }}</span>
    <span class="live-clock__date">{{ date }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const time  = ref('')
const date  = ref('')
let   timer = null

function tick() {
  const now = new Date()

  time.value = now.toLocaleTimeString('en-GB', {
    hour:   '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })

  date.value = now.toLocaleDateString('en-GB', {
    weekday: 'short',
    day:     '2-digit',
    month:   'short',
    year:    'numeric'
  })
}

onMounted(() => {
  tick()
  timer = setInterval(tick, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.live-clock {
  display:        flex;
  flex-direction: column;
  align-items:    flex-end;
  gap:            1px;
}

.live-clock__time {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-text-white);
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.5px;
}

.live-clock__date {
  font-size: var(--font-size-xs);
  color:     rgba(255,255,255,0.55);
  letter-spacing: 0.3px;
}
</style>