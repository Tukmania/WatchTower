<template>
  <AppShell>
    <div class="event-log-view">

      <!-- Page header -->
      <div class="event-log-view__header">
        <div>
          <h1 class="event-log-view__title">Event Log</h1>
          <p class="event-log-view__sub">
            Full audit trail of all logged events for today's shift
          </p>
        </div>
        <button class="event-log-view__refresh" @click="refresh">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2.5">
            <polyline points="23 4 23 10 17 10"/>
            <path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/>
          </svg>
          Refresh
        </button>
      </div>

      <!-- Table -->
      <EventLogTable />

    </div>
  </AppShell>
</template>

<script setup>
import { onMounted }      from 'vue'
import { useEventStore }  from '../stores/eventStore.js'
import AppShell           from '../components/layout/AppShell.vue'
import EventLogTable      from '../components/events/EventLogTable.vue'

const eventStore = useEventStore()

onMounted(() => eventStore.fetchRecent())

function refresh() {
  eventStore.fetchRecent()
}
</script>

<style scoped>
.event-log-view {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-md);
  height:         100%;
  min-height:     0;
}

.event-log-view__header {
  display:         flex;
  align-items:     flex-start;
  justify-content: space-between;
  flex-shrink:     0;
}

.event-log-view__title {
  font-size:   var(--font-size-xl);
  font-weight: 800;
  color:       var(--color-primary);
}

.event-log-view__sub {
  font-size:  var(--font-size-sm);
  color:      var(--color-text-muted);
  margin-top: 2px;
}

.event-log-view__refresh {
  display:       flex;
  align-items:   center;
  gap:           var(--space-xs);
  padding:       8px var(--space-md);
  background:    var(--color-bg-card);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size:     var(--font-size-sm);
  font-weight:   600;
  color:         var(--color-text-secondary);
  cursor:        pointer;
  transition:    var(--transition);
  font-family:   var(--font-family);
}

.event-log-view__refresh:hover {
  background: var(--color-bg-section);
  color:      var(--color-text-primary);
}
</style>