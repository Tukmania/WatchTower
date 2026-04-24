<template>
  <aside class="summary-panel">

    <!-- Header -->
    <div class="summary-panel__header">
      <div class="summary-panel__header-left">
        <span class="live-dot" />
        <span class="summary-panel__title">Live Summary</span>
      </div>
      <span class="summary-panel__block">{{ currentBlock }}</span>
    </div>

    <!-- Stats grid -->
    <div class="summary-panel__stats">
      <SummaryStatCard
        label="Total Bag Wraps"
        :value="countsStore.totalBagWraps"
        icon="🎒"
        icon-bg="rgba(37,99,235,0.1)"
      />
      <SummaryStatCard
        label="Total Box Wraps"
        :value="countsStore.totalBoxWraps"
        icon="📦"
        icon-bg="rgba(124,58,237,0.1)"
      />
      <SummaryStatCard
        label="Total Foot Traffic"
        :value="countsStore.totalFootTraffic"
        icon="🚶"
        icon-bg="rgba(5,150,105,0.1)"
      />
      <SummaryStatCard
        label="People Interacted"
        :value="countsStore.totalInteractions"
        icon="🤝"
        icon-bg="rgba(37,99,235,0.1)"
      />
      <SummaryStatCard
        label="Walk-ins"
        :value="countsStore.totalWalkins"
        icon="👣"
        icon-bg="rgba(220,38,38,0.1)"
      />
      <SummaryStatCard
        label="Receipts Issued"
        :value="countsStore.totalReceipts"
        icon="🧾"
        icon-bg="rgba(5,150,105,0.1)"
      />
    </div>

    <!-- Divider -->
    <div class="summary-panel__divider" />

    <!-- Quick actions -->
    <QuickActionsBar />

    <!-- Divider -->
    <div class="summary-panel__divider" />

    <!-- Generate report button -->
    <button class="summary-panel__report-btn" @click="handleReport">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2.5">
        <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      Generate Excel Report
    </button>

  </aside>
</template>

<script setup>
import { computed }        from 'vue'
import { useCountsStore }  from '../../stores/countsStore.js'
import { downloadReport }  from '../../api/reports.js'
import SummaryStatCard     from './SummaryStatCard.vue'
import QuickActionsBar     from './QuickActionsBar.vue'

const countsStore  = useCountsStore()
const currentBlock = computed(() => countsStore.currentBlock || '—')

async function handleReport() {
  const date = new Date().toISOString().split('T')[0]
  await downloadReport(date)
}
</script>

<style scoped>
.summary-panel {
  width:          280px;
  min-width:      280px;
  height:         100%;
  display:        flex;
  flex-direction: column;
  gap:            var(--space-md);
  background:     var(--color-bg-card);
  border-left:    1px solid var(--color-border);
  padding:        var(--space-md);
  overflow-y:     auto;
  flex-shrink:    0;
}

/* ── Header ───────────────────────────────────────────────── */
.summary-panel__header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
}

.summary-panel__header-left {
  display:     flex;
  align-items: center;
  gap:         var(--space-xs);
}

.live-dot {
  width:         8px;
  height:        8px;
  background:    var(--color-live);
  border-radius: 50%;
  animation:     pulse 2s ease-in-out infinite;
  flex-shrink:   0;
}

@keyframes pulse {
  0%, 100% { opacity: 1;   transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}

.summary-panel__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
}

.summary-panel__block {
  font-size:     var(--font-size-xs);
  font-weight:   600;
  color:         var(--color-text-muted);
  background:    var(--color-bg-section);
  border:        1px solid var(--color-border);
  padding:       3px 8px;
  border-radius: var(--radius-sm);
  white-space:   nowrap;
}

/* ── Stats ────────────────────────────────────────────────── */
.summary-panel__stats {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
}

/* ── Divider ──────────────────────────────────────────────── */
.summary-panel__divider {
  height:     1px;
  background: var(--color-border);
  flex-shrink: 0;
}

/* ── Report button ────────────────────────────────────────── */
.summary-panel__report-btn {
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             var(--space-sm);
  width:           100%;
  padding:         12px var(--space-md);
  background:      var(--color-primary);
  color:           white;
  border:          none;
  border-radius:   var(--radius-md);
  font-size:       var(--font-size-sm);
  font-weight:     600;
  cursor:          pointer;
  transition:      var(--transition);
  letter-spacing:  0.2px;
  font-family:     var(--font-family);
}

.summary-panel__report-btn:hover {
  background: var(--color-primary-light);
  transform:  translateY(-1px);
  box-shadow: var(--shadow-md);
}

.summary-panel__report-btn:active {
  transform: translateY(0);
}
</style>