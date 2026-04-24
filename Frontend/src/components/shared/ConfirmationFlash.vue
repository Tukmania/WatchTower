<script setup>
import { ref, computed, watch } from 'vue'
import { useEventStore } from '../../stores/eventStore.js'

const eventStore = useEventStore()

const visible   = ref(false)
const lastEvent = ref(null)
let   hideTimer = null

// ── Derive display info from the last logged event ────────────
const type = computed(() => {
  if (!lastEvent.value) return 'default'
  const subtype    = lastEvent.value.subtype
  const event_type = lastEvent.value.event_type
  if (subtype === 'bag_wrap')     return 'bag-wrap'
  if (subtype === 'box_wrap')     return 'box-wrap'
  if (subtype === 'foot_traffic') return 'foot-traffic'
  if (event_type === 'interaction') return 'interaction'
  if (event_type === 'walkin')      return 'walkin'
  if (event_type === 'receipt')     return 'receipt'
  return 'default'
})

const icon = computed(() => {
  const map = {
    'bag-wrap':     '🎒',
    'box-wrap':     '📦',
    'foot-traffic': '🚶',
    'interaction':  '🤝',
    'walkin':       '🚶',
    'receipt':      '🧾',
    'default':      '✅'
  }
  return map[type.value] || '✅'
})

const title = computed(() => {
  if (!lastEvent.value) return 'Logged'
  const subtype    = lastEvent.value.subtype
  const event_type = lastEvent.value.event_type
  if (subtype === 'bag_wrap')       return 'Bag Wrap'
  if (subtype === 'box_wrap')       return 'Box Wrap'
  if (subtype === 'foot_traffic')   return 'Foot Traffic'
  if (event_type === 'interaction') return 'Interaction'
  if (event_type === 'walkin')      return 'Walk-in'
  if (event_type === 'receipt')     return 'Receipt'
  return 'Event Logged'
})

const detail = computed(() => {
  if (!lastEvent.value) return ''
  return lastEvent.value.location || ''
})

const timeBlock = computed(() => {
  if (!lastEvent.value) return ''
  return lastEvent.value.time_block || ''
})

// ── Watch event store for new events ─────────────────────────
// Every time a new event is prepended, show the flash
watch(
  () => eventStore.recentEvents[0],
  (newEvent) => {
    if (!newEvent) return

    lastEvent.value = newEvent

    // Clear any existing timer so rapid clicks reset the timer
    if (hideTimer) clearTimeout(hideTimer)

    visible.value = true

    // Auto-hide after 1.8 seconds
    hideTimer = setTimeout(() => {
      visible.value = false
    }, 1800)
  }
)
</script>

<template>
  <Teleport to="body">
    <Transition name="flash">
      <div
        v-if="visible"
        class="flash-overlay"
        :class="`flash-overlay--${type}`"
      >
        <div class="flash-card">

          <div class="flash-card__icon">{{ icon }}</div>

          <div class="flash-card__content">
            <p class="flash-card__title">{{ title }}</p>
            <p class="flash-card__detail">{{ detail }}</p>
          </div>

          <div class="flash-card__block">
            <span class="flash-card__block-label">block</span>
            <span class="flash-card__block-value">{{ timeBlock }}</span>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>



<style scoped>
/* ── Positioning — bottom right, non-intrusive ────────────── */
.flash-overlay {
  position:      fixed;
  bottom:        var(--space-xl);
  right:         var(--space-xl);
  z-index:       9999;
  pointer-events: none;
}

/* ── Card ─────────────────────────────────────────────────── */
.flash-card {
  display:       flex;
  align-items:   center;
  gap:           var(--space-md);
  padding:       var(--space-md) var(--space-lg);
  background:    var(--color-primary);
  border-radius: var(--radius-lg);
  box-shadow:    var(--shadow-lg);
  min-width:     280px;
  border-left:   4px solid transparent;
  position:      relative;
  overflow:      hidden;
}

/* ── Progress bar at bottom — drains over 1.8s ───────────── */
.flash-card::after {
  content:          '';
  position:         absolute;
  bottom:           0;
  left:             0;
  height:           3px;
  width:            100%;
  background:       rgba(255, 255, 255, 0.35);
  transform-origin: left;
  animation:        drain 1.8s linear forwards;
}

@keyframes drain {
  from { transform: scaleX(1); }
  to   { transform: scaleX(0); }
}

/* ── Color variants — left border changes per event type ─── */
.flash-overlay--bag-wrap     .flash-card { border-left-color: #60a5fa; }
.flash-overlay--box-wrap     .flash-card { border-left-color: #a78bfa; }
.flash-overlay--foot-traffic .flash-card { border-left-color: #34d399; }
.flash-overlay--interaction  .flash-card { border-left-color: #60a5fa; }
.flash-overlay--walkin       .flash-card { border-left-color: #f87171; }
.flash-overlay--receipt      .flash-card { border-left-color: #34d399; }

/* ── Icon ─────────────────────────────────────────────────── */
.flash-card__icon {
  font-size:   24px;
  flex-shrink: 0;
}

/* ── Content ──────────────────────────────────────────────── */
.flash-card__content {
  flex: 1;
}

.flash-card__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-text-white);
  line-height: 1.2;
}

.flash-card__detail {
  font-size:  var(--font-size-sm);
  color:      rgba(255, 255, 255, 0.65);
  margin-top: 2px;
}

/* ── Time block badge ─────────────────────────────────────── */
.flash-card__block {
  display:        flex;
  flex-direction: column;
  align-items:    flex-end;
  gap:            2px;
  flex-shrink:    0;
}

.flash-card__block-label {
  font-size:      var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color:          rgba(255, 255, 255, 0.45);
}

.flash-card__block-value {
  font-size:   var(--font-size-sm);
  font-weight: 700;
  color:       rgba(255, 255, 255, 0.9);
  white-space: nowrap;
}

/* ── Enter / Leave transition ─────────────────────────────── */
.flash-enter-active {
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.flash-leave-active {
  transition: all 0.25s ease-in;
}

.flash-enter-from {
  opacity:   0;
  transform: translateX(60px) scale(0.92);
}

.flash-leave-to {
  opacity:   0;
  transform: translateX(20px) scale(0.96);
}
</style>