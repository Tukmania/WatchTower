<template>
  <div class="log-table">

    <!-- Filters bar -->
    <div class="log-table__filters">

      <div class="filter-group">
        <label class="filter-group__label">Search</label>
        <input
          v-model="searchQuery"
          type="text"
          class="filter-group__input"
          placeholder="Location or event type..."
        />
      </div>

      <div class="filter-group">
        <label class="filter-group__label">Category</label>
        <select v-model="filterCategory" class="filter-group__select">
          <option value="">All</option>
          <option value="terminal">Terminal</option>
          <option value="shop">Shop</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-group__label">Event Type</label>
        <select v-model="filterType" class="filter-group__select">
          <option value="">All</option>
          <option value="bag_wrap">Bag Wrap</option>
          <option value="box_wrap">Box Wrap</option>
          <option value="foot_traffic">Foot Traffic</option>
          <option value="interaction">Interaction</option>
          <option value="walkin">Walk-in</option>
          <option value="receipt">Receipt</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-group__label">Time Block</label>
        <select v-model="filterBlock" class="filter-group__select">
          <option value="">All Blocks</option>
          <option
            v-for="block in availableBlocks"
            :key="block"
            :value="block"
          >
            {{ block }}
          </option>
        </select>
      </div>

      <button class="filter-clear" @click="clearFilters">
        Clear
      </button>

    </div>

    <!-- Results count -->
    <div class="log-table__meta">
      <span class="log-table__count">
        {{ filteredEvents.length }} event{{ filteredEvents.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- Table -->
    <div class="log-table__wrapper">
      <table class="log-table__table">
        <thead>
          <tr>
            <th class="col-num">#</th>
            <th class="col-time">Timestamp</th>
            <th class="col-block">Time Block</th>
            <th class="col-location">Location</th>
            <th class="col-category">Category</th>
            <th class="col-type">Event Type</th>
          </tr>
        </thead>
        <tbody>
          <!-- Empty state -->
          <tr v-if="filteredEvents.length === 0">
            <td colspan="6" class="log-table__empty">
              <span class="log-table__empty-icon">🔍</span>
              <p>No events match your filters</p>
            </td>
          </tr>

          <!-- Rows -->
          <tr
            v-for="(event, index) in filteredEvents"
            :key="event.id"
            class="log-table__row"
          >
            <td class="col-num">{{ index + 1 }}</td>
            <td class="col-time">
              <span class="log-table__timestamp">
                {{ event.timestamp }}
              </span>
            </td>
            <td class="col-block">
              <span class="log-table__block-pill">
                {{ event.time_block }}
              </span>
            </td>
            <td class="col-location">
              <div class="log-table__location">
                <span>
                  {{ event.location_category === 'terminal' ? '✈️' : '🏪' }}
                </span>
                <span class="log-table__location-name">
                  {{ event.location }}
                </span>
              </div>
            </td>
            <td class="col-category">
              <span class="log-table__category"
                :class="event.location_category === 'terminal'
                  ? 'category--terminal'
                  : 'category--shop'"
              >
                {{ event.location_category }}
              </span>
            </td>
            <td class="col-type">
              <EventTypeBadge
                :type="event.event_type"
                :subtype="event.subtype"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useEventStore } from '../../stores/eventStore.js'
import EventTypeBadge    from './EventTypeBadge.vue'

const eventStore = useEventStore()

const searchQuery    = ref('')
const filterCategory = ref('')
const filterType     = ref('')
const filterBlock    = ref('')

function clearFilters() {
  searchQuery.value    = ''
  filterCategory.value = ''
  filterType.value     = ''
  filterBlock.value    = ''
}

// All unique time blocks from events — for the dropdown
const availableBlocks = computed(() => {
  const blocks = new Set(eventStore.allEvents.map(e => e.time_block))
  return [...blocks].sort()
})

const filteredEvents = computed(() => {
  return eventStore.allEvents.filter(event => {
    const key = event.subtype || event.event_type

    const matchSearch = !searchQuery.value ||
      event.location.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      event.event_type.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchCategory = !filterCategory.value ||
      event.location_category === filterCategory.value

    const matchType = !filterType.value ||
      key === filterType.value

    const matchBlock = !filterBlock.value ||
      event.time_block === filterBlock.value

    return matchSearch && matchCategory && matchType && matchBlock
  })
})
</script>

<style scoped>
.log-table {
  display:        flex;
  flex-direction: column;
  gap:            var(--space-md);
  height:         100%;
  min-height:     0;
}

/* ── Filters ──────────────────────────────────────────────── */
.log-table__filters {
  display:     flex;
  align-items: flex-end;
  gap:         var(--space-md);
  flex-wrap:   wrap;
  padding:     var(--space-md);
  background:  var(--color-bg-card);
  border-radius: var(--radius-lg);
  border:      1px solid var(--color-border);
}

.filter-group {
  display:        flex;
  flex-direction: column;
  gap:            4px;
  flex:           1;
  min-width:      140px;
}

.filter-group__label {
  font-size:      var(--font-size-xs);
  font-weight:    600;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color:          var(--color-text-muted);
}

.filter-group__input,
.filter-group__select {
  padding:       8px var(--space-sm);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-sm);
  font-family:   var(--font-family);
  color:         var(--color-text-primary);
  background:    var(--color-bg-section);
  outline:       none;
  transition:    var(--transition);
}

.filter-group__input:focus,
.filter-group__select:focus {
  border-color: var(--color-primary-light);
  background:   var(--color-bg-card);
}

.filter-clear {
  padding:       8px var(--space-md);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background:    transparent;
  font-size:     var(--font-size-sm);
  font-weight:   600;
  color:         var(--color-text-secondary);
  cursor:        pointer;
  transition:    var(--transition);
  font-family:   var(--font-family);
  align-self:    flex-end;
  white-space:   nowrap;
}

.filter-clear:hover {
  background:  var(--color-bg-section);
  color:       var(--color-text-primary);
}

/* ── Meta ─────────────────────────────────────────────────── */
.log-table__meta {
  padding: 0 var(--space-xs);
}

.log-table__count {
  font-size:   var(--font-size-sm);
  font-weight: 500;
  color:       var(--color-text-muted);
}

/* ── Table wrapper ────────────────────────────────────────── */
.log-table__wrapper {
  flex:         1;
  overflow-y:   auto;
  background:   var(--color-bg-card);
  border-radius: var(--radius-lg);
  border:       1px solid var(--color-border);
}

/* ── Table ────────────────────────────────────────────────── */
.log-table__table {
  width:           100%;
  border-collapse: collapse;
  font-size:       var(--font-size-sm);
}

.log-table__table thead {
  position:    sticky;
  top:         0;
  z-index:     10;
  background:  var(--color-bg-section);
}

.log-table__table th {
  padding:     12px var(--space-md);
  text-align:  left;
  font-size:   var(--font-size-xs);
  font-weight: 700;
  color:       var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  border-bottom: 2px solid var(--color-border);
  white-space:  nowrap;
}

/* ── Rows ─────────────────────────────────────────────────── */
.log-table__row {
  border-bottom: 1px solid var(--color-border-light);
  transition:    background 0.15s ease;
}

.log-table__row:hover {
  background: var(--color-bg-section);
}

.log-table__row:last-child {
  border-bottom: none;
}

.log-table__table td {
  padding:     10px var(--space-md);
  vertical-align: middle;
}

/* ── Column widths ────────────────────────────────────────── */
.col-num      { width: 48px; color: var(--color-text-muted); font-size: var(--font-size-xs); }
.col-time     { width: 160px; }
.col-block    { width: 150px; }
.col-location { min-width: 180px; }
.col-category { width: 110px; }
.col-type     { width: 140px; }

/* ── Cell content ─────────────────────────────────────────── */
.log-table__timestamp {
  font-variant-numeric: tabular-nums;
  color:                var(--color-text-secondary);
}

.log-table__block-pill {
  display:       inline-block;
  padding:       2px 8px;
  background:    var(--color-bg-section);
  border:        1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-xs);
  font-weight:   600;
  color:         var(--color-text-secondary);
  white-space:   nowrap;
}

.log-table__location {
  display:     flex;
  align-items: center;
  gap:         var(--space-xs);
}

.log-table__location-name {
  font-weight: 500;
  color:       var(--color-text-primary);
}

.log-table__category {
  display:       inline-block;
  padding:       2px 8px;
  border-radius: var(--radius-sm);
  font-size:     var(--font-size-xs);
  font-weight:   600;
  text-transform: capitalize;
}

.category--terminal {
  background: rgba(37, 99, 235, 0.08);
  color:      #1d4ed8;
}

.category--shop {
  background: rgba(245, 158, 11, 0.1);
  color:      #92400e;
}

/* ── Empty ────────────────────────────────────────────────── */
.log-table__empty {
  text-align:  center;
  padding:     var(--space-2xl) !important;
  color:       var(--color-text-muted);
}

.log-table__empty-icon {
  display:       block;
  font-size:     32px;
  margin-bottom: var(--space-sm);
}
</style>