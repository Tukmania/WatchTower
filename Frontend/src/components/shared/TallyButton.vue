<template>
  <button
    class="tally-btn"
    :class="{ 'tally-btn--loading': isLoading, 'tally-btn--pressed': pressed }"
    :disabled="isLoading"
    @click="handleClick"
  >
    <!-- Rainbow glow layer — always animating -->
    <span class="tally-btn__glow" />

    <!-- Dark background layer -->
    <span class="tally-btn__bg" />

    <!-- Content layer — sits above everything -->
    <span class="tally-btn__content">
      <span class="tally-btn__icon">{{ icon }}</span>
      <span class="tally-btn__label">{{ label }}</span>
      <span v-if="isLoading" class="tally-btn__spinner" />
    </span>

  </button>
</template>

<script setup>
import { ref } from 'vue'
import { useEventLogger } from '../../composables/useEventLogger.js'

const props = defineProps({
  label:            { type: String,  required: true },
  icon:             { type: String,  default: '+' },
  variant:          { type: String,  default: 'primary' },
  eventType:        { type: String,  required: true },
  subtype:          { type: String,  default: '' },
  location:         { type: String,  required: true },
  locationCategory: { type: String,  required: true }
})

const emit = defineEmits(['logged'])

const { log, isLoading } = useEventLogger()
const pressed = ref(false)

async function handleClick() {
  pressed.value = true
  setTimeout(() => { pressed.value = false }, 150)

  const result = await log(
    props.eventType,
    props.subtype,
    props.location,
    props.locationCategory
  )

  if (result.success) {
    emit('logged', result.event)
  }
}
</script>

<style scoped>
/* ── Base button ──────────────────────────────────────────── */
.tally-btn {
  width:       100%;
  height:      44px;
  border:      none;
  outline:     none;
  color:       #ffffff;
  background:  transparent;
  cursor:      pointer;
  position:    relative;
  z-index:     0;
  border-radius: 10px;
  padding:     0;
  font-family: var(--font-family);
  user-select: none;
  transition:  transform 0.1s ease, opacity 0.2s ease;
}

.tally-btn:disabled {
  opacity: 0.6;
  cursor:  not-allowed;
}

/* ── Press animation ──────────────────────────────────────── */
.tally-btn--pressed {
  animation: btn-press 0.15s ease;
}

@keyframes btn-press {
  0%   { transform: scale(1); }
  40%  { transform: scale(0.96); }
  100% { transform: scale(1); }
}

/* ── Rainbow glow layer — always glowing, never stops ────── */
.tally-btn__glow {
  content:    '';
  background: linear-gradient(
    45deg,
    #ff0000,
    #ff7300,
    #fffb00,
    #48ff00,
    #00ffd5,
    #002bff,
    #7a00ff,
    #ff00c8,
    #ff0000
  );
  position:         absolute;
  top:              -2px;
  left:             -2px;
  background-size:  400%;
  z-index:          -1;
  filter:           blur(5px);
  width:            calc(100% + 4px);
  height:           calc(100% + 4px);
  animation:        glowing 20s linear infinite;

  /* Always visible — opacity 1 at all times including idle */
  opacity:          1;

  transition:       filter 0.3s ease, opacity 0.3s ease;
  border-radius:    10px;
}

/* On hover — intensify the glow */
.tally-btn:hover:not(:disabled) .tally-btn__glow {
  filter:  blur(8px);
  opacity: 1;
}

/* On click — glow pulses brighter */
.tally-btn:active:not(:disabled) .tally-btn__glow {
  filter:  blur(12px);
  opacity: 1;
}

/* ── Dark solid background layer ─────────────────────────── */
.tally-btn__bg {
  position:      absolute;
  z-index:       -1;
  content:       '';
  width:         100%;
  height:        100%;
  background:    #0f172a;
  left:          0;
  top:           0;
  border-radius: 10px;
  transition:    background 0.15s ease;
}

/* On click — bg flashes slightly lighter */
.tally-btn:active:not(:disabled) .tally-btn__bg {
  background: #1e293b;
}

/* ── Content layer — text and icon ───────────────────────── */
.tally-btn__content {
  position:        relative;
  z-index:         2;
  display:         flex;
  align-items:     center;
  justify-content: center;
  gap:             8px;
  width:           100%;
  height:          100%;
  padding:         0 var(--space-md);
}

.tally-btn__icon {
  font-size:   15px;
  line-height: 1;
  flex-shrink: 0;
}

.tally-btn__label {
  font-size:      var(--font-size-sm);
  font-weight:    600;
  letter-spacing: 0.2px;
  color:          #ffffff;
  white-space:    nowrap;
}

/* On active — label darkens to show press feedback */
.tally-btn:active:not(:disabled) .tally-btn__label {
  color: rgba(255, 255, 255, 0.75);
}

/* ── Loading spinner ──────────────────────────────────────── */
.tally-btn__spinner {
  width:         13px;
  height:        13px;
  border:        2px solid rgba(255, 255, 255, 0.25);
  border-top:    2px solid #ffffff;
  border-radius: 50%;
  animation:     spin 0.6s linear infinite;
  flex-shrink:   0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── The rainbow keyframe animation ──────────────────────── */
@keyframes glowing {
  0%   { background-position: 0 0; }
  50%  { background-position: 400% 0; }
  100% { background-position: 0 0; }
}
</style>