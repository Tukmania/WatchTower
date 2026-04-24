<template>
  <div class="event-row" :class="{ 'event-row--new': isNew }">

    <!-- Time -->
    <div class="event-row__time">
      <span class="event-row__time-value">{{ formattedTime }}</span>
      <span class="event-row__time-block">{{ event.time_block }}</span>
    </div>

    <!-- Location -->
    <div class="event-row__location">
      <span class="event-row__location-icon">
        {{ event.location_category === 'terminal' ? '✈️' : '🏪' }}
      </span>
      <span class="event-row__location-name">{{ event.location }}</span>
    </div>

    <!-- Badge -->
    <div class="event-row__badge">
      <EventTypeBadge
        :type="event.event_type"
        :subtype="event.subtype"
      />
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import EventTypeBadge from './EventTypeBadge.vue'

const props = defineProps({
  event: { type: Object, required: true }
})

// Flash new row briefly when it appears
const isNew = ref(true)
onMounted(() => {
  setTimeout(() => { isNew.value = false }, 800)
})

const formattedTime = computed(() => {
  if (!props.event.timestamp) return ''
  // timestamp format: "2025-11-28 10:24:10"
  const parts = props.event.timestamp.split(' ')
  return parts[1] ? parts[1].slice(0, 8) : props.event.timestamp
})
</script>

<style scoped>
.event-row {
  display:       grid;
  grid-template-columns: 130px 1fr auto;
  align-items:   center;
  gap:           var(--space-md);
  padding:       10px var(--space-md);
  border-radius: var(--radius-md);
  transition:    background 0.2s ease;
  border:        1px solid transparent;
}

.event-row:hover {
  background: var(--color-bg-section);
}

/* Flash highlight for brand new rows */
.event-row--new {
  background:   rgba(37, 99, 235, 0.05);
  border-color: rgba(37, 99, 235, 0.12);
  animation:    row-appear 0.8s ease forwards;
}

@keyframes row-appear {
  0%   { background: rgba(37, 99, 235, 0.1); }
  100% { background: transparent; border-color: transparent; }
}

/* ── Time ─────────────────────────────────────────────────── */
.event-row__time {
  display:        flex;
  flex-direction: column;
  gap:            2px;
}

.event-row__time-value {
  font-size:   var(--font-size-sm);
  font-weight: 600;
  color:       var(--color-text-primary);
  font-variant-numeric: tabular-nums;
}

.event-row__time-block {
  font-size: var(--font-size-xs);
  color:     var(--color-text-muted);
}

/* ── Location ─────────────────────────────────────────────── */
.event-row__location {
  display:     flex;
  align-items: center;
  gap:         var(--space-xs);
  min-width:   0;
}

.event-row__location-icon {
  font-size:   13px;
  flex-shrink: 0;
}

.event-row__location-name {
  font-size:     var(--font-size-sm);
  font-weight:   500;
  color:         var(--color-text-secondary);
  white-space:   nowrap;
  overflow:      hidden;
  text-overflow: ellipsis;
}

/* ── Badge ────────────────────────────────────────────────── */
.event-row__badge {
  display:     flex;
  justify-content: flex-end;
  flex-shrink: 0;
}
</style>