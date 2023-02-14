<template>
  <img alt="background" src="./static/img/background.jpg" />
  <Loginmodal msg="Welcome to Your Vue.js App" v-if="showLoginmodal"/>
</template>

<script>
import Loginmodal from './components/Loginmodal.vue'

export default {
  name: 'App',
  components: {
    Loginmodal
  },
  data() {
    return {
      showLoginmodal: true,
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;

  overflow: hidden;
}

img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  object-fit: fill;
  z-index: -9999;
}
</style>
