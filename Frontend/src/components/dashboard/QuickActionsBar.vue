<template>
  <div class="quick-actions">

    <h3 class="quick-actions__title">Quick Actions</h3>

    <button
      class="quick-actions__btn quick-actions__btn--undo"
      :disabled="isLoading"
      @click="handleUndo"
    >
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2.5">
        <path d="M3 7v6h6"/><path d="M21 17a9 9 0 00-9-9 9 9 0 00-6 2.3L3 13"/>
      </svg>
      {{ isLoading ? 'Undoing...' : 'Undo Last Event' }}
    </button>

    <button
      class="quick-actions__btn quick-actions__btn--refresh"
      :disabled="isRefreshing"
      @click="handleRefresh"
    >
      <svg
        width="15" height="15" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2.5"
        :class="{ 'spin': isRefreshing }"
      >
        <polyline points="23 4 23 10 17 10"/>
        <path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/>
      </svg>
      {{ isRefreshing ? 'Refreshing...' : 'Refresh Counts' }}
    </button>

    <!-- Undo confirmation message -->
    <Transition name="slide-up">
      <div v-if="undoMessage" class="quick-actions__feedback" :class="undoSuccess ? 'feedback--success' : 'feedback--error'">
        {{ undoMessage }}
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref }             from 'vue'
import { useEventLogger }  from '../../composables/useEventLogger.js'
import { useCountsStore }  from '../../stores/countsStore.js'

const { undo, isLoading } = useEventLogger()
const countsStore = useCountsStore()

const isRefreshing  = ref(false)
const undoMessage   = ref('')
const undoSuccess   = ref(true)
let   messageTimer  = null

async function handleUndo() {
  const result = await undo()

  if (messageTimer) clearTimeout(messageTimer)

  if (result.success) {
    const loc          = result.undone?.location || 'event'
    undoMessage.value  = `✓ Undone: ${loc}`
    undoSuccess.value  = true
  } else {
    undoMessage.value  = result.message || 'Nothing to undo'
    undoSuccess.value  = false
  }

  messageTimer = setTimeout(() => {
    undoMessage.value = ''
  }, 2500)
}

async function handleRefresh() {
  isRefreshing.value = true
  await countsStore.refreshCounts()
  setTimeout(() => { isRefreshing.value = false }, 600)
}
</script>

<style scoped>
.quick-actions {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
}

.quick-actions__title {
  font-size:      var(--font-size-xs);
  font-weight:    700;
  color:          var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.quick-actions__btn {
  display:         flex;
  align-items:     center;
  gap:             var(--space-sm);
  width:           100%;
  padding:         10px var(--space-md);
  border-radius:   var(--radius-md);
  font-size:       var(--font-size-sm);
  font-weight:     600;
  cursor:          pointer;
  transition:      var(--transition);
  font-family:     var(--font-family);
  border:          1px solid transparent;
}

.quick-actions__btn:disabled {
  opacity: 0.6;
  cursor:  not-allowed;
}

.quick-actions__btn--undo {
  background: transparent;
  color:      var(--color-text-secondary);
  border-color: var(--color-border);
}

.quick-actions__btn--undo:hover:not(:disabled) {
  background:   var(--color-bg-section);
  border-color: var(--color-border-dark, #cbd5e0);
  color:        var(--color-text-primary);
}

.quick-actions__btn--refresh {
  background: transparent;
  color:      var(--color-text-secondary);
  border-color: var(--color-border);
}

.quick-actions__btn--refresh:hover:not(:disabled) {
  background:   var(--color-bg-section);
  border-color: var(--color-border-dark, #cbd5e0);
  color:        var(--color-text-primary);
}

/* ── Spin animation for refresh icon ─────────────────────── */
.spin {
  animation: spin-icon 0.7s linear infinite;
}

@keyframes spin-icon {
  to { transform: rotate(360deg); }
}

/* ── Feedback message ─────────────────────────────────────── */
.quick-actions__feedback {
  padding:       var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-sm);
  font-weight:   500;
}

.feedback--success {
  background: rgba(5, 150, 105, 0.08);
  color:      var(--color-success);
  border:     1px solid rgba(5, 150, 105, 0.2);
}

.feedback--error {
  background: rgba(220, 38, 38, 0.08);
  color:      var(--color-danger);
  border:     1px solid rgba(220, 38, 38, 0.2);
}

/* ── Slide up transition ──────────────────────────────────── */
.slide-up-enter-active,
.slide-up-leave-active  { transition: all 0.2s ease; }
.slide-up-enter-from    { opacity: 0; transform: translateY(6px); }
.slide-up-leave-to      { opacity: 0; transform: translateY(-4px); }
</style>