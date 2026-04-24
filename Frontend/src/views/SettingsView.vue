<template>
  <AppShell>
    <div class="settings-view">

      <div class="settings-view__header">
        <h1 class="settings-view__title">Settings</h1>
        <p class="settings-view__sub">Configure your shift details</p>
      </div>

      <div class="settings-card card">

        <div class="settings-card__header">
          <h2 class="settings-card__title">Shift Configuration</h2>
        </div>

        <div class="settings-card__body">

          <!-- Operator name -->
          <div class="field">
            <label class="field__label">Operator Name</label>
            <input
              v-model="operatorName"
              type="text"
              class="field__input"
              placeholder="Enter your name"
              @input="sessionStore.setOperatorName(operatorName)"
            />
            <p class="field__hint">
              Appears in the topbar and on generated reports
            </p>
          </div>

          <!-- Shift date -->
          <div class="field">
            <label class="field__label">Shift Date</label>
            <input
              v-model="shiftDate"
              type="date"
              class="field__input"
              @change="sessionStore.setShiftDate(shiftDate)"
            />
            <p class="field__hint">
              Used to filter events and generate the correct report
            </p>
          </div>

        </div>

        <!-- Saved confirmation -->
        <Transition name="fade-msg">
          <div v-if="saved" class="settings-card__saved">
            ✓ Settings saved automatically
          </div>
        </Transition>

      </div>

    </div>
  </AppShell>
</template>

<script setup>
import { ref, watch }       from 'vue'
import { useSessionStore }  from '../stores/sessionStore.js'
import AppShell             from '../components/layout/AppShell.vue'

const sessionStore = useSessionStore()
const operatorName = ref(sessionStore.operatorName)
const shiftDate    = ref(sessionStore.shiftDate)
const saved        = ref(false)
let   saveTimer    = null

// Show "saved" confirmation whenever anything changes
watch([operatorName, shiftDate], () => {
  if (saveTimer) clearTimeout(saveTimer)
  saved.value = true
  saveTimer = setTimeout(() => { saved.value = false }, 2000)
})
</script>

<style scoped>
.settings-view {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-lg);
  max-width:      600px;
}

.settings-view__header {}

.settings-view__title {
  font-size:   var(--font-size-xl);
  font-weight: 800;
  color:       var(--color-primary);
}

.settings-view__sub {
  font-size:  var(--font-size-sm);
  color:      var(--color-text-muted);
  margin-top: 2px;
}

/* ── Card ─────────────────────────────────────────────────── */
.settings-card {
  overflow: hidden;
}

.settings-card__header {
  padding:       var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  background:    var(--color-bg-section);
}

.settings-card__title {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
}

.settings-card__body {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap:     var(--space-lg);
}

.settings-card__saved {
  padding:     var(--space-sm) var(--space-lg);
  background:  rgba(5, 150, 105, 0.07);
  border-top:  1px solid rgba(5, 150, 105, 0.15);
  font-size:   var(--font-size-sm);
  font-weight: 600;
  color:       var(--color-success);
}

/* ── Field ────────────────────────────────────────────────── */
.field {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-xs);
}

.field__label {
  font-size:      var(--font-size-sm);
  font-weight:    600;
  color:          var(--color-text-secondary);
  letter-spacing: 0.2px;
}

.field__input {
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

.field__input:focus {
  border-color: var(--color-primary-light);
  background:   white;
  box-shadow:   0 0 0 3px rgba(37, 99, 235, 0.08);
}

.field__hint {
  font-size: var(--font-size-xs);
  color:     var(--color-text-muted);
}

/* ── Saved message transition ─────────────────────────────── */
.fade-msg-enter-active,
.fade-msg-leave-active { transition: opacity 0.3s ease; }
.fade-msg-enter-from,
.fade-msg-leave-to     { opacity: 0; }
</style>