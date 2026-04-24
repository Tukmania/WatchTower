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
import { ref }              from 'vue'
import { RouterView }       from 'vue-router'
import ConfirmationFlash    from './components/shared/ConfirmationFlash.vue'
import UndoToast            from './components/shared/UndoToast.vue'
import { useEventStore }    from './stores/eventStore.js'
import { watch }            from 'vue'

const undoMessage = ref('')
const undoSuccess = ref(true)
const undoTrigger = ref(0)

// Listen for undo events from anywhere in the app
// QuickActionsBar emits to a global event bus via store
const eventStore = useEventStore()
watch(() => eventStore.lastUndoResult, (result) => {
  if (!result) return
  undoMessage.value = result.message
  undoSuccess.value = result.success
  undoTrigger.value++
})
</script>