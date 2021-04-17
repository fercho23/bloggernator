<template>
  <div class="row">
    <div class="col-12">
      <h3>
        Post Create
      </h3>
      <span v-if="error">Post Error: {{ error }}</span>
      <span v-if="errorGetCommunities">Post Error: {{ error }}</span>

      <form @submit.prevent="callCreate" id="createForm">
        <div class="form-group">
          <label for="title">Title</label>
          <input type="text" name="title" id="title" class="form-control">
        </div>

        <div class="form-group">
          <label for="slug">Slug</label>
          <input type="text" name="slug" id="slug" class="form-control">
        </div>

        <div class="form-group">
          <label for="community">Community</label>
          <select id="community" name="community" class="form-control">
              <option disabled selected>Select a Community</option>
              <option v-for="(community, index) in communities" 
                :key="index" 
                :value="community.uuid">{{ community.name }}
              </option>
          </select>
        </div>

        <div class="form-group">
          <label for="language">Language</label>
          <select id="language" name="language" class="form-control">
              <option disabled selected>Select a Language</option>
              <option v-for="(language, index) in languages" 
                :key="index" 
                :value="language.uuid">{{ language.name }}
              </option>
          </select>
        </div>

        <div class="form-group">
          <label for="body">Body</label>
          <input type="text" name="body" id="body" class="form-control">
        </div>

        <div class="form-group">
          <label for="abstract">Abstract</label>
          <input type="text" name="abstract" id="abstract" class="form-control">
        </div>

        <button type="submit" class="btn btn-primary">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import { getAPI } from "../../api/axios-base";
  import { URL_API_COMMUNITY_CURRENT_USER_LIST, URL_API_POST_CREATE } from "../../constants.js";

  export default {
    name: "post-create",
    computed: mapState(["languages"]),
    data() {
      return {
        communities: [],
        error: undefined,
        errorGetCommunities: undefined,
      }
    },
    beforeMount() {
      this.getCommunities();
    },

    methods: {
      getCommunities() {
        const params = new URLSearchParams();
        params.append("current_user", this.$store.state.currentUser.uuid);

        getAPI.get(URL_API_COMMUNITY_CURRENT_USER_LIST, {
          params: params
        })
          .then((response) => {
            this.communities = response.data;
          })
          .catch(e => {
            this.errorGetCommunities = e.response.data.detail;
          });
      },

      callCreate() {
        let formData = new FormData(document.getElementById("createForm"));

        getAPI.post(URL_API_POST_CREATE, formData)
          .then((response) => {
            console.log(response);
            this.$router.push({ name: "post-list" });
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