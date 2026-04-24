<template>
  <div class="stat-card">
    <div class="stat-card__left">
      <span class="stat-card__label">{{ label }}</span>
      <span class="stat-card__value" :class="{ 'stat-pop': flash }">
        {{ value }}
      </span>
    </div>
    <div class="stat-card__icon-wrap" :style="{ background: iconBg }">
      <span class="stat-card__icon">{{ icon }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  label:   { type: String, required: true },
  value:   { type: Number, default: 0 },
  icon:    { type: String, default: '📊' },
  iconBg:  { type: String, default: 'rgba(37,99,235,0.1)' }
})

const flash = ref(false)

watch(() => props.value, () => {
  flash.value = true
  setTimeout(() => { flash.value = false }, 400)
})
</script>

<style scoped>
.stat-card {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding:         var(--space-md);
  background:      var(--color-bg-section);
  border-radius:   var(--radius-md);
  border:          1px solid var(--color-border-light);
  transition:      var(--transition);
}

.stat-card:hover {
  background: var(--color-bg-hover);
}

.stat-card__left {
  display:        flex;
  flex-direction: column;
  gap:            4px;
}

.stat-card__label {
  font-size:      var(--font-size-xs);
  font-weight:    600;
  color:          var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.stat-card__value {
  font-size:   var(--font-size-2xl);
  font-weight: 800;
  color:       var(--color-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
  transition:  var(--transition);
}

.stat-pop {
  animation: count-pop 0.4s ease;
}

.stat-card__icon-wrap {
  width:           40px;
  height:          40px;
  border-radius:   var(--radius-md);
  display:         flex;
  align-items:     center;
  justify-content: center;
  flex-shrink:     0;
}

.stat-card__icon {
  font-size: 20px;
}
</style>