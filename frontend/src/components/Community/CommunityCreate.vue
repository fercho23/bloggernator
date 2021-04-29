<template>
  <div class="row">
    <div class="col-12">

      <h3>
        Community Create
      </h3>
      <div v-if="error" class="alert alert-danger">Community Error: {{ error }}</div>

      <form @submit.prevent="callCreate" id="createForm">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" name="name" id="name" class="form-control">
        </div>

        <div class="form-group">
          <label for="slug">Slug</label>
          <input type="text" name="slug" id="slug" class="form-control">
        </div>

        <div class="form-group">
          <label for="detail">Detail</label>
          <textarea name="detail" id="detail" class="form-control"></textarea>

        </div>

        <button type="submit" class="btn btn-primary">Create</button>
      </form>

    </div>
  </div>
</template>

<script>
  import { getAPI } from "../../api/axios-base";
  import { URL_API_COMMUNITY_CREATE } from "../../constants.js";

  export default {
    name: "community-create",
    props: ["community"],
    data() {
      return {
        error: undefined,
      }
    },

    methods: {

      callCreate() {
        let formData = new FormData(document.getElementById("createForm"));

        getAPI.post(URL_API_COMMUNITY_CREATE, formData)
          .then((response) => {
            console.log(response);
            this.$store.dispatch("updateLocalCurrentUser");
            this.$router.push({ name: "community-list" });
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