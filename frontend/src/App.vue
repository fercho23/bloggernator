
<template>
    <div id="app">
      <NavBar></NavBar>

      <div class="container container-fluid mt-2">
        <router-view/>
      </div>
    </div>
</template>

<script>
  import NavBar from "./components/Layout/NavBar.vue";

  export default {
    name: "app",
    components: {
      NavBar
    },
    mounted() {
      this.$store.dispatch("getLanguages");
    },
  };
</script>

<style>
</style>