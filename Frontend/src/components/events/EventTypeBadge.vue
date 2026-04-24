<template>
  <span class="badge" :class="`badge--${variant}`">
    <span class="badge__dot" />
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type:    { type: String, required: true },
  subtype: { type: String, default: '' }
})

const config = {
  bag_wrap:     { label: 'Bag Wrap',     variant: 'bag-wrap'     },
  box_wrap:     { label: 'Box Wrap',     variant: 'box-wrap'     },
  foot_traffic: { label: 'Foot Traffic', variant: 'foot-traffic' },
  interaction:  { label: 'Interaction',  variant: 'interaction'  },
  walkin:       { label: 'Walk-in',      variant: 'walkin'       },
  receipt:      { label: 'Receipt',      variant: 'receipt'      }
}

const resolved = computed(() => {
  // Terminal events use subtype as the key
  // Shop events use event_type as the key
  const key = props.subtype || props.type
  return config[key] || { label: props.type, variant: 'default' }
})

const label   = computed(() => resolved.value.label)
const variant = computed(() => resolved.value.variant)
</script>

<style scoped>
.badge {
  display:       inline-flex;
  align-items:   center;
  gap:           5px;
  padding:       3px 10px;
  border-radius: 999px;
  font-size:     var(--font-size-xs);
  font-weight:   600;
  white-space:   nowrap;
  letter-spacing: 0.2px;
}

.badge__dot {
  width:         6px;
  height:        6px;
  border-radius: 50%;
  flex-shrink:   0;
}

/* ── Variants ─────────────────────────────────────────────── */
.badge--bag-wrap {
  background: rgba(37, 99, 235, 0.1);
  color:      #1d4ed8;
}
.badge--bag-wrap .badge__dot { background: #2563eb; }

.badge--box-wrap {
  background: rgba(124, 58, 237, 0.1);
  color:      #6d28d9;
}
.badge--box-wrap .badge__dot { background: #7c3aed; }

.badge--foot-traffic {
  background: rgba(5, 150, 105, 0.1);
  color:      #047857;
}
.badge--foot-traffic .badge__dot { background: #059669; }

.badge--interaction {
  background: rgba(37, 99, 235, 0.1);
  color:      #1d4ed8;
}
.badge--interaction .badge__dot { background: #2563eb; }

.badge--walkin {
  background: rgba(220, 38, 38, 0.1);
  color:      #b91c1c;
}
.badge--walkin .badge__dot { background: #dc2626; }

.badge--receipt {
  background: rgba(5, 150, 105, 0.1);
  color:      #047857;
}
.badge--receipt .badge__dot { background: #059669; }

.badge--default {
  background: rgba(148, 163, 184, 0.15);
  color:      var(--color-text-muted);
}
.badge--default .badge__dot { background: var(--color-text-muted); }
</style>