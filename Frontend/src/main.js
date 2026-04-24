import { createApp }        from 'vue'
import { createPinia }      from 'pinia'
import piniaPersistedState  from 'pinia-plugin-persistedstate'
import router               from './router/index.js'
import App                  from './App.vue'
import './assets/main.css'

const pinia = createPinia()
pinia.use(piniaPersistedState)

const app = createApp(App)

app.use(pinia)
app.use(router)

app.mount('#app')