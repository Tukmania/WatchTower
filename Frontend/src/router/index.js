import { createRouter, createWebHistory } from 'vue-router'
import DashboardView  from '../views/DashboardView.vue'
import EventLogView   from '../views/EventLogView.vue'
import ReportsView    from '../views/ReportsView.vue'
import SettingsView   from '../views/SettingsView.vue'
import TerminalsView  from '../views/TerminalsView.vue'
import ShopsView      from '../views/ShopsView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/terminals',
    name: 'Terminals',
    component: TerminalsView
  },
  {
    path: '/shops',
    name: 'Shops',
    component: ShopsView
  },
  {
    path: '/events',
    name: 'EventLog',
    component: EventLogView
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ReportsView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router