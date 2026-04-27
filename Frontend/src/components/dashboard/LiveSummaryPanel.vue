<template>
  <aside class="summary-panel">

    <!-- Header -->
    <div class="panel-header">
      <div class="panel-header__left">
        <span class="live-dot" />
        <span class="panel-title">Hourly Reports</span>
      </div>
      <span class="panel-block-badge">{{ currentBlock }}</span>
    </div>

    <!-- Scrollable hourly feed -->
    <div class="hourly-feed">
      <div v-if="!hourSlots.length" class="hourly-empty">
        No shift data yet
      </div>

      <div v-for="slot in hourSlots" :key="slot.key" class="hour-block">

        <!-- Hour heading -->
        <div class="hour-heading">HOURLY REPORT {{ slot.label }}</div>

        <!-- Terminals -->
        <div class="sub-section sub-section--border">
          <div
            v-for="t in TERMINAL_LIST"
            :key="t.name"
            class="mono-line"
            :class="{
              'mono-line--muted':    noActivity(slot, t.name) && statusStore.isOnline(t.name),
              'mono-line--offline':  !statusStore.isOnline(t.name)
            }"
          >{{ dotLine(t.short, terminalText(slot, t.name)) }}</div>
        </div>

        <!-- Shops -->
        <div
          v-for="(s, idx) in SHOP_LIST"
          :key="s.name"
          class="sub-section"
          :class="{ 'sub-section--border': idx < SHOP_LIST.length - 1 }"
        >
          <div class="shop-heading">{{ s.short }}</div>
          <template v-if="statusStore.isOnline(s.name)">
            <template v-if="!s.walkInOnly">
              <div class="mono-line">{{ dotLine('Interactions', shopVal(slot, s.name, 'interaction')) }}</div>
              <div class="mono-line">{{ dotLine('Receipts',     shopVal(slot, s.name, 'receipt')) }}</div>
            </template>
            <div class="mono-line">{{ dotLine('Walk In', shopVal(slot, s.name, 'walkin')) }}</div>
          </template>
          <div v-else class="mono-line mono-line--offline">OfflineMode</div>
        </div>

      </div>
    </div>

    <!-- Divider -->
    <div class="h-divider" />

    <!-- Quick actions -->
    <QuickActionsBar />

    <!-- Divider -->
    <div class="h-divider" />

    <!-- Generate report button -->
    <button class="report-btn" @click="handleReport">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter }         from 'vue-router'
import { useCountsStore }    from '../../stores/countsStore.js'
import { useStatusStore }    from '../../stores/statusStore.js'
import { fetchHourlyCounts } from '../../api/counts.js'
import QuickActionsBar       from './QuickActionsBar.vue'

// ── Location lists ─────────────────────────────────────────────────────────────
const TERMINAL_LIST = [
  { name: 'TERMINAL 1A', short: 'T1A' },
  { name: 'TERMINAL 1B', short: 'T1B' },
  { name: 'TERMINAL 1C', short: 'T1C' },
  { name: 'TERMINAL 1D', short: 'T1D' },
  { name: 'MARINA',      short: 'Marina' }
]

const SHOP_LIST = [
  { name: 'LAOMAI JKIA',                  short: 'LAOMAI JKIA',              walkInOnly: false },
  { name: 'LAOMAI MOMBASA',               short: 'LAOMAI MSA',               walkInOnly: false },
  { name: 'CRAYSON PHARMACY JKIA',        short: 'CRAYSON PHARMACY JKIA',    walkInOnly: false },
  { name: 'CRAYSON PHARMACY KIAMBU ROAD', short: 'CRAYSON PHARMACY KIAMBU RD', walkInOnly: false },
  { name: 'CRAYSON PHARMACY MOMBASA',     short: 'CRAYSON PHARMACY MOMBASA', walkInOnly: false },
  { name: 'SKYLINE GYM',                  short: 'SKYLINE GYM',              walkInOnly: true  }
]

// ── State ──────────────────────────────────────────────────────────────────────
const countsStore  = useCountsStore()
const statusStore  = useStatusStore()
const currentBlock = computed(() => countsStore.currentBlock || '—')
const hourlyData   = ref({})
let   pollTimer    = null

// ── Dot-leader line builder ────────────────────────────────────────────────────
function dotLine(label, value, width = 32) {
  const l = String(label)
  const v = String(value)
  const dots = Math.max(2, width - l.length - v.length)
  return l + '.'.repeat(dots) + v
}

// ── Hour key / label helpers ───────────────────────────────────────────────────
function pad(n) { return String(n).padStart(2, '0') }

function buildHourKey(h) {
  const endH = (h + 1) % 24
  return `${pad(h)}:00 – ${pad(endH)}:00`
}

function getShiftHours() {
  const h = new Date().getHours()
  if (h >= 7 && h <= 17) {
    return Array.from({ length: h - 7 + 1 }, (_, i) => 7 + i)
  }
  if (h >= 18) {
    return Array.from({ length: h - 18 + 1 }, (_, i) => 18 + i)
  }
  // Early morning 00–06: rest of nightshift
  return [
    ...Array.from({ length: 6 }, (_, i) => 18 + i),
    ...Array.from({ length: h + 1 }, (_, i) => i)
  ]
}

// ── Computed slots (most recent first) ────────────────────────────────────────
const hourSlots = computed(() => {
  return [...getShiftHours()].reverse().map(h => {
    const endH  = (h + 1) % 24
    const key   = buildHourKey(h)
    const label = `${pad(h)}00HRS - ${pad(endH)}00HRS`
    const data  = hourlyData.value[key] || { terminals: {}, shops: {} }
    return { key, label, data }
  })
})

// ── Row value helpers ──────────────────────────────────────────────────────────
function noActivity(slot, terminalName) {
  const d = slot.data.terminals[terminalName]
  if (!d) return true
  return (d.bag_wrap || 0) === 0 && (d.box_wrap || 0) === 0
}

function terminalText(slot, terminalName) {
  if (!statusStore.isOnline(terminalName)) return 'OfflineMode'
  if (noActivity(slot, terminalName)) return 'No activities'
  const d = slot.data.terminals[terminalName]
  return `${d.bag_wrap || 0} Bags ${d.box_wrap || 0} Boxes`
}

function shopVal(slot, shopName, metric) {
  const d = slot.data.shops[shopName]
  if (!d) return 0
  return d[metric] || 0
}

// ── Data fetching ──────────────────────────────────────────────────────────────
async function fetchHourly() {
  try {
    const date = new Date().toISOString().split('T')[0]
    const res  = await fetchHourlyCounts(date)
    hourlyData.value = res.data
  } catch (err) {
    console.error('Failed to fetch hourly counts:', err)
  }
}

onMounted(() => {
  fetchHourly()
  pollTimer = setInterval(fetchHourly, 10000)
})

onUnmounted(() => {
  clearInterval(pollTimer)
})

// ── Report button → navigate to Reports view for interval selection ────────────
const router = useRouter()
function handleReport() {
  router.push('/reports')
}
</script>

<style scoped>
/* ── Panel shell ──────────────────────────────────────────────────────────────── */
.summary-panel {
  width:           310px;
  min-width:       310px;
  height:          100%;
  display:         flex;
  flex-direction:  column;
  background:      var(--color-bg-card);
  border-left:     1px solid var(--color-border);
  padding:         12px;
  gap:             10px;
  flex-shrink:     0;
  overflow:        hidden;
  box-sizing:      border-box;
}

/* ── Header ───────────────────────────────────────────────────────────────────── */
.panel-header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  flex-shrink:     0;
}

.panel-header__left {
  display:     flex;
  align-items: center;
  gap:         6px;
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

.panel-title {
  font-size:   14px;
  font-weight: 700;
  color:       var(--color-primary);
}

.panel-block-badge {
  font-size:     10px;
  font-weight:   600;
  color:         var(--color-text-muted);
  background:    var(--color-bg-section);
  border:        1px solid var(--color-border);
  padding:       2px 7px;
  border-radius: 4px;
  white-space:   nowrap;
}

/* ── Scrollable feed ──────────────────────────────────────────────────────────── */
.hourly-feed {
  flex:            1;
  min-height:      0;
  overflow-y:      scroll;
  display:         flex;
  flex-direction:  column;
  gap:             8px;
  padding-right:   2px;
}

/* Always-visible thin scrollbar */
.hourly-feed::-webkit-scrollbar        { width: 4px; }
.hourly-feed::-webkit-scrollbar-track  { background: var(--color-bg-section); border-radius: 2px; }
.hourly-feed::-webkit-scrollbar-thumb  { background: var(--color-border); border-radius: 2px; }
.hourly-feed::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }

.hourly-empty {
  font-size:  12px;
  color:      var(--color-text-muted);
  text-align: center;
  padding:    16px 0;
}

/* ── Hour block ───────────────────────────────────────────────────────────────── */
.hour-block {
  border:        1px solid var(--color-border);
  border-radius: 4px;
}

.hour-heading {
  background:     var(--color-primary);
  color:          #fff;
  font-family:    'Courier New', Courier, monospace;
  font-size:      9px;
  font-weight:    700;
  letter-spacing: 0.4px;
  padding:        4px 8px;
  border-radius:  3px 3px 0 0;
}

/* ── Sub-sections (terminals block + each shop block) ─────────────────────────── */
.sub-section {
  padding: 4px 8px;
}

.sub-section--border {
  border-bottom: 1px solid var(--color-border);
}

.shop-heading {
  font-family:    'Courier New', Courier, monospace;
  font-size:      9px;
  font-weight:    700;
  text-transform: uppercase;
  text-align:     center;
  color:          var(--color-text-muted);
  padding-bottom: 2px;
  letter-spacing: 0.3px;
}

/* ── Monospace dot-leader lines ───────────────────────────────────────────────── */
.mono-line {
  font-family: 'Courier New', Courier, monospace;
  font-size:   10px;
  line-height: 1.55;
  white-space: nowrap;
  overflow:    hidden;
  color:       var(--color-text);
}

.mono-line--muted {
  color:      var(--color-text-muted);
  font-style: italic;
}

.mono-line--offline {
  color:       var(--color-danger, #dc2626);
  font-style:  italic;
  font-weight: 600;
}

/* ── Divider ──────────────────────────────────────────────────────────────────── */
.h-divider {
  height:      1px;
  background:  var(--color-border);
  flex-shrink: 0;
}

/* ── Report button ────────────────────────────────────────────────────────────── */
.report-btn {
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             8px;
  width:           100%;
  padding:         11px 16px;
  background:      var(--color-primary);
  color:           white;
  border:          none;
  border-radius:   6px;
  font-size:       13px;
  font-weight:     600;
  cursor:          pointer;
  transition:      var(--transition);
  letter-spacing:  0.2px;
  font-family:     var(--font-family);
  flex-shrink:     0;
}

.report-btn:hover {
  background: var(--color-primary-light);
  transform:  translateY(-1px);
  box-shadow: var(--shadow-md);
}

.report-btn:active {
  transform: translateY(0);
}
</style>
