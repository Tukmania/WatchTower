<template>
  <div class="feed card">

    <!-- Header -->
    <div class="feed__header">
      <div class="feed__header-left">
        <span class="feed__header-icon">⚡</span>
        <h3 class="feed__title">Recent Events</h3>
        <span class="feed__count">{{ eventStore.lastTen.length }}</span>
      </div>
      <div class="feed__header-right">
        <span class="feed__live-indicator">
          <span class="feed__live-dot" />
          Live
        </span>
        <RouterLink to="/events" class="feed__view-all">
          View all →
        </RouterLink>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="eventStore.isLoading" class="feed__loading">
      <div class="feed__spinner" />
      <span>Loading events...</span>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="eventStore.lastTen.length === 0"
      class="feed__empty"
    >
      <span class="feed__empty-icon">📋</span>
      <p class="feed__empty-title">No events yet</p>
      <p class="feed__empty-sub">
        Events will appear here as you log them
      </p>
    </div>

    <!-- Event rows -->
    <div v-else class="feed__list" ref="feedList">
      <TransitionGroup name="feed-item" tag="div">
        <EventLogRow
          v-for="event in eventStore.lastTen"
          :key="event.id"
          :event="event"
        />
      </TransitionGroup>
    </div>

  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { RouterLink }           from 'vue-router'
import { useEventStore }        from '../../stores/eventStore.js'
import EventLogRow              from './EventLogRow.vue'

const eventStore = useEventStore()
const feedList   = ref(null)

// Auto-scroll to top when new events come in
watch(
  () => eventStore.recentEvents[0],
  async () => {
    await nextTick()
    if (feedList.value) {
      feedList.value.scrollTop = 0
    }
  }
)
</script>

<style scoped>
.feed {
  display:        flex;
  flex-direction: column;
  overflow:       hidden;
  flex-shrink:    0;
}

/* ── Header ───────────────────────────────────────────────── */
.feed__header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding:         var(--space-md);
  border-bottom:   1px solid var(--color-border);
  flex-shrink:     0;
}

.feed__header-left {
  display:     flex;
  align-items: center;
  gap:         var(--space-sm);
}

.feed__header-icon {
  font-size: 16px;
}

.feed__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
}

.feed__count {
  display:         inline-flex;
  align-items:     center;
  justify-content: center;
  width:           22px;
  height:          22px;
  background:      var(--color-primary);
  color:           white;
  border-radius:   50%;
  font-size:       var(--font-size-xs);
  font-weight:     700;
}

.feed__header-right {
  display:     flex;
  align-items: center;
  gap:         var(--space-md);
}

.feed__live-indicator {
  display:     flex;
  align-items: center;
  gap:         5px;
  font-size:   var(--font-size-xs);
  font-weight: 600;
  color:       var(--color-live);
}

.feed__live-dot {
  width:         6px;
  height:        6px;
  background:    var(--color-live);
  border-radius: 50%;
  animation:     pulse 2s ease-in-out infinite;
  flex-shrink:   0;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

.feed__view-all {
  font-size:       var(--font-size-xs);
  font-weight:     600;
  color:           var(--color-primary-light);
  text-decoration: none;
  transition:      var(--transition);
}

.feed__view-all:hover {
  color: var(--color-primary);
}

/* ── Loading ──────────────────────────────────────────────── */
.feed__loading {
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             var(--space-sm);
  padding:         var(--space-xl);
  color:           var(--color-text-muted);
  font-size:       var(--font-size-sm);
}

.feed__spinner {
  width:         18px;
  height:        18px;
  border:        2px solid var(--color-border);
  border-top:    2px solid var(--color-primary-light);
  border-radius: 50%;
  animation:     spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Empty state ──────────────────────────────────────────── */
.feed__empty {
  display:         flex;
  flex-direction:  column;
  align-items:     center;
  justify-content: center;
  padding:         var(--space-xl);
  gap:             var(--space-sm);
  text-align:      center;
}

.feed__empty-icon {
  font-size:    32px;
  margin-bottom: var(--space-xs);
}

.feed__empty-title {
  font-size:   var(--font-size-md);
  font-weight: 600;
  color:       var(--color-text-secondary);
}

.feed__empty-sub {
  font-size: var(--font-size-sm);
  color:     var(--color-text-muted);
}

/* ── List ─────────────────────────────────────────────────── */
.feed__list {
  overflow-y: auto;
  flex:       1;
  padding:    var(--space-sm);
}

/* ── TransitionGroup animations ───────────────────────────── */
.feed-item-enter-active {
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feed-item-leave-active {
  transition: all 0.2s ease-in;
}

.feed-item-enter-from {
  opacity:   0;
  transform: translateY(-12px) scale(0.97);
}

.feed-item-leave-to {
  opacity:   0;
  transform: translateX(20px);
}

.feed-item-move {
  transition: transform 0.25s ease;
}
</style>