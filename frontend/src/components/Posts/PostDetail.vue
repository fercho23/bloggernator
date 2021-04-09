<template>
  <div v-if="this.post">
    <span v-if="isAuthorOrContributor(this.post)" v-on:click="updatePost(this.post)" class="btn btn-primary float-right">Update</span>

    <h4>{{this.post.title}}</h4>

    <div>
      {{this.post.body}}
    </div>
  </div>
  <div v-else="">
    <span v-if="error">Post Error: {{ error }}</span>
    <p>Please click on a Post...</p>
  </div>

</template>

<script>
import http from "../../http-common";

export default {
  name: "post-details",
  props: ["post"],
  data() {
    return {
      error: undefined,
    }
  },
  beforeMount() {
    if (this.post === undefined)
      this.retrievePost(this.$route.params.slug)
  },
  methods: {
    isAuthorOrContributor(post) {
      if (post.author)
        return true
      return false
    },
    updatePost(post) {
      console.log(post)
    },
    retrievePost(slug) {
      http
        .get("/post/" + slug + "/")
        .then(response => {
          this.post = response.data;
        })
        .catch(e => {
          this.error = e.response.data.detail;
        });
    }
  }
};
</script>

<style>
</style>