<script setup>
import { ref,computed } from "vue";
import TallyButton from "../shared/TallyButton.vue";
import { useCountsStore } from "../../stores/countsStore";


const props = defineProps({
  terminal: { type: Object, required: true },
});

const countsStore = useCountsStore();

const counts = computed(() => {
  return countsStore.getTerminalCounts(props.terminal.name);
});

//Flash state per button type
const bagFlash  = ref(false);
const boxFlash  = ref(false);
const footFlash = ref(false);

function flash(type) {
  if (type === 'bag_wrap')     { bagFlash.value  = true; setTimeout(() => bagFlash.value  = false, 400) }
  if (type === 'box_wrap')     { boxFlash.value  = true; setTimeout(() => boxFlash.value  = false, 400) }
  if (type === 'foot_traffic') { footFlash.value = true; setTimeout(() => footFlash.value = false, 400) }
}

function onLogged(event) {
  flash(event.subtype);
}


</script>

<template>
  <div class="terminal-card card">

    <div class="terminal-card__header">
      <span class="terminal-card__name">{{ terminal.name }}</span>
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
        @logged="onLogged"
      />
    </div>

    <div class="terminal-card__counts">
      <div class="count-item">
        <span class="count-item__icon">🎒</span>
        <span class="count-item__value" :class="{ 'count-pop': bagFlash }">
          {{ counts.bag_wrap || 0 }}
        </span>
      </div>
      <div class="count-item">
        <span class="count-item__icon">📦</span>
        <span class="count-item__value" :class="{ 'count-pop': boxFlash }">
          {{ counts.box_wrap || 0 }}
        </span>
      </div>
      <div class="count-item">
        <span class="count-item__icon">🚶</span>
        <span class="count-item__value" :class="{ 'count-pop': footFlash }">
          {{ counts.foot_traffic || 0 }}
        </span>
      </div>
    </div>

  </div>
</template>


<style scoped>
.terminal-card {
  padding:    var(--space-md);
  display:    flex;
  flex-direction: column;
  gap:        var(--space-sm);
  min-width:  0;
}

.terminal-card__header {
  padding-bottom: var(--space-sm);
  border-bottom:  1px solid var(--color-border-light);
}

.terminal-card__name {
  font-size:   var(--font-size-sm);
  font-weight: 700;
  color:       var(--color-primary);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.terminal-card__buttons {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

/* ── Count bar ────────────────────────────────────────────── */
.terminal-card__counts {
  display:          flex;
  justify-content:  space-around;
  padding-top:      var(--space-sm);
  border-top:       1px solid var(--color-border-light);
  margin-top:       var(--space-xs);
}

.count-item {
  display:        flex;
  flex-direction: column;
  align-items:    center;
  gap:            2px;
}

.count-item__icon {
  font-size: 13px;
}

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
</style>