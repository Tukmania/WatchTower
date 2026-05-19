import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount }                                  from '@vue/test-utils'
import { setActivePinia, createPinia }            from 'pinia'
import TallyButton                                from '../../components/shared/TallyButton.vue'

// ── Single combined mock for api/events.js ────────────────────────────────
vi.mock('../../api/events.js', () => ({
  logEvent: vi.fn().mockResolvedValue({
    data: {
      id:         1,
      event_type: 'wrap',
      subtype:    'bag_wrap',
      location:   'TERMINAL 1A',
      timestamp:  '2025-11-28 10:24:10',
      time_block: '10:00 – 10:30',
      shift_date: '2025-11-28'
    }
  }),
  fetchRecentEvents: vi.fn().mockResolvedValue({ data: [] })
}))

// ── Single combined mock for api/counts.js ────────────────────────────────
// Both fetchCounts AND fetchHourlyCounts must live in ONE vi.mock call
// Two vi.mock calls for the same file — second one overwrites the first
vi.mock('../../api/counts.js', () => ({
  fetchCounts: vi.fn().mockResolvedValue({
    data: {
      terminals:     {},
      shops:         {},
      summary:       {},
      block_summary: {},
      current_block: '10:00 – 10:30'
    }
  }),
  fetchHourlyCounts: vi.fn().mockResolvedValue({
    data: {
      hours:  ['10:00', '11:00', '12:00'],
      counts: [5, 10, 15]
    }
  }),
  fetchTrend: vi.fn().mockResolvedValue({ data: [] })
}))

// ─────────────────────────────────────────────────────────────────────────
describe('TallyButton', () => {

  beforeEach(() => {
    setActivePinia(createPinia())
  })

  // ── Test 1 ────────────────────────────────────────────────────────────
  it('renders the label correctly', () => {
    const wrapper = mount(TallyButton, {
      props: {
        label:            'Bag Wrap',
        icon:             '🎒',
        variant:          'bag-wrap',
        eventType:        'wrap',
        subtype:          'bag_wrap',
        location:         'TERMINAL 1A',
        locationCategory: 'terminal'
      }
    })

    expect(wrapper.text()).toContain('Bag Wrap')
  })

  // ── Test 2 ────────────────────────────────────────────────────────────
  it('renders a button element', () => {
    const wrapper = mount(TallyButton, {
      props: {
        label:            'Bag Wrap',
        icon:             '🎒',
        variant:          'bag-wrap',
        eventType:        'wrap',
        subtype:          'bag_wrap',
        location:         'TERMINAL 1A',
        locationCategory: 'terminal'
      }
    })

    expect(wrapper.find('button').exists()).toBe(true)
  })

  // ── Test 3 ────────────────────────────────────────────────────────────
  it('is not disabled when not loading', () => {
    const wrapper = mount(TallyButton, {
      props: {
        label:            'Bag Wrap',
        icon:             '🎒',
        variant:          'bag-wrap',
        eventType:        'wrap',
        subtype:          'bag_wrap',
        location:         'TERMINAL 1A',
        locationCategory: 'terminal'
      }
    })

    expect(wrapper.find('button').attributes('disabled')).toBeUndefined()
  })

  // ── Test 4 ────────────────────────────────────────────────────────────
  it('calls log event when clicked', async () => {
    const { logEvent } = await import('../../api/events.js')

    const wrapper = mount(TallyButton, {
      props: {
        label:            'Bag Wrap',
        icon:             '🎒',
        variant:          'bag-wrap',
        eventType:        'wrap',
        subtype:          'bag_wrap',
        location:         'TERMINAL 1A',
        locationCategory: 'terminal'
      }
    })

    await wrapper.find('button').trigger('click')
    await wrapper.vm.$nextTick()

    expect(logEvent).toHaveBeenCalled()
  })

  // ── Test 5 ────────────────────────────────────────────────────────────
it('emits logged event after successful click', async () => {
  const { flushPromises } = await import('@vue/test-utils')

  const wrapper = mount(TallyButton, {
    props: {
      label:            'Bag Wrap',
      icon:             '🎒',
      variant:          'bag-wrap',
      eventType:        'wrap',
      subtype:          'bag_wrap',
      location:         'TERMINAL 1A',
      locationCategory: 'terminal'
    }
  })

  // Trigger the click
  await wrapper.find('button').trigger('click')

  // flushPromises drains every pending Promise in the queue completely
  // This waits for the ENTIRE chain to finish:
  // handleClick → log() → logEvent() → prependEvent() → refreshCounts() → emit()
  await flushPromises()

  // Now the emit chain is guaranteed to have completed
  expect(wrapper.emitted('logged')).toBeTruthy()
})

  // ── Test 6 ────────────────────────────────────────────────────────────
  it('shows spinner when loading', async () => {
    const wrapper = mount(TallyButton, {
      props: {
        label:            'Bag Wrap',
        icon:             '🎒',
        variant:          'bag-wrap',
        eventType:        'wrap',
        subtype:          'bag_wrap',
        location:         'TERMINAL 1A',
        locationCategory: 'terminal'
      }
    })

    // Before clicking — spinner must not exist
    expect(wrapper.find('.tally-btn__spinner').exists()).toBe(false)

    // Start the click but do not await — we want to catch the loading state
    wrapper.find('button').trigger('click')

    // One tick is enough for isLoading to flip to true
    await wrapper.vm.$nextTick()

    // Spinner must now be visible
    expect(wrapper.find('.tally-btn__spinner').exists()).toBe(true)
  })

})