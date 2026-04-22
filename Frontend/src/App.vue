<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f0f4f8;
}
</style>