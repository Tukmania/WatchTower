<template>
  <div class="app-shell">
    <SidebarNav />
    <div class="app-shell__body">
      <TopBar />
      <div class="app-shell__content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import SidebarNav from './SidebarNav.vue'
import TopBar     from './TopBar.vue'
</script>

<style scoped>
.app-shell {
  display:    flex;
  width:      100vw;
  height:     100vh;
  overflow:   hidden;
  background: var(--color-bg-page);
}

.app-shell__body {
  display:        flex;
  flex-direction: column;
  flex:           1;
  overflow:       hidden;
  min-width:      0;
}

.app-shell__content {
  flex:       1;
  overflow:   hidden;
  padding:    var(--space-md);
  display:    flex;
  min-height: 0;
}
</style>