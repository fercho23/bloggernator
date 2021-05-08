<template>
  <div class="row">
    <div class="col-12">
      <template v-if="user">
        <h3>
          Profile Update: <small> {{ user.username }}</small>
        </h3>
        <div class="alert alert-danger" v-if="error">Profile Error: {{ error }}</div>

        <form @submit.prevent="callUpdate" id="updateForm">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" class="form-control" :value="user.username">
          </div>

          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </template>
      <template v-else="">
        <div class="alert alert-danger" v-if="error">Profile Error: {{ error }}</div>
        <p>Please click on a Profile...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { getAPI } from "../../api/axios-base";
  import { URL_API_USER_READ, URL_API_USER_UPDATE } from "../../constants.js";

  export default {
    name: 'profile-update',
    props: ['user'],
    data() {
      return {
        error: undefined,
      }
    },

    beforeMount() {
      if (this.user === undefined)
        this.retrieveUser(this.$route.params.username);
    },
    methods: {

      retrieveUser(username) {
        getAPI.get(URL_API_USER_READ.replace(':username', username))
          .then(response => {
            this.user = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },

      callUpdate() {
        let formData = new FormData(document.getElementById('updateForm'));

        getAPI.patch(URL_API_USER_UPDATE.replace(':username', this.user.username), formData)
          .then((response) => {
            console.log(response);
            this.user.username = formData.get('username')
            this.$store.commit('updateCurrentUser', this.user);
            this.$router.push({
              name: 'profile',
              params: { username: this.user.username }
            });
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