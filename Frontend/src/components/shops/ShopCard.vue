<template>
  <div class="shop-card card">

    <div class="shop-card__header">
      <span class="shop-card__name">{{ shop.name }}</span>
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
        @logged="onLogged('receipt')"
      />
    </div>

    <div class="shop-card__counts">
      <div class="count-item">
        <span class="count-item__label">Interactions</span>
        <span class="count-item__value" :class="{ 'count-pop': interactionFlash }">
          {{ counts.interaction || 0 }}
        </span>
      </div>
      <div class="count-item">
        <span class="count-item__label">Walk-ins</span>
        <span class="count-item__value" :class="{ 'count-pop': walkinFlash }">
          {{ counts.walkin || 0 }}
        </span>
      </div>
      <div class="count-item">
        <span class="count-item__label">Receipts</span>
        <span class="count-item__value" :class="{ 'count-pop': receiptFlash }">
          {{ counts.receipt || 0 }}
        </span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCountsStore } from '../../stores/countsStore.js'
import TallyButton from '../shared/TallyButton.vue'

const props = defineProps({
  shop: { type: Object, required: true }
})

const countsStore = useCountsStore()
const counts = computed(() => countsStore.getShopCounts(props.shop.name))

const interactionFlash = ref(false)
const walkinFlash      = ref(false)
const receiptFlash     = ref(false)

function flash(type) {
  const map = {
    interaction: interactionFlash,
    walkin:      walkinFlash,
    receipt:     receiptFlash
  }
  if (map[type]) {
    map[type].value = true
    setTimeout(() => { map[type].value = false }, 400)
  }
}

function onLogged(type) {
  flash(type)
}
</script>

<style scoped>
.shop-card {
  padding:        var(--space-md);
  display:        flex;
  flex-direction: column;
  gap:            var(--space-sm);
  min-width:      0;
}

.shop-card__header {
  padding-bottom: var(--space-sm);
  border-bottom:  1px solid var(--color-border-light);
}

.shop-card__name {
  font-size:      var(--font-size-sm);
  font-weight:    700;
  color:          var(--color-primary);
  letter-spacing: 0.5px;
  text-transform: uppercase;
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
  padding-top:     var(--space-sm);
  border-top:      1px solid var(--color-border-light);
  margin-top:      var(--space-xs);
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
</style>