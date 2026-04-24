<template>
  <header class="topbar">

    <!-- Left — title + live badge -->
    <div class="topbar__left">
      <div class="topbar__brand">
        <span class="topbar__brand-title">WatchTower</span>
        <span class="topbar__brand-sub">CCTV Monitoring & Event Tally System</span>
      </div>
      <div class="topbar__live">
        <span class="topbar__live-dot" />
        <span class="topbar__live-label">Live Monitoring</span>
      </div>
    </div>

    <!-- Right — clock + operator -->
    <div class="topbar__right">
      <LiveClock />

      <div class="topbar__divider" />

      <div class="topbar__operator">
        <div class="topbar__operator-avatar">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <div class="topbar__operator-info">
          <span class="topbar__operator-name">{{ sessionStore.operatorName }}</span>
          <span class="topbar__operator-role">Operator</span>
        </div>
      </div>
    </div>

  </header>
</template>

<script setup>
import { useSessionStore } from '../../stores/sessionStore.js'
import LiveClock           from '../shared/LiveClock.vue'

const sessionStore = useSessionStore()
</script>

<style scoped>
.topbar {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  height:          58px;
  min-height:      58px;
  background:      var(--color-topbar-bg);
  padding:         0 var(--space-lg);
  border-bottom:   1px solid rgba(255,255,255,0.07);
  flex-shrink:     0;
  z-index:         50;
}

/* ── Left ─────────────────────────────────────────────────── */
.topbar__left {
  display:     flex;
  align-items: center;
  gap:         var(--space-lg);
}

.topbar__brand {
  display:        flex;
  flex-direction: column;
  gap:            1px;
}

.topbar__brand-title {
  font-size:      var(--font-size-md);
  font-weight:    800;
  color:          white;
  letter-spacing: 0.3px;
}

.topbar__brand-sub {
  font-size: var(--font-size-xs);
  color:     rgba(255,255,255,0.45);
  letter-spacing: 0.2px;
}

/* ── Live badge ───────────────────────────────────────────── */
.topbar__live {
  display:       flex;
  align-items:   center;
  gap:           var(--space-xs);
  background:    rgba(34, 197, 94, 0.12);
  border:        1px solid rgba(34, 197, 94, 0.3);
  padding:       4px 12px;
  border-radius: 999px;
}

.topbar__live-dot {
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

.topbar__live-label {
  font-size:   var(--font-size-xs);
  font-weight: 600;
  color:       var(--color-live);
  letter-spacing: 0.3px;
}

/* ── Right ────────────────────────────────────────────────── */
.topbar__right {
  display:     flex;
  align-items: center;
  gap:         var(--space-lg);
}

.topbar__divider {
  width:      1px;
  height:     28px;
  background: rgba(255,255,255,0.12);
}

/* ── Operator ─────────────────────────────────────────────── */
.topbar__operator {
  display:     flex;
  align-items: center;
  gap:         var(--space-sm);
}

.topbar__operator-avatar {
  width:           32px;
  height:          32px;
  background:      rgba(255,255,255,0.1);
  border-radius:   50%;
  display:         flex;
  align-items:     center;
  justify-content: center;
  color:           rgba(255,255,255,0.7);
  flex-shrink:     0;
}

.topbar__operator-info {
  display:        flex;
  flex-direction: column;
  gap:            1px;
}

.topbar__operator-name {
  font-size:   var(--font-size-sm);
  font-weight: 600;
  color:       white;
}

.topbar__operator-role {
  font-size: var(--font-size-xs);
  color:     rgba(255,255,255,0.45);
}
</style>