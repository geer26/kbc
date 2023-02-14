<template>
    <div class="modal">
        <h2>login</h2>
        <label for="username">username</label>
        <input type="text" id="username" ref="username">
        <label for="password">password</label>
        <input type="password" id="password" ref="password">
        <button>submit</button>
    </div>
</template>

<script>
export default {
  name: 'Loginmodal',
  props: {
    msg: String
  }
}
</script>

<style scoped>

.modal {
    border-radius: 5px;
    max-width: 70%;
    max-height: 70%;
    background: var(--light_gray);
    padding: 10px;
    box-shadow: var(--modal_shadow);
    -webkit-box-shadow: var(--modal_shadow);
    color: var(--dark_logo_blue);

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.modal h2 {
    margin: 5px;
}

.modal label {
    margin: 10px;
    font-size: .8rem;
    font-weight: bold;
}

.modal button {
    margin: 10px;
}

</style>
