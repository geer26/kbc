<template>
  <img alt="background" src="./static/img/background.jpg" />
  <Loginmodal :msg="msg" v-if="showLoginmodal"/>
  <Addfirst :msg="msg" v-if="showFirstUser" />
</template>

<script>
import Loginmodal from './components/Loginmodal.vue'
import Addfirst from './components/Addfirst.vue'

export default {
  
  name: 'App',

  components: {
    Loginmodal,
    Addfirst,
  },

  data() {
    return {
      showLoginmodal: false,
      showFirstUser: true,
      msg: '',
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

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
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
