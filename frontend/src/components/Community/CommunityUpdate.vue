<template>
  <div class="row">
    <div class="col-12">
      <template v-if="community">
        <h3>
          Community Update: <small> {{ community.name }}</small>
        </h3>
        <div class="alert alert-danger" v-if="error">Community Error: {{ error }}</div>

        <form @submit.prevent="callUpdate" id="updateForm">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" name="name" id="name" class="form-control" :value="community.name">
          </div>

          <div class="form-group">
            <label for="slug">Slug</label>
            <input type="text" name="slug" id="slug" class="form-control" :value="community.slug">
          </div>

          <div class="form-group">
            <label for="detail">Detail</label>
            <input type="text" name="detail" id="detail" class="form-control" :value="community.detail">
          </div>

          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </template>
      <template v-else="">
        <div class="alert alert-danger" v-if="error">Community Error: {{ error }}</div>
        <p>Please click on a Community...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { getAPI } from "../../api/axios-base";
  import { URL_API_COMMUNITY_READ, URL_API_COMMUNITY_UPDATE } from "../../constants.js";

  export default {
    name: "community-update",
    props: ["community"],
    data() {
      return {
        error: undefined,
      }
    },

    beforeMount() {
      if (this.community === undefined)
        this.retrieveCommunity(this.$route.params.slug);
    },
    methods: {

      retrieveCommunity(slug) {
        getAPI.get(URL_API_COMMUNITY_READ.replace(":slug", slug))
          .then(response => {
            this.community = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },

      callUpdate() {
        let formData = new FormData(document.getElementById("updateForm"));

        getAPI.patch(URL_API_COMMUNITY_UPDATE.replace(":slug", this.community.slug), formData)
          .then((response) => {
            console.log(response);
            this.$router.push({ name: "community-detail", params: { slug: this.community.slug } });
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