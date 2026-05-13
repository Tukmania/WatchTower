<template>
  <AppShell>
    <div class="reports-view">

      <!-- Page header -->
      <div class="reports-view__header">
        <div>
          <h1 class="reports-view__title">Reports</h1>
          <p class="reports-view__sub">
            Generate and download a shift Excel report for any time interval
          </p>
        </div>
      </div>

      <div class="reports-view__body">

        <!-- Generator card -->
        <div class="report-card card">

          <div class="report-card__header">
            <div class="report-card__header-icon">
              <svg width="22" height="22" viewBox="0 0 24 24"
                   fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div>
              <h2 class="report-card__title">Generate Excel Report</h2>
              <p class="report-card__sub">
                Choose the start and end of your shift to include all events
                within that interval in the report
              </p>
            </div>
          </div>

          <div class="report-card__body">

            <!-- Quick-select shift presets -->
            <div class="presets">
              <span class="presets__label">Quick select:</span>
              <button class="preset-btn" @click="applyPreset('day')">Today Day Shift</button>
              <button class="preset-btn" @click="applyPreset('night')">Tonight Night Shift</button>
              <button class="preset-btn" @click="applyPreset('lastNight')">Last Night Shift</button>
            </div>

            <!-- Start datetime -->
            <div class="report-field">
              <label class="report-field__label">Start</label>
              <input
                v-model="startDt"
                type="datetime-local"
                class="report-field__input"
              />
            </div>

            <!-- End datetime -->
            <div class="report-field">
              <label class="report-field__label">End</label>
              <input
                v-model="endDt"
                type="datetime-local"
                class="report-field__input"
              />
            </div>

            <!-- Interval summary -->
            <div v-if="intervalLabel" class="interval-summary">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                   stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              {{ intervalLabel }}
            </div>

            <!-- Validation error -->
            <div v-if="validationError" class="field-error">
              {{ validationError }}
            </div>

            <!-- Generate button -->
            <button
              class="report-btn"
              :class="{ 'report-btn--loading': isGenerating,
                        'report-btn--success': success }"
              :disabled="isGenerating || !!validationError || !startDt || !endDt"
              @click="handleGenerate"
            >
              <template v-if="isGenerating">
                <span class="report-btn__spinner" />
                Generating Report...
              </template>
              <template v-else-if="success">
                <svg width="18" height="18" viewBox="0 0 24 24"
                     fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Report Downloaded!
              </template>
              <template v-else>
                <svg width="18" height="18" viewBox="0 0 24 24"
                     fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Generate Excel Report
              </template>
            </button>

            <!-- API error -->
            <Transition name="fade-msg">
              <div v-if="error" class="report-error">
                <svg width="16" height="16" viewBox="0 0 24 24"
                     fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {{ error }}
              </div>
            </Transition>

          </div>
        </div>

        <!-- Info card -->
        <div class="info-card card">

          <div class="info-card__header">
            <h3 class="info-card__title">What's included in the report</h3>
          </div>

          <div class="info-card__body">

            <div class="info-sheet">
              <div class="info-sheet__badge info-sheet__badge--blue">Sheet 1</div>
              <div class="info-sheet__content">
                <p class="info-sheet__name">Terminal Wraps</p>
                <p class="info-sheet__desc">
                  Bag wraps, box wraps and foot traffic per terminal,
                  grouped by 30-minute time blocks with totals row
                </p>
              </div>
            </div>

            <div class="info-divider" />

            <div class="info-sheet">
              <div class="info-sheet__badge info-sheet__badge--amber">Sheet 2</div>
              <div class="info-sheet__content">
                <p class="info-sheet__name">Shop Activity</p>
                <p class="info-sheet__desc">
                  Interactions, walk-ins and receipt counts per shop,
                  grouped by 30-minute time blocks with totals row
                </p>
              </div>
            </div>

            <div class="info-divider" />

            <div class="info-sheet">
              <div class="info-sheet__badge info-sheet__badge--green">Sheet 3</div>
              <div class="info-sheet__content">
                <p class="info-sheet__name">Raw Event Log</p>
                <p class="info-sheet__desc">
                  Every individual event with exact timestamp, location,
                  category, event type and time block
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useReportExport } from '../composables/useReportExport.js'
import AppShell            from '../components/layout/AppShell.vue'

const { isGenerating, error, success, generate } = useReportExport()

// ── Datetime helpers ───────────────────────────────────────────────────────────
function toLocal(date) {
  // Returns "YYYY-MM-DDTHH:MM" in local time for datetime-local inputs
  const y  = date.getFullYear()
  const mo = String(date.getMonth() + 1).padStart(2, '0')
  const d  = String(date.getDate()).padStart(2, '0')
  const h  = String(date.getHours()).padStart(2, '0')
  const mi = String(date.getMinutes()).padStart(2, '0')
  return `${y}-${mo}-${d}T${h}:${mi}`
}

function smartDefaults() {
  const now  = new Date()
  const h    = now.getHours()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1)
  const tomorrow  = new Date(today); tomorrow.setDate(today.getDate() + 1)

  if (h >= 7 && h < 18) {
    // Dayshift in progress
    return {
      start: toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 7, 0)),
      end:   toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18, 0))
    }
  } else if (h >= 18) {
    // Nightshift in progress (evening)
    return {
      start: toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18, 0)),
      end:   toLocal(new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 7, 0))
    }
  } else {
    // Early morning (0–6): nightshift that started yesterday
    return {
      start: toLocal(new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 18, 0)),
      end:   toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 7, 0))
    }
  }
}

const defaults = smartDefaults()
const startDt  = ref(defaults.start)
const endDt    = ref(defaults.end)

// ── Preset appliers ────────────────────────────────────────────────────────────
function applyPreset(preset) {
  const now       = new Date()
  const today     = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1)
  const tomorrow  = new Date(today); tomorrow.setDate(today.getDate() + 1)

  if (preset === 'day') {
    startDt.value = toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 7, 0))
    endDt.value   = toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18, 0))
  } else if (preset === 'night') {
    startDt.value = toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18, 0))
    endDt.value   = toLocal(new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 7, 0))
  } else if (preset === 'lastNight') {
    startDt.value = toLocal(new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 18, 0))
    endDt.value   = toLocal(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 7, 0))
  }
}

// ── Validation ─────────────────────────────────────────────────────────────────
const validationError = computed(() => {
  if (!startDt.value || !endDt.value) return null
  if (new Date(endDt.value) <= new Date(startDt.value)) {
    return 'End time must be after start time.'
  }
  return null
})

// ── Interval label ─────────────────────────────────────────────────────────────
const intervalLabel = computed(() => {
  if (!startDt.value || !endDt.value) return ''
  const s = new Date(startDt.value)
  const e = new Date(endDt.value)
  const fmt = (d) => d.toLocaleString('en-GB', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: false
  })
  const diffMs  = e - s
  const diffH   = Math.floor(diffMs / 3600000)
  const diffMin = Math.floor((diffMs % 3600000) / 60000)
  const durStr  = diffMin ? `${diffH}h ${diffMin}m` : `${diffH}h`
  return `${fmt(s)} → ${fmt(e)}  (${durStr})`
})

// ── Generate ───────────────────────────────────────────────────────────────────
async function handleGenerate() {
  if (validationError.value) return
  await generate(startDt.value, endDt.value)
}
</script>

<style scoped>
.reports-view {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-lg);
}

.reports-view__header { flex-shrink: 0; }

.reports-view__title {
  font-size:   var(--font-size-xl);
  font-weight: 800;
  color:       var(--color-primary);
}

.reports-view__sub {
  font-size:  var(--font-size-sm);
  color:      var(--color-text-muted);
  margin-top: 2px;
}

/* ── Body layout ──────────────────────────────────────────── */
.reports-view__body {
  display:               grid;
  grid-template-columns: 1fr 1fr;
  gap:                   var(--space-lg);
  align-items:           start;
}

@media (max-width: 900px) {
  .reports-view__body { grid-template-columns: 1fr; }
}

/* ── Report card ──────────────────────────────────────────── */
.report-card__header {
  display:       flex;
  align-items:   flex-start;
  gap:           var(--space-md);
  padding:       var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  background:    var(--color-bg-section);
}

.report-card__header-icon {
  width:           44px;
  height:          44px;
  min-width:       44px;
  background:      var(--color-primary);
  border-radius:   var(--radius-md);
  display:         flex;
  align-items:     center;
  justify-content: center;
  color:           white;
}

.report-card__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
}

.report-card__sub {
  font-size:   var(--font-size-sm);
  color:       var(--color-text-muted);
  margin-top:  4px;
  line-height: 1.5;
}

.report-card__body {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap:     var(--space-md);
}

/* ── Presets ──────────────────────────────────────────────── */
.presets {
  display:     flex;
  align-items: center;
  gap:         var(--space-sm);
  flex-wrap:   wrap;
}

.presets__label {
  font-size:   var(--font-size-xs);
  font-weight: 600;
  color:       var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.preset-btn {
  padding:       4px 10px;
  border:        1px solid var(--color-border);
  border-radius: 20px;
  background:    var(--color-bg-section);
  color:         var(--color-text-secondary);
  font-size:     var(--font-size-xs);
  font-weight:   600;
  cursor:        pointer;
  transition:    var(--transition);
  font-family:   var(--font-family);
  white-space:   nowrap;
}

.preset-btn:hover {
  background:   var(--color-primary);
  border-color: var(--color-primary);
  color:        white;
}

/* ── Field ────────────────────────────────────────────────── */
.report-field {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-xs);
}

.report-field__label {
  font-size:   var(--font-size-sm);
  font-weight: 600;
  color:       var(--color-text-secondary);
}

.report-field__input {
  padding:       10px var(--space-md);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size:     var(--font-size-base);
  font-family:   var(--font-family);
  color:         var(--color-text-primary);
  background:    var(--color-bg-section);
  outline:       none;
  transition:    var(--transition);
}

.report-field__input:focus {
  border-color: var(--color-primary-light);
  background:   var(--color-bg-card);
  box-shadow:   0 0 0 3px rgba(37, 99, 235, 0.08);
}

/* ── Interval summary pill ────────────────────────────────── */
.interval-summary {
  display:       flex;
  align-items:   center;
  gap:           6px;
  padding:       8px 12px;
  background:    rgba(37, 99, 235, 0.06);
  border:        1px solid rgba(37, 99, 235, 0.15);
  border-radius: var(--radius-md);
  font-size:     var(--font-size-sm);
  font-weight:   500;
  color:         var(--color-primary);
}

/* ── Validation error ─────────────────────────────────────── */
.field-error {
  font-size:   var(--font-size-sm);
  color:       var(--color-danger, #dc2626);
  font-weight: 500;
}

/* ── Generate button ──────────────────────────────────────── */
.report-btn {
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             var(--space-sm);
  width:           100%;
  padding:         14px var(--space-lg);
  background:      var(--color-primary);
  color:           white;
  border:          none;
  border-radius:   var(--radius-md);
  font-size:       var(--font-size-md);
  font-weight:     700;
  cursor:          pointer;
  transition:      var(--transition);
  font-family:     var(--font-family);
  letter-spacing:  0.2px;
}

.report-btn:hover:not(:disabled) {
  background: var(--color-primary-light);
  transform:  translateY(-1px);
  box-shadow: var(--shadow-md);
}

.report-btn:active:not(:disabled) { transform: translateY(0); }

.report-btn:disabled {
  opacity: 0.55;
  cursor:  not-allowed;
}

.report-btn--loading { background: var(--color-primary-light); opacity: 0.85; }
.report-btn--success { background: var(--color-success); }

.report-btn__spinner {
  width:         18px;
  height:        18px;
  border:        2px solid rgba(255,255,255,0.35);
  border-top:    2px solid white;
  border-radius: 50%;
  animation:     spin 0.7s linear infinite;
  flex-shrink:   0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── API error ────────────────────────────────────────────── */
.report-error {
  display:       flex;
  align-items:   flex-start;
  gap:           var(--space-sm);
  padding:       var(--space-md);
  background:    rgba(220, 38, 38, 0.07);
  border:        1px solid rgba(220, 38, 38, 0.2);
  border-radius: var(--radius-md);
  font-size:     var(--font-size-sm);
  color:         var(--color-danger);
  line-height:   1.5;
}

/* ── Info card ────────────────────────────────────────────── */
.info-card__header {
  padding:       var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  background:    var(--color-bg-section);
}

.info-card__title {
  font-size:      var(--font-size-sm);
  font-weight:    700;
  color:          var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-card__body {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
}

.info-sheet {
  display:     flex;
  align-items: flex-start;
  gap:         var(--space-md);
  padding:     var(--space-md) 0;
}

.info-sheet__badge {
  padding:       4px 10px;
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-xs);
  font-weight:   700;
  white-space:   nowrap;
  flex-shrink:   0;
}

.info-sheet__badge--blue  { background: rgba(37,99,235,0.1);  color: #1d4ed8; }
.info-sheet__badge--amber { background: rgba(217,119,6,0.1);  color: #92400e; }
.info-sheet__badge--green { background: rgba(5,150,105,0.1);  color: #047857; }

.info-sheet__name {
  font-size:   var(--font-size-sm);
  font-weight: 600;
  color:       var(--color-text-primary);
}

.info-sheet__desc {
  font-size:   var(--font-size-sm);
  color:       var(--color-text-muted);
  margin-top:  4px;
  line-height: 1.5;
}

.info-divider {
  height:     1px;
  background: var(--color-border-light);
}

/* ── Transitions ──────────────────────────────────────────── */
.fade-msg-enter-active,
.fade-msg-leave-active { transition: opacity 0.25s ease; }
.fade-msg-enter-from,
.fade-msg-leave-to     { opacity: 0; }
</style>
