<script setup>
import { computed } from "vue";
import { useCountsStore } from "../../stores/countsStore.js";
import ShopCard from "./ShopCard.vue";
import { SHOPS } from "../../constants/shops.js";

const countsStore = useCountsStore();
const shops = SHOPS;
const currentBlock = computed(() => countsStore.currentBlock || "—");
</script>

<template>
  <div class="shops-panel">
    <div class="panel-header">
      <div class="panel-header__left">
        <span class="panel-header__icon">🏪</span>
        <div>
          <h2 class="panel-header__title">Retail Shops</h2>
          <p class="panel-header__sub">
            Track interactions, walk-ins & receipts
          </p>
        </div>
      </div>
      <div class="panel-header__block">
        <span class="section-label">Current block</span>
        <span class="panel-header__time">{{ currentBlock }}</span>
      </div>
    </div>

    <div class="shops-panel__grid">
      <ShopCard v-for="shop in shops" :key="shop.id" :shop="shop" />
    </div>
  </div>
</template>

<style scoped>
.shops-panel {
  background: var(--color-bg-card);
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.panel-header__left {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.panel-header__icon {
  font-size: 22px;
}

.panel-header__title {
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--color-primary);
}

.panel-header__sub {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-top: 1px;
}

.panel-header__block {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.panel-header__time {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-bg-section);
  border: 1px solid var(--color-border);
  padding: 3px 10px;
  border-radius: var(--radius-sm);
}

/* ── Grid ─────────────────────────────────────────────────── */
.shops-panel__grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-sm);
}

@media (max-width: 1400px) {
  .shops-panel__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
