<template>
  <div id="app">
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>

    <!-- Global overlays — mounted once at root -->
    <ConfirmationFlash />
    <UndoToast
      :message="undoMessage"
      :success="undoSuccess"
      :trigger="undoTrigger"
    />
  </div>
</template>

<script setup>
import { ref, watch, watchEffect } from 'vue'
import { RouterView }              from 'vue-router'
import ConfirmationFlash           from './components/shared/ConfirmationFlash.vue'
import UndoToast                   from './components/shared/UndoToast.vue'
import { useEventStore }           from './stores/eventStore.js'
import { useThemeStore }           from './stores/themeStore.js'

const undoMessage = ref('')
const undoSuccess = ref(true)
const undoTrigger = ref(0)

const eventStore = useEventStore()
watch(() => eventStore.lastUndoResult, (result) => {
  if (!result) return
  undoMessage.value = result.message
  undoSuccess.value = result.success
  undoTrigger.value++
})

const themeStore = useThemeStore()
watchEffect(() => {
  document.documentElement.classList.toggle('dark', themeStore.isDark)
})
</script>