<template>
  <AppShell>
    <div class="dashboard">

      <!-- Main content area -->
      <div class="dashboard__main">
        <TerminalPanel />
        <ShopsPanel />
        <RecentEventsFeed />
      </div>

      <!-- Right summary panel -->
      <LiveSummaryPanel />

    </div>
  </AppShell>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useCountsStore }         from '../stores/countsStore.js'
import { useEventStore }          from '../stores/eventStore.js'
import AppShell                   from '../components/layout/AppShell.vue'
import TerminalPanel              from '../components/terminals/TerminalPanel.vue'
import ShopsPanel                 from '../components/shops/ShopsPanel.vue'
import LiveSummaryPanel           from '../components/dashboard/LiveSummaryPanel.vue'
import RecentEventsFeed           from '../components/events/RecentEventsFeed.vue'

const countsStore = useCountsStore()
const eventStore  = useEventStore()

onMounted(async () => {
  await eventStore.fetchRecent()
  countsStore.startPolling()
})

onUnmounted(() => {
  countsStore.stopPolling()
})
</script>

<style scoped>
.dashboard {
  display:   flex;
  gap:       var(--space-md);
  height:    100%;
  min-height: 0;
}

.dashboard__main {
  flex:           1;
  display:        flex;
  flex-direction: column;
  gap:            var(--space-md);
  overflow-y:     auto;
  min-width:      0;
  padding-right:  var(--space-xs);
}
</style>