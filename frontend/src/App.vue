<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <Loginmodal msg="Welcome to Your Vue.js App"/>
</template>

<script>
import Loginmodal from './components/Loginmodal.vue'

export default {
  name: 'App',
  components: {
    Loginmodal
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
