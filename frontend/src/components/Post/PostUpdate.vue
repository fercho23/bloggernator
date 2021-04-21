<template>
  <div class="row">
    <div class="col-12">
      <template v-if="post">
        <h3>
          Post Update: <small> {{ post.title }}</small>
        </h3>
        <span v-if="error">Post Error: {{ error }}</span>
        <span v-if="errorGetCommunities">Post Error: {{ error }}</span>

        <form @submit.prevent="callUpdate" id="updateForm">
          <div class="form-group">
            <label for="title">Title</label>
            <input type="text" name="title" id="title" class="form-control" :value="post.title">
          </div>

          <div class="form-group">
            <label for="slug">Slug</label>
            <input type="text" name="slug" id="slug" class="form-control" :value="post.slug">
          </div>

          <div class="form-group">
            <label for="community">Community</label>
            <select id="community" name="community" class="form-control" :disabled="currentUser.uuid !== post.author.uuid">
                <option disabled selected>Select a Community</option>
                <option v-for="(community, index) in communities" 
                  :selected="community.uuid === post.community.uuid"
                  :key="index" 
                  :value="community.uuid">{{ community.name }}
                </option>
            </select>
          </div>

        <div class="form-group">
          <label for="language">Language</label>
          <select id="language" name="language" class="form-control" :disabled="currentUser.uuid !== post.author.uuid">
              <option disabled selected>Select a Language</option>
              <option v-for="(language, index) in languages" 
                :selected="language.uuid === post.language.uuid"
                :key="index" 
                :value="language.uuid">{{ language.name }}
              </option>
          </select>
        </div>

          <div class="form-group">
            <label for="body">Body</label>
            <input type="text" name="body" id="body" class="form-control" :value="post.body">
          </div>

          <div class="form-group">
            <label for="abstract">Abstract</label>
            <input type="text" name="abstract" id="abstract" class="form-control" :value="post.abstract">
          </div>

          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </template>
      <template v-else="">
        <span v-if="error">Post Error: {{ error }}</span>
        <p>Please click on a Post...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import { getAPI } from "../../api/axios-base";
  import { URL_API_POST_READ, URL_API_POST_UPDATE } from "../../constants.js";

  export default {
    name: "post-update",
    props: ["post"],
    computed: mapState(["currentUser", "languages"]),
    data() {
      return {
        communities: [],
        error: undefined,
        errorGetCommunities: undefined,
      }
    },

    beforeMount() {
      this.getCommunities();
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug);
    },
    methods: {
      getCommunities() {
        this.communities = this.currentUser.owns_communities.concat(this.currentUser.member_communities)
      },

      retrievePost(slug) {
        getAPI.get(URL_API_POST_READ.replace(':slug', slug))
          .then(response => {
            this.post = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },

      callUpdate() {
        let formData = new FormData(document.getElementById("updateForm"));

        getAPI.patch(URL_API_POST_UPDATE.replace(':slug', this.post.slug), formData)
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