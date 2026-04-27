<template>
  <AppShell>
    <div class="status-view">

      <div class="status-view__header">
        <h1 class="status-view__title">✈️ Terminals</h1>
        <p class="status-view__sub">Toggle a terminal offline to pause data logging and mark it as unavailable</p>
      </div>

      <div class="status-list">
        <div
          v-for="t in TERMINALS"
          :key="t.name"
          class="status-item card"
          :class="{ 'status-item--offline': !statusStore.isOnline(t.name) }"
        >
          <div class="status-item__left">
            <div class="status-item__icon-wrap" :class="statusStore.isOnline(t.name) ? 'icon-wrap--online' : 'icon-wrap--offline'">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 .9h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
              </svg>
            </div>
            <div class="status-item__info">
              <div class="status-item__name">{{ t.name }}</div>
              <span class="status-badge" :class="statusStore.isOnline(t.name) ? 'badge--online' : 'badge--offline'">
                {{ statusStore.isOnline(t.name) ? 'Online' : 'Offline Mode' }}
              </span>
            </div>
          </div>

          <button
            class="toggle"
            :class="{ 'toggle--on': statusStore.isOnline(t.name) }"
            :aria-label="`Toggle ${t.name}`"
            @click="statusStore.toggle(t.name)"
          >
            <span class="toggle__knob" />
          </button>
        </div>
      </div>

    </div>
  </AppShell>
</template>

<script setup>
import AppShell        from '../components/layout/AppShell.vue'
import { TERMINALS }   from '../constants/terminals.js'
import { useStatusStore } from '../stores/statusStore.js'

const statusStore = useStatusStore()
</script>

<style scoped>
.status-view {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-lg);
  max-width:      640px;
}

.status-view__title {
  font-size:   var(--font-size-xl);
  font-weight: 800;
  color:       var(--color-primary);
}

.status-view__sub {
  font-size:  var(--font-size-sm);
  color:      var(--color-text-muted);
  margin-top: 3px;
}

/* ── List ─────────────────────────────────────────────────── */
.status-list {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
}

.status-item {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding:         var(--space-md) var(--space-lg);
  transition:      background 0.2s ease, opacity 0.2s ease;
}

.status-item--offline {
  opacity: 0.75;
  background: var(--color-bg-section) !important;
}

.status-item__left {
  display:     flex;
  align-items: center;
  gap:         var(--space-md);
}

/* ── Icon circle ──────────────────────────────────────────── */
.status-item__icon-wrap {
  width:           40px;
  height:          40px;
  border-radius:   50%;
  display:         flex;
  align-items:     center;
  justify-content: center;
  flex-shrink:     0;
  transition:      background 0.2s ease, color 0.2s ease;
}

.icon-wrap--online {
  background: rgba(37, 99, 235, 0.12);
  color:      var(--color-primary);
}

.icon-wrap--offline {
  background: rgba(100, 116, 139, 0.12);
  color:      var(--color-text-muted);
}

/* ── Info ─────────────────────────────────────────────────── */
.status-item__info {
  display:        flex;
  flex-direction: column;
  gap:            4px;
}

.status-item__name {
  font-size:      var(--font-size-sm);
  font-weight:    700;
  color:          var(--color-text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ── Badges ───────────────────────────────────────────────── */
.status-badge {
  display:       inline-block;
  font-size:     10px;
  font-weight:   700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding:       2px 8px;
  border-radius: 20px;
}

.badge--online {
  background: rgba(5, 150, 105, 0.12);
  color:      var(--color-success, #059669);
  border:     1px solid rgba(5, 150, 105, 0.25);
}

.badge--offline {
  background: rgba(220, 38, 38, 0.1);
  color:      var(--color-danger, #dc2626);
  border:     1px solid rgba(220, 38, 38, 0.2);
}

/* ── Toggle switch ────────────────────────────────────────── */
.toggle {
  width:         48px;
  height:        26px;
  border-radius: 13px;
  background:    #cbd5e1;
  border:        none;
  cursor:        pointer;
  position:      relative;
  transition:    background 0.25s ease;
  flex-shrink:   0;
  padding:       0;
}

.toggle--on {
  background: var(--color-primary);
}

.toggle__knob {
  position:      absolute;
  top:           3px;
  left:          3px;
  width:         20px;
  height:        20px;
  background:    white;
  border-radius: 50%;
  transition:    transform 0.25s ease;
  box-shadow:    0 1px 4px rgba(0,0,0,0.2);
}

.toggle--on .toggle__knob {
  transform: translateX(22px);
}
</style>
