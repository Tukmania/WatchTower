<script setup>
import { ref, computed }    from 'vue'
import TallyButton          from '../shared/TallyButton.vue'
import { useCountsStore }   from '../../stores/countsStore'
import { useStatusStore }   from '../../stores/statusStore.js'

const props = defineProps({
  terminal: { type: Object, required: true }
})

const countsStore = useCountsStore()
const statusStore = useStatusStore()

const isOnline = computed(() => statusStore.isOnline(props.terminal.name))
const counts   = computed(() => countsStore.getTerminalCounts(props.terminal.name))

const bagFlash  = ref(false)
const boxFlash  = ref(false)
const footFlash = ref(false)

function flash(type) {
  if (type === 'bag_wrap')     { bagFlash.value  = true; setTimeout(() => bagFlash.value  = false, 400) }
  if (type === 'box_wrap')     { boxFlash.value  = true; setTimeout(() => boxFlash.value  = false, 400) }
  if (type === 'foot_traffic') { footFlash.value = true; setTimeout(() => footFlash.value = false, 400) }
}

function onLogged(event) { flash(event.subtype) }
</script>

<template>
  <div class="terminal-card card" :class="{ 'terminal-card--offline': !isOnline }">

    <div class="terminal-card__header">
      <span class="terminal-card__name">{{ terminal.name }}</span>
      <span v-if="!isOnline" class="offline-chip">OFFLINE</span>
    </div>

    <div class="terminal-card__buttons">
      <TallyButton
        label="Bag Wrap"
        icon="🎒"
        variant="bag-wrap"
        event-type="wrap"
        subtype="bag_wrap"
        :location="terminal.name"
        location-category="terminal"
        :disabled="!isOnline"
        @logged="onLogged"
      />
      <TallyButton
        label="Box Wrap"
        icon="📦"
        variant="box-wrap"
        event-type="wrap"
        subtype="box_wrap"
        :location="terminal.name"
        location-category="terminal"
        :disabled="!isOnline"
        @logged="onLogged"
      />
      <TallyButton
        label="Foot Traffic"
        icon="🚶"
        variant="foot-traffic"
        event-type="foot_traffic"
        subtype="foot_traffic"
        :location="terminal.name"
        location-category="terminal"
        :disabled="!isOnline"
        @logged="onLogged"
      />
    </div>

    <div class="terminal-card__counts">
      <template v-if="isOnline">
        <div class="count-item">
          <span class="count-item__icon">🎒</span>
          <span class="count-item__value" :class="{ 'count-pop': bagFlash }">{{ counts.bag_wrap || 0 }}</span>
        </div>
        <div class="count-item">
          <span class="count-item__icon">📦</span>
          <span class="count-item__value" :class="{ 'count-pop': boxFlash }">{{ counts.box_wrap || 0 }}</span>
        </div>
        <div class="count-item">
          <span class="count-item__icon">🚶</span>
          <span class="count-item__value" :class="{ 'count-pop': footFlash }">{{ counts.foot_traffic || 0 }}</span>
        </div>
      </template>
      <div v-else class="offline-notice">Offline — data paused</div>
    </div>

  </div>
</template>


<style scoped>
.terminal-card {
  padding:        var(--space-md);
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
  min-width:      0;
  transition:     opacity 0.2s ease, background 0.2s ease;
}

.terminal-card--offline {
  opacity:    0.72;
  background: var(--color-bg-section) !important;
}

.terminal-card__header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding-bottom:  var(--space-sm);
  border-bottom:   1px solid var(--color-border-light);
}

.terminal-card__name {
  font-size:      var(--font-size-sm);
  font-weight:    700;
  color:          var(--color-primary);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.offline-chip {
  font-size:      9px;
  font-weight:    700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  background:     rgba(220, 38, 38, 0.1);
  color:          var(--color-danger, #dc2626);
  border:         1px solid rgba(220, 38, 38, 0.25);
  padding:        2px 7px;
  border-radius:  10px;
}

.terminal-card__buttons {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-xs);
}

/* ── Count bar ────────────────────────────────────────────── */
.terminal-card__counts {
  display:         flex;
  justify-content: space-around;
  align-items:     center;
  padding-top:     var(--space-sm);
  border-top:      1px solid var(--color-border-light);
  margin-top:      var(--space-xs);
  min-height:      44px;
}

.count-item {
  display:        flex;
  flex-direction: column;
  align-items:    center;
  gap:            2px;
}

.count-item__icon  { font-size: 13px; }

.count-item__value {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
  min-width:   24px;
  text-align:  center;
  transition:  var(--transition);
}

.count-pop {
  animation: count-pop 0.4s ease;
}

.offline-notice {
  font-size:   11px;
  font-weight: 600;
  color:       var(--color-danger, #dc2626);
  text-align:  center;
  letter-spacing: 0.3px;
}
</style>
