<template>
  <div v-if="this.post">
    <h4>{{this.post.title}}</h4>
    <div>
      {{this.post.body}}
    </div>
  </div>
  <div v-else="">
    <br>
    <p>Please click on a Post...</p>
  </div>
</template>

<script>
console.log(this);

export default {
  name: "post-details",
  props: ["post"],
};
</script>

<style>
</style>