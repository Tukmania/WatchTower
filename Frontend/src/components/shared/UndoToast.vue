<template>
  <Teleport to="body">
    <Transition name="undo-toast">
      <div
        v-if="visible"
        class="undo-toast"
        :class="isSuccess ? 'undo-toast--success' : 'undo-toast--error'"
      >

        <!-- Icon -->
        <div class="undo-toast__icon">
          <svg
            v-if="isSuccess"
            width="18" height="18" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2.5"
          >
            <path d="M3 7v6h6"/>
            <path d="M21 17a9 9 0 00-9-9 9 9 0 00-6 2.3L3 13"/>
          </svg>
          <svg
            v-else
            width="18" height="18" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2.5"
          >
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>

        <!-- Message -->
        <div class="undo-toast__content">
          <p class="undo-toast__title">
            {{ isSuccess ? 'Event Undone' : 'Undo Failed' }}
          </p>
          <p class="undo-toast__detail">{{ detail }}</p>
        </div>

        <!-- Progress bar -->
        <div class="undo-toast__progress" />

      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useEventStore }        from '../../stores/eventStore.js'

const props = defineProps({
  message: { type: String,  default: '' },
  success: { type: Boolean, default: true },
  trigger: { type: Number,  default: 0 }
})

const visible   = ref(false)
const isSuccess = ref(true)
const detail    = ref('')
let   timer     = null

// Parent component bumps `trigger` to show the toast
watch(() => props.trigger, () => {
  if (!props.message) return

  isSuccess.value = props.success
  detail.value    = props.message

  if (timer) clearTimeout(timer)
  visible.value = true

  timer = setTimeout(() => {
    visible.value = false
  }, 2500)
})
</script>

<style scoped>
.undo-toast {
  position:       fixed;
  bottom:         var(--space-xl);
  left:           50%;
  transform:      translateX(-50%);
  z-index:        9998;
  display:        flex;
  align-items:    center;
  gap:            var(--space-md);
  padding:        var(--space-md) var(--space-lg);
  border-radius:  var(--radius-lg);
  box-shadow:     var(--shadow-lg);
  min-width:      300px;
  max-width:      420px;
  pointer-events: none;
  overflow:       hidden;
  position:       fixed;
}

/* ── Variants ─────────────────────────────────────────────── */
.undo-toast--success {
  background:  #0f1d3d;
  border-left: 4px solid var(--color-success);
}

.undo-toast--error {
  background:  #0f1d3d;
  border-left: 4px solid var(--color-danger);
}

/* ── Icon ─────────────────────────────────────────────────── */
.undo-toast__icon {
  flex-shrink: 0;
  display:     flex;
  align-items: center;
}

.undo-toast--success .undo-toast__icon { color: var(--color-success); }
.undo-toast--error   .undo-toast__icon { color: var(--color-danger);  }

/* ── Content ──────────────────────────────────────────────── */
.undo-toast__content {
  flex: 1;
}

.undo-toast__title {
  font-size:   var(--font-size-sm);
  font-weight: 700;
  color:       white;
}

.undo-toast__detail {
  font-size:  var(--font-size-xs);
  color:      rgba(255,255,255,0.55);
  margin-top: 2px;
}

/* ── Progress bar ─────────────────────────────────────────── */
.undo-toast__progress {
  position:         absolute;
  bottom:           0;
  left:             0;
  height:           3px;
  width:            100%;
  transform-origin: left;
  animation:        drain 2.5s linear forwards;
}

.undo-toast--success .undo-toast__progress {
  background: var(--color-success);
}

.undo-toast--error .undo-toast__progress {
  background: var(--color-danger);
}

@keyframes drain {
  from { transform: scaleX(1); }
  to   { transform: scaleX(0); }
}

/* ── Transition ───────────────────────────────────────────── */
.undo-toast-enter-active {
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.undo-toast-leave-active {
  transition: all 0.2s ease-in;
}
.undo-toast-enter-from {
  opacity:   0;
  transform: translateX(-50%) translateY(16px) scale(0.95);
}
.undo-toast-leave-to {
  opacity:   0;
  transform: translateX(-50%) translateY(8px);
}
</style>