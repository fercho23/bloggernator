<template>
  <div class="row">
    <div class="col-12">
      <h3>
        Post Create
      </h3>
      <span v-if="error" class="alert alert-danger">Post Error: {{ error }}</span>
      <span v-if="errorGetCommunities" class="alert alert-danger">Post Error: {{ error }}</span>

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
              <option :value="undefined" disabled selected>Select a Community</option>
              <option v-for="(community, index) in communities" 
                :key="index" 
                :value="community.uuid">{{ community.name }}
              </option>
          </select>
        </div>

        <div class="form-group">
          <label>Contributors</label>
          <span v-for="(contributor, index) in contributors" :key="index" class="badge badge-secondary mx-1 mb-1">
            {{ contributor.username }}
            <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeContributor(index)">
              <span aria-hidden="true">&times;</span>
            </button>
            <input type="hidden" v-model="contributors[index]">
          </span>

          <AutoComplete :api="autocompleteContributors" :prop-to-show="'username'" :function-after="autocompleteContributorsAfter" />
        </div>

        <div class="form-group">
          <label for="language">Language</label>
          <select id="language" name="language" class="form-control">
              <option :value="undefined" disabled selected>Select a Language</option>
              <option v-for="(language, index) in allLanguages" 
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
  import AutoComplete from '../Layout/AutoComplete';
  import { mapState } from 'vuex';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_POST_CREATE, URL_API_USER_LIST } from '../../constants.js';

  export default {
    name: 'post-create',
    computed: mapState(['currentUser', 'allLanguages']),
    components: {
      AutoComplete
    },
    data() {
      return {
        contributors: undefined,
        communities: [],
        error: undefined,
        errorGetCommunities: undefined,
      }
    },
    beforeMount() {
      this.getCommunities();
    },

    methods: {

      // CONTRIBUTORS
        autocompleteContributors(username) {
          let query = {};
            query.username = username;

          query.not_in_username = [];
          query.not_in_username.push(this.currentUser.username);
          if (Array.isArray(this.contributors))
            query.not_in_username = query.not_in_username.concat(this.contributors.map(({ username }) => username))

          return getAPI.get(URL_API_USER_LIST, {
            params: query
          });
        },

        autocompleteContributorsAfter(selected) {
          if (selected) {
            if (this.contributors === undefined)
              this.contributors = [];
            this.contributors.push(selected);
          }
        },

        removeContributor(index) {
          if (this.contributors[index] !== undefined) {
            this.contributors.splice(index, 1);
          }
        },
      // -- CONTRIBUTORS

      getCommunities() {
        this.communities = this.currentUser.owns_communities.concat(this.currentUser.member_communities)
      },

      callCreate() {
        let formData = new FormData(document.getElementById('createForm'));

        getAPI.post(URL_API_POST_CREATE, formData)
          .then((response) => {
            console.log(response);
            this.$router.push({ name: 'post-list' });
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