<template>
  <aside class="sidebar">

    <!-- Logo -->
    <div class="sidebar__logo">
      <div class="sidebar__logo-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="3"   stroke="white" stroke-width="2"/>
          <circle cx="12" cy="12" r="8"   stroke="white" stroke-width="1.5" stroke-dasharray="3 2"/>
          <circle cx="12" cy="12" r="11.5" stroke="white" stroke-width="1" opacity="0.4"/>
        </svg>
      </div>
    </div>

    <!-- Nav links -->
    <nav class="sidebar__nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.route"
        :to="item.route"
        class="sidebar__item"
        :class="{ 'sidebar__item--active': isActive(item.route) }"
        :title="item.label"
      >
        <span class="sidebar__item-icon" v-html="item.icon" />
        <span class="sidebar__item-label">{{ item.label }}</span>
      </RouterLink>
    </nav>

    <!-- Bottom -->
    <div class="sidebar__bottom">
      <RouterLink
        to="/settings"
        class="sidebar__item"
        :class="{ 'sidebar__item--active': isActive('/settings') }"
        title="Settings"
      >
        <span class="sidebar__item-icon" v-html="icons.settings" />
        <span class="sidebar__item-label">Settings</span>
      </RouterLink>
    </div>

  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

function isActive(path) {
  return route.path === path
}

const icons = {
  dashboard: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
    <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
  </svg>`,
  terminals: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 .9h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>
  </svg>`,
  shops: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
    <path d="M16 10a4 4 0 01-8 0"/>
  </svg>`,
  eventlog: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
    <polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
  </svg>`,
  incidents: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>`,
  reports: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
    <line x1="6"  y1="20" x2="6"  y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>
  </svg>`,
  settings: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="3"/>
    <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
  </svg>`
}

const navItems = [
  { route: '/dashboard', label: 'Dashboard', icon: icons.dashboard },
  { route: '/terminals', label: 'Terminals',  icon: icons.terminals },
  { route: '/shops',     label: 'Shops',      icon: icons.shops },
  { route: '/events',    label: 'Event Log',  icon: icons.eventlog },
  { route: '/incidents', label: 'Incidents',  icon: icons.incidents },
  { route: '/reports',   label: 'Reports',    icon: icons.reports }
]
</script>

<style scoped>
.sidebar {
  width:           var(--color-sidebar-width, 68px);
  min-width:       68px;
  height:          100vh;
  background:      var(--color-sidebar-bg);
  display:         flex;
  flex-direction:  column;
  align-items:     center;
  padding:         var(--space-sm) 0;
  z-index:         100;
  border-right:    1px solid rgba(255,255,255,0.05);
}

/* ── Logo ─────────────────────────────────────────────────── */
.sidebar__logo {
  padding:       var(--space-md) 0;
  margin-bottom: var(--space-sm);
  width:         100%;
  display:       flex;
  justify-content: center;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}

.sidebar__logo-icon {
  width:           38px;
  height:          38px;
  background:      var(--color-primary-light);
  border-radius:   var(--radius-md);
  display:         flex;
  align-items:     center;
  justify-content: center;
}

/* ── Nav ──────────────────────────────────────────────────── */
.sidebar__nav {
  display:        flex;
  flex-direction: column;
  align-items:    center;
  gap:            var(--space-xs);
  flex:           1;
  width:          100%;
  padding:        var(--space-sm) 0;
}

.sidebar__item {
  display:         flex;
  flex-direction:  column;
  align-items:     center;
  justify-content: center;
  gap:             4px;
  width:           52px;
  height:          52px;
  border-radius:   var(--radius-md);
  color:           var(--color-sidebar-icon);
  text-decoration: none;
  transition:      var(--transition);
  position:        relative;
  cursor:          pointer;
}

.sidebar__item:hover {
  background: rgba(255,255,255,0.07);
  color:      rgba(255,255,255,0.85);
}

.sidebar__item--active {
  background: var(--color-sidebar-active);
  color:      white;
}

.sidebar__item--active::before {
  content:       '';
  position:      absolute;
  left:          -1px;
  top:           50%;
  transform:     translateY(-50%);
  width:         3px;
  height:        24px;
  background:    white;
  border-radius: 0 3px 3px 0;
}

.sidebar__item-icon {
  display:         flex;
  align-items:     center;
  justify-content: center;
  flex-shrink:     0;
}

.sidebar__item-label {
  font-size:   8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  line-height: 1;
}

/* ── Bottom ───────────────────────────────────────────────── */
.sidebar__bottom {
  width:   100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-sm) 0;
  border-top: 1px solid rgba(255,255,255,0.07);
}
</style>