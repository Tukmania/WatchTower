<template>
  <AppShell>
    <div class="incident-view">

      <!-- Header -->
      <div class="incident-view__header">
        <div>
          <h1 class="incident-view__title">Incident Log</h1>
          <p class="incident-view__sub">Record CCTV incidents observed during the shift</p>
        </div>
      </div>

      <div class="incident-view__body">

        <!-- ── Log form card ─────────────────────────────────────── -->
        <div class="form-card card">

          <div class="form-card__header">
            <div class="form-card__header-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                   stroke="currentColor" stroke-width="2" stroke-linecap="round"
                   stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <div>
              <h2 class="form-card__title">Log New Incident</h2>
              <p class="form-card__sub">Fill in all fields and click Save to record the incident</p>
            </div>
          </div>

          <div class="form-card__body">

            <!-- Row 1: Shift + Date + Time -->
            <div class="field-row">

              <div class="field field--sm">
                <label class="field__label">Shift</label>
                <select v-model="form.shift" class="field__input field__select">
                  <option value="DAYSHIFT">DAYSHIFT</option>
                  <option value="NIGHTSHIFT">NIGHTSHIFT</option>
                </select>
              </div>

              <div class="field field--sm">
                <label class="field__label">Date</label>
                <input
                  v-model="form.date"
                  type="date"
                  class="field__input"
                />
              </div>

              <div class="field field--md">
                <label class="field__label">Time</label>
                <input
                  v-model="form.time"
                  type="text"
                  class="field__input"
                  placeholder="e.g. 1620HRS or 0700HRS – 0830HRS"
                />
              </div>

            </div>

            <!-- Row 2: Terminal -->
            <div class="field">
              <label class="field__label">Terminal / Location</label>
              <input
                v-model="form.terminal"
                type="text"
                class="field__input"
                placeholder="e.g. TERMINAL 1A, MARINA, LAOMAI JKIA"
                list="terminal-suggestions"
              />
              <datalist id="terminal-suggestions">
                <option value="TERMINAL 1A"/>
                <option value="TERMINAL 1B"/>
                <option value="TERMINAL 1C"/>
                <option value="TERMINAL 1D"/>
                <option value="MARINA"/>
                <option value="LAOMAI JKIA"/>
                <option value="LAOMAI MOMBASA"/>
                <option value="CRAYSON PHARMACY JKIA"/>
                <option value="CRAYSON PHARMACY KIAMBU ROAD"/>
                <option value="CRAYSON PHARMACY MOMBASA"/>
                <option value="SKYLINE GYM"/>
                <option value="All Terminals"/>
                <option value="All Locations"/>
              </datalist>
            </div>

            <!-- Row 3: Description -->
            <div class="field">
              <label class="field__label">Type of Incident</label>
              <textarea
                v-model="form.description"
                class="field__textarea"
                rows="4"
                placeholder="Describe the incident as observed through CCTV…"
              />
            </div>

            <!-- Validation error -->
            <div v-if="formError" class="form-error">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                   stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ formError }}
            </div>

            <!-- Save button -->
            <button
              class="save-btn"
              :class="{ 'save-btn--loading': isSaving, 'save-btn--success': saveSuccess }"
              :disabled="isSaving"
              @click="handleSave"
            >
              <template v-if="isSaving">
                <span class="save-btn__spinner" />
                Saving…
              </template>
              <template v-else-if="saveSuccess">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Incident Saved
              </template>
              <template v-else>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2.5">
                  <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                  <polyline points="17 21 17 13 7 13 7 21"/>
                  <polyline points="7 3 7 8 15 8"/>
                </svg>
                Save Incident
              </template>
            </button>

          </div>
        </div>

        <!-- ── Logged incidents table ─────────────────────────────── -->
        <div class="log-card card">

          <div class="log-card__header">
            <h3 class="log-card__title">
              Recorded Incidents
              <span v-if="incidents.length" class="log-card__count">{{ incidents.length }}</span>
            </h3>
            <button class="refresh-btn" @click="loadIncidents">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                   stroke="currentColor" stroke-width="2.5">
                <polyline points="23 4 23 10 17 10"/>
                <path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/>
              </svg>
              Refresh
            </button>
          </div>

          <!-- Empty state -->
          <div v-if="!incidents.length && !isLoading" class="log-empty">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="1.5" opacity="0.3">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <p>No incidents logged for this shift</p>
          </div>

          <!-- Loading -->
          <div v-else-if="isLoading" class="log-loading">
            <span class="log-loading__spinner" />
          </div>

          <!-- Table -->
          <div v-else class="log-table-wrap">
            <table class="log-table">
              <thead>
                <tr>
                  <th>SHIFT</th>
                  <th>DATE</th>
                  <th>TIME</th>
                  <th>TERMINAL</th>
                  <th>TYPE OF INCIDENT</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="inc in incidents" :key="inc.id">
                  <td>
                    <span class="shift-badge"
                          :class="inc.shift === 'DAYSHIFT' ? 'shift-badge--day' : 'shift-badge--night'">
                      {{ inc.shift }}
                    </span>
                  </td>
                  <td class="td--date">{{ inc.date }}</td>
                  <td class="td--time">{{ inc.time }}</td>
                  <td class="td--terminal">{{ inc.terminal }}</td>
                  <td class="td--desc">{{ inc.description }}</td>
                  <td class="td--action">
                    <button class="delete-btn" title="Delete incident"
                            @click="handleDelete(inc.id)">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                           stroke="currentColor" stroke-width="2.5">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>
                        <path d="M10 11v6M14 11v6"/>
                        <path d="M9 6V4h6v2"/>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>

      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, onMounted }       from 'vue'
import AppShell                 from '../components/layout/AppShell.vue'
import { logIncident, fetchIncidents, deleteIncident } from '../api/incidents.js'

// ── Form state ─────────────────────────────────────────────────────────────────
function detectShift() {
  const h = new Date().getHours()
  return (h >= 7 && h < 18) ? 'DAYSHIFT' : 'NIGHTSHIFT'
}

function todayIso() {
  return new Date().toISOString().split('T')[0]
}

const form = ref({
  shift:       detectShift(),
  date:        todayIso(),
  time:        '',
  terminal:    '',
  description: ''
})

const formError   = ref('')
const isSaving    = ref(false)
const saveSuccess = ref(false)
let   successTimer = null

// ── Incidents list ─────────────────────────────────────────────────────────────
const incidents = ref([])
const isLoading = ref(false)

async function loadIncidents() {
  isLoading.value = true
  try {
    const res = await fetchIncidents()
    incidents.value = res.data
  } catch (e) {
    console.error('Failed to load incidents:', e)
  } finally {
    isLoading.value = false
  }
}

// ── Save ───────────────────────────────────────────────────────────────────────
function validate() {
  const f = form.value
  if (!f.shift)       return 'Shift is required.'
  if (!f.date)        return 'Date is required.'
  if (!f.time.trim()) return 'Time is required.'
  if (!f.terminal.trim()) return 'Terminal / Location is required.'
  if (!f.description.trim()) return 'Incident description is required.'
  return ''
}

async function handleSave() {
  formError.value = validate()
  if (formError.value) return

  isSaving.value = true
  try {
    const res = await logIncident({ ...form.value })
    incidents.value.push(res.data)

    // Reset description and time but keep shift/date for quick re-entry
    form.value.time        = ''
    form.value.description = ''
    formError.value        = ''

    saveSuccess.value = true
    if (successTimer) clearTimeout(successTimer)
    successTimer = setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (e) {
    formError.value = 'Failed to save incident. Please try again.'
    console.error(e)
  } finally {
    isSaving.value = false
  }
}

// ── Delete ─────────────────────────────────────────────────────────────────────
async function handleDelete(id) {
  try {
    await deleteIncident(id)
    incidents.value = incidents.value.filter(i => i.id !== id)
  } catch (e) {
    console.error('Failed to delete incident:', e)
  }
}

onMounted(loadIncidents)
</script>

<style scoped>
.incident-view {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-lg);
  height:         100%;
  min-height:     0;
  overflow-y:     auto;
}

.incident-view__header { flex-shrink: 0; }

.incident-view__title {
  font-size:   var(--font-size-xl);
  font-weight: 800;
  color:       var(--color-primary);
}

.incident-view__sub {
  font-size:  var(--font-size-sm);
  color:      var(--color-text-muted);
  margin-top: 2px;
}

/* ── Body grid ────────────────────────────────────────────── */
.incident-view__body {
  display:               grid;
  grid-template-columns: 1fr 1fr;
  gap:                   var(--space-lg);
  align-items:           start;
  flex-shrink:           0;
}

@media (max-width: 960px) {
  .incident-view__body { grid-template-columns: 1fr; }
}

/* ── Form card ────────────────────────────────────────────── */
.form-card__header {
  display:       flex;
  align-items:   flex-start;
  gap:           var(--space-md);
  padding:       var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  background:    var(--color-bg-section);
}

.form-card__header-icon {
  width:           44px;
  height:          44px;
  min-width:       44px;
  background:      #7C3AED;
  border-radius:   var(--radius-md);
  display:         flex;
  align-items:     center;
  justify-content: center;
  color:           white;
  flex-shrink:     0;
}

.form-card__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
}

.form-card__sub {
  font-size:   var(--font-size-sm);
  color:       var(--color-text-muted);
  margin-top:  4px;
  line-height: 1.5;
}

.form-card__body {
  padding:        var(--space-lg);
  display:        flex;
  flex-direction: column;
  gap:            var(--space-md);
}

/* ── Field row ────────────────────────────────────────────── */
.field-row {
  display: flex;
  gap:     var(--space-md);
}

.field      { display: flex; flex-direction: column; gap: var(--space-xs); flex: 1; }
.field--sm  { flex: 0 0 auto; min-width: 110px; }
.field--md  { flex: 1; }

.field__label {
  font-size:      var(--font-size-sm);
  font-weight:    600;
  color:          var(--color-text-secondary);
  letter-spacing: 0.2px;
}

.field__input,
.field__select,
.field__textarea {
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

.field__input:focus,
.field__select:focus,
.field__textarea:focus {
  border-color: #7C3AED;
  background:   var(--color-bg-card);
  box-shadow:   0 0 0 3px rgba(124, 58, 237, 0.1);
}

.field__select { cursor: pointer; }

.field__textarea {
  resize:      vertical;
  line-height: 1.55;
  min-height:  90px;
}

/* ── Validation error ─────────────────────────────────────── */
.form-error {
  display:     flex;
  align-items: center;
  gap:         var(--space-xs);
  font-size:   var(--font-size-sm);
  color:       var(--color-danger);
  font-weight: 500;
}

/* ── Save button ──────────────────────────────────────────── */
.save-btn {
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             var(--space-sm);
  width:           100%;
  padding:         13px var(--space-lg);
  background:      #7C3AED;
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

.save-btn:hover:not(:disabled) {
  background: #6d28d9;
  transform:  translateY(-1px);
  box-shadow: var(--shadow-md);
}

.save-btn:active:not(:disabled) { transform: translateY(0); }
.save-btn:disabled              { opacity: 0.55; cursor: not-allowed; }
.save-btn--loading              { background: #6d28d9; opacity: 0.85; }
.save-btn--success              { background: var(--color-success); }

.save-btn__spinner {
  width:         16px;
  height:        16px;
  border:        2px solid rgba(255,255,255,0.35);
  border-top:    2px solid white;
  border-radius: 50%;
  animation:     spin 0.7s linear infinite;
  flex-shrink:   0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Log card ─────────────────────────────────────────────── */
.log-card__header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding:         var(--space-md) var(--space-lg);
  border-bottom:   1px solid var(--color-border);
  background:      var(--color-bg-section);
}

.log-card__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
  display:     flex;
  align-items: center;
  gap:         var(--space-sm);
}

.log-card__count {
  display:         inline-flex;
  align-items:     center;
  justify-content: center;
  min-width:       22px;
  height:          22px;
  padding:         0 6px;
  background:      #7C3AED;
  color:           white;
  border-radius:   999px;
  font-size:       var(--font-size-xs);
  font-weight:     700;
}

.refresh-btn {
  display:       flex;
  align-items:   center;
  gap:           var(--space-xs);
  padding:       6px var(--space-sm);
  background:    var(--color-bg-card);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size:     var(--font-size-xs);
  font-weight:   600;
  color:         var(--color-text-secondary);
  cursor:        pointer;
  transition:    var(--transition);
  font-family:   var(--font-family);
}

.refresh-btn:hover {
  background: var(--color-bg-hover);
  color:      var(--color-text-primary);
}

/* ── Empty / loading states ───────────────────────────────── */
.log-empty {
  display:        flex;
  flex-direction: column;
  align-items:    center;
  justify-content: center;
  gap:            var(--space-sm);
  padding:        var(--space-2xl) var(--space-lg);
  color:          var(--color-text-muted);
  font-size:      var(--font-size-sm);
}

.log-loading {
  display:         flex;
  justify-content: center;
  padding:         var(--space-2xl);
}

.log-loading__spinner {
  display:       block;
  width:         24px;
  height:        24px;
  border:        2px solid var(--color-border);
  border-top:    2px solid #7C3AED;
  border-radius: 50%;
  animation:     spin 0.7s linear infinite;
}

/* ── Table ────────────────────────────────────────────────── */
.log-table-wrap {
  overflow-x: auto;
}

.log-table {
  width:           100%;
  border-collapse: collapse;
  font-size:       var(--font-size-sm);
}

.log-table thead tr {
  background: var(--color-bg-section);
}

.log-table th {
  padding:        8px var(--space-md);
  text-align:     left;
  font-size:      var(--font-size-xs);
  font-weight:    700;
  color:          var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom:  1px solid var(--color-border);
  white-space:    nowrap;
}

.log-table tbody tr {
  border-bottom: 1px solid var(--color-border-light);
  transition:    background var(--transition-fast);
}

.log-table tbody tr:hover {
  background: var(--color-bg-hover);
}

.log-table td {
  padding:     10px var(--space-md);
  color:       var(--color-text-primary);
  vertical-align: top;
}

.td--date     { white-space: nowrap; color: var(--color-text-secondary); }
.td--time     { white-space: nowrap; color: var(--color-text-secondary); font-family: 'Courier New', monospace; font-size: var(--font-size-xs); }
.td--terminal { white-space: nowrap; font-weight: 600; }
.td--desc     { max-width: 320px; line-height: 1.55; }
.td--action   { width: 40px; text-align: center; }

/* ── Shift badge ──────────────────────────────────────────── */
.shift-badge {
  display:       inline-block;
  padding:       2px 8px;
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-xs);
  font-weight:   700;
  white-space:   nowrap;
  letter-spacing: 0.3px;
}

.shift-badge--day {
  background: rgba(37, 99, 235, 0.1);
  color:      #1d4ed8;
}

.shift-badge--night {
  background: rgba(124, 58, 237, 0.1);
  color:      #6d28d9;
}

/* ── Delete button ────────────────────────────────────────── */
.delete-btn {
  display:         flex;
  align-items:     center;
  justify-content: center;
  width:           28px;
  height:          28px;
  border:          1px solid var(--color-border);
  border-radius:   var(--radius-sm);
  background:      var(--color-bg-section);
  color:           var(--color-text-muted);
  cursor:          pointer;
  transition:      var(--transition);
}

.delete-btn:hover {
  background:   rgba(220, 38, 38, 0.08);
  border-color: rgba(220, 38, 38, 0.3);
  color:        var(--color-danger);
}
</style>
