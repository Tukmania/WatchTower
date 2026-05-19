import { describe, it, expect, vi, beforeEach } from 'vitest'
import { nextTick }                              from 'vue'
import { mount }                                 from '@vue/test-utils'
import { createPinia, setActivePinia }           from 'pinia'
import { useCountsStore }                        from '../../stores/countsStore.js'
import TerminalCard                              from '../../components/terminals/TerminalCard.vue'

vi.mock('../../api/events.js', () => ({
  logEvent: vi.fn().mockResolvedValue({
    data: {
      id:         1,
      event_type: 'wrap',
      subtype:    'bag_wrap',
      location:   'TERMINAL 1A',
      timestamp:  '2025-11-28 10:00:00',
      time_block: '10:00 – 10:30',
      shift_date: '2025-11-28'
    }
  }),
  fetchRecentEvents: vi.fn().mockResolvedValue({ data: [] })
}))

vi.mock('../../api/counts.js', () => ({
  fetchCounts: vi.fn().mockResolvedValue({
    data: {
      terminals:     {},
      shops:         {},
      summary:       {},
      block_summary: {},
      current_block: ''
    }
  }),
  fetchTrend:        vi.fn().mockResolvedValue({ data: [] }),
  fetchHourlyCounts: vi.fn().mockResolvedValue({ data: {} })
}))

describe('TerminalCard', () => {

  let pinia

  beforeEach(() => {
    pinia = createPinia()
    setActivePinia(pinia)
  })

  function mountCard(terminalProps = { id: 'terminal_1a', name: 'TERMINAL 1A' }) {
    return mount(TerminalCard, {
      props: {
        terminal: terminalProps
      },
      global: {
        plugins: [pinia]
      }
    })
  }

  it('displays the terminal name', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('TERMINAL 1A')
  })

  it('renders three tally buttons', () => {
    const wrapper = mountCard()
    expect(wrapper.findAll('button')).toHaveLength(3)
  })

  it('displays counts from the store', async () => {
    const store = useCountsStore()

    store.terminalCounts = {
      'TERMINAL 1A': { bag_wrap: 7, box_wrap: 3, foot_traffic: 15 }
    }

    const wrapper = mountCard()

    // nextTick is from Vue — waits for reactive re-render
    await nextTick()

    expect(wrapper.text()).toContain('7')
    expect(wrapper.text()).toContain('3')
    expect(wrapper.text()).toContain('15')
  })

  it('shows zero counts when store has no data for terminal', () => {
    const wrapper = mountCard()
    const countValues = wrapper.findAll('.count-item__value')
    countValues.forEach(count => {
      expect(count.text()).toBe('0')
    })
  })

})