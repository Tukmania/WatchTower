import { ref, onMounted, onUnmounted } from 'vue'

export function useTimeBlock() {
  const currentBlock = ref('')
  let   timer        = null

  function compute() {
    const now         = new Date()
    const minutes     = now.getHours() * 60 + now.getMinutes()
    const blockStart  = Math.floor(minutes / 30) * 30
    const blockEnd    = blockStart + 30

    const startH = Math.floor(blockStart / 60)
    const startM = blockStart % 60
    const endH   = Math.floor(blockEnd / 60) >= 24 ? 0 : Math.floor(blockEnd / 60)
    const endM   = blockEnd % 60

    currentBlock.value =
      `${String(startH).padStart(2,'0')}:${String(startM).padStart(2,'0')} – ` +
      `${String(endH).padStart(2,'0')}:${String(endM).padStart(2,'0')}`
  }

  onMounted(() => {
    compute()
    timer = setInterval(compute, 60000)
  })

  onUnmounted(() => {
    clearInterval(timer)
  })

  return { currentBlock }
}