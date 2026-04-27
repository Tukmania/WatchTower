<template>
  <div class="shop-card card" :class="{ 'shop-card--offline': !isOnline }">

    <div class="shop-card__header">
      <span class="shop-card__name">{{ shop.name }}</span>
      <span v-if="!isOnline" class="offline-chip">OFFLINE</span>
    </div>

    <div class="shop-card__buttons">
      <TallyButton
        label="Interaction"
        icon="🤝"
        variant="interaction"
        event-type="interaction"
        subtype=""
        :location="shop.name"
        location-category="shop"
        :disabled="!isOnline"
        @logged="onLogged('interaction')"
      />
      <TallyButton
        label="Walk-in"
        icon="🚶"
        variant="walkin"
        event-type="walkin"
        subtype=""
        :location="shop.name"
        location-category="shop"
        :disabled="!isOnline"
        @logged="onLogged('walkin')"
      />
      <TallyButton
        label="Receipt"
        icon="🧾"
        variant="receipt"
        event-type="receipt"
        subtype=""
        :location="shop.name"
        location-category="shop"
        :disabled="!isOnline"
        @logged="onLogged('receipt')"
      />
    </div>

    <div class="shop-card__counts">
      <template v-if="isOnline">
        <div class="count-item">
          <span class="count-item__label">Interactions</span>
          <span class="count-item__value" :class="{ 'count-pop': interactionFlash }">{{ counts.interaction || 0 }}</span>
        </div>
        <div class="count-item">
          <span class="count-item__label">Walk-ins</span>
          <span class="count-item__value" :class="{ 'count-pop': walkinFlash }">{{ counts.walkin || 0 }}</span>
        </div>
        <div class="count-item">
          <span class="count-item__label">Receipts</span>
          <span class="count-item__value" :class="{ 'count-pop': receiptFlash }">{{ counts.receipt || 0 }}</span>
        </div>
      </template>
      <div v-else class="offline-notice">Offline — data paused</div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed }  from 'vue'
import { useCountsStore } from '../../stores/countsStore.js'
import { useStatusStore } from '../../stores/statusStore.js'
import TallyButton        from '../shared/TallyButton.vue'

const props = defineProps({
  shop: { type: Object, required: true }
})

const countsStore = useCountsStore()
const statusStore = useStatusStore()

const isOnline = computed(() => statusStore.isOnline(props.shop.name))
const counts   = computed(() => countsStore.getShopCounts(props.shop.name))

const interactionFlash = ref(false)
const walkinFlash      = ref(false)
const receiptFlash     = ref(false)

function flash(type) {
  const map = { interaction: interactionFlash, walkin: walkinFlash, receipt: receiptFlash }
  if (map[type]) {
    map[type].value = true
    setTimeout(() => { map[type].value = false }, 400)
  }
}

function onLogged(type) { flash(type) }
</script>

<style scoped>
.shop-card {
  padding:        var(--space-md);
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
  min-width:      0;
  transition:     opacity 0.2s ease, background 0.2s ease;
}

.shop-card--offline {
  opacity:    0.72;
  background: var(--color-bg-section) !important;
}

.shop-card__header {
  display:         flex;
  align-items:     center;
  justify-content: space-between;
  padding-bottom:  var(--space-sm);
  border-bottom:   1px solid var(--color-border-light);
}

.shop-card__name {
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

.shop-card__buttons {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-xs);
}

/* ── Count bar ────────────────────────────────────────────── */
.shop-card__counts {
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

.count-item__label {
  font-size:      var(--font-size-xs);
  color:          var(--color-text-muted);
  font-weight:    500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.count-item__value {
  font-size:   var(--font-size-md);
  font-weight: 700;
  color:       var(--color-primary);
  text-align:  center;
  transition:  var(--transition);
}

.count-pop {
  animation: count-pop 0.4s ease;
}

.offline-notice {
  font-size:      11px;
  font-weight:    600;
  color:          var(--color-danger, #dc2626);
  text-align:     center;
  letter-spacing: 0.3px;
}
</style>
