<template>
  <div class="row">
    <div class="col-12">
      <template v-if="post">
        <h3>
          Post Update: <small> {{ post.title }}</small>
        </h3>

        <form @submit.prevent="callUpdate" id="updateForm">
          <div class="form-group">
            <label for="title">Title</label>
            <input type="text" name="title" id="title" class="form-control" :value="post.title">
          </div>

          <div class="form-group">
            <label for="slug">Slug</label> <b-button size="sm" variant="outline-primary" @click="generateSlug()">Generate Slug</b-button>
            <input type="text" name="slug" id="slug" class="form-control" :value="post.slug">
          </div>

          <div class="form-group">
            <label for="community">Community</label>
            <select id="community" name="community" class="form-control" :disabled="currentUser.uuid !== post.author.uuid">
                <option :value="undefined" disabled selected>Select a Community</option>
                <option v-for="(community, index) in communities" 
                  :selected="community.uuid === post.community.uuid"
                  :key="index" 
                  :value="community.slug">{{ community.name }}
                </option>
            </select>
          </div>

          <div class="form-group">
            <label>Contributors</label>
            <span v-for="(contributor, index) in contributors" :key="index" class="badge badge-secondary mx-1 mb-1">
              {{ contributor.username }}
              <b-button class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeContributor(index)">
                <span aria-hidden="true">&times;</span>
              </b-button>
              <input type="hidden" v-model="contributors[index]">
            </span>

            <AutoComplete :api="autocompleteContributors" :prop-to-show="'username'" :function-after="autocompleteContributorsAfter" />
          </div>

          <div class="form-group">
            <label for="language">Language</label>
            <select id="language" name="language" class="form-control" :disabled="currentUser.uuid !== post.author.uuid">
                <option :value="undefined" disabled selected>Select a Language</option>
                <option v-for="(language, index) in allLanguages" 
                  :selected="language.uuid === post.language.uuid"
                  :key="index" 
                  :value="language.slug">{{ language.name }}
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

          <b-button type="submit" class="btn btn-primary">Update</b-button>
        </form>
      </template>
      <template v-else="">
        <span v-if="error" class="alert alert-danger">Post Error: {{ error }}</span>
        <p>Please click on a Post...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import AutoComplete from '../Layout/AutoComplete';
  import { mapState } from 'vuex';
  import strToSlug from '../../utils/strToSlug.js';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_POST_READ, URL_API_POST_UPDATE, URL_API_USER_LIST } from '../../constants.js';

  export default {
    name: 'post-update',
    props: ['post'],
    computed: mapState(['currentUser', 'allLanguages']),
    components: {
      AutoComplete,
    },
    mixins: [
      strToSlug,
    ],

    data() {
      return {
        communities: [],
        contributors: this.post ? this.post.contributors : undefined,
        error: undefined,
      }
    },

    beforeMount() {
      this.getCommunities();
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug);
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

      generateSlug() {
        if (document.getElementById('title') && document.getElementById('title').value) {
          document.getElementById('slug').value = this.strToSlug(document.getElementById('title').value);
        }
      },

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
        let formData = new FormData(document.getElementById('updateForm'));

        getAPI.patch(URL_API_POST_UPDATE.replace(':slug', this.post.slug), formData)
          .then((response) => {
            this.$root.$bvToast.toast(`Post "${response.data.name}" was successfully updated.`, {
              title: 'Success',
              variant: 'success',
              solid: true
            });
            this.$router.push({ name: 'post-list' });
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data.detail, {
              title: 'Error',
              variant: 'danger',
              solid: true
            });
          });
      }
    }
  };
</script>

<style>
</style>