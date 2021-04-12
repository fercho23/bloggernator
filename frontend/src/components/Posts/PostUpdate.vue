<template>
  <div v-if="this.post">
    <h3>
      Post Update: <small></small>
    </h3>

    <form @submit.prevent="postUpdate">
      <div class="form-group">
        <label for="field-title">Title</label>
        <input type="text" name="field-title" id="field-title" :value="this.post.title" class="form-control">
      </div>

      <div class="form-group">
        <label for="field-body">Body</label>
        <input type="text" name="field-body" id="field-body" :value="this.post.body" class="form-control">
      </div>

      <div class="form-group">
        <label for="field-abstract">Abstract</label>
        <input type="text" name="field-abstract" id="field-abstract" :value="this.post.abstract" class="form-control">
      </div>

      <button type="submit" class="btn btn-primary">Update</button>
    </form>
  </div>
  <div v-else="">
    <span v-if="error">Post Error: {{ error }}</span>
    <p>Please click on a Post...</p>
  </div>

</template>

<script>
  import { getAPI } from '../../api/axios-base'
  import { URL_API_POST_READ, URL_API_POST_UPDATE } from '../../constants.js';

  export default {
    name: "post-update",
    props: ["post"],
    data() {
      return {
        error: undefined,
        form: {
          title: '',
          body: '',
          abstract: ''
        }
      }
    },
    beforeMount() {
      console.log(this.post);
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug)
    },
    methods: {
      retrievePost(slug) {
        getAPI
          .get(URL_API_POST_READ.replace(':slug', slug))
          .then(response => {
            this.post = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },

      postUpdate() {
        getAPI
          .patch(URL_API_POST_UPDATE.replace(':slug', this.post.slug), this.form)
            .then((response) => {
              console.log(response);
            });
      }
    }
  };
</script>

<style>
</style>