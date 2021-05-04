<template>
  <div class="row">
    <div class="col-12">

      <div class="float-right">
        <router-link
          v-if="accessToken!=null"
          class="btn btn-primary mr-1"
          :to="{
            name: 'post-create'
          }">
          Create Post
        </router-link>

        <b-button v-b-toggle.filtersCollapse variant="primary">Toggle Filters</b-button>
      </div>

      <h3>Post List</h3>

      <b-collapse id="filtersCollapse">
        <b-card class="bg-light my-2">
          <template #header>
            <strong>Filters</strong>
          </template>

          <b-card-body>
            <form @submit.prevent="callFilter" id="filterForm">
              <div class="form-row">
                <div class="form-group col-md-12">
                  <label>Title</label>
                  <input type="text" v-model="filters.title" class="form-control">
                </div>
              </div>

              <div class="form-row">
                <div class="form-group col-md-6">
                  <label>Communities</label>
                  <span v-for="(community, index) in filters.communities" :key="index" class="badge badge-secondary mx-1 mb-1">
                    {{ community }}
                    <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeCommunity(index)">
                      <span aria-hidden="true">&times;</span>
                    </button>
                    <input type="hidden" v-model="filters.communities[index]">
                  </span>

                  <AutoComplete :api="autocompleteCommunities" :prop-to-show="'name'" :function-after="autocompleteCommunitiesAfter" />
                </div>

                <div class="form-group col-md-6">
                  <label>Language</label>
                  <select v-model="filters.language" class="form-control">
                      <option :value="undefined">Select a Language</option>
                      <option v-for="(language, index) in allLanguages" 
                        :key="index" 
                        :value="language.slug">{{ language.name }}
                      </option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group col-md-6">
                  <label>Authors</label>
                  <span v-for="(author, index) in filters.authors" :key="index" class="badge badge-secondary mx-1 mb-1">
                    {{ author }}
                    <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeAuthor(index)">
                      <span aria-hidden="true">&times;</span>
                    </button>
                    <input type="hidden" v-model="filters.authors[index]">
                  </span>

                  <AutoComplete :api="autocompleteAuthors" :prop-to-show="'username'" :function-after="autocompleteAuthorsAfter" />
                </div>

                <div class="form-group col-md-6">
                  <label>Contributors</label>
                  <span v-for="(contributor, index) in filters.contributors" :key="index" class="badge badge-secondary mx-1 mb-1">
                    {{ contributor }}
                    <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeContributor(index)">
                      <span aria-hidden="true">&times;</span>
                    </button>
                    <input type="hidden" v-model="filters.contributors[index]">
                  </span>

                  <AutoComplete :api="autocompleteContributors" :prop-to-show="'username'" :function-after="autocompleteContributorsAfter" />
                </div>
              </div>

              <button type="submit" class="btn btn-primary">Filter</button>
              <button type="button" class="btn btn-link float-right" @click="clearFilters()">Clear Filters</button>
            </form>
          </b-card-body>
        </b-card>
      </b-collapse>

      <div class="row">
        <div class="col-6" v-for="(post, index) in posts" :key="index">
          <router-link
            title="Post Detail"
            :to="{
              name: 'post-detail',
              params: { post: post, slug: post.slug }
            }">
            {{ post.title }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import { getAPI } from "../../api/axios-base";
  import AutoComplete from "../Layout/AutoComplete";
  import { URL_API_COMMUNITY_LIST, URL_API_POST_LIST, URL_API_USER_LIST } from "../../constants.js";

  export default {
    name: "post-list",
    computed: mapState(["accessToken", "allLanguages"]),
    components: {
      AutoComplete
    },
    data() {
      return {
        filters: {
          title: this.$route.query.title,
          language: this.$route.query.language,
          authors: this.$route.query.authors === undefined ? undefined : (Array.isArray(this.$route.query.authors) ? this.$route.query.authors : [this.$route.query.authors]),
          contributors: this.$route.query.contributors === undefined ? undefined : (Array.isArray(this.$route.query.contributors) ? this.$route.query.contributors : [this.$route.query.contributors]),
          communities: this.$route.query.communities === undefined ? undefined : (Array.isArray(this.$route.query.communities) ? this.$route.query.communities : [this.$route.query.communities]),
        },
        posts: [],
      };
    },

    beforeRouteUpdate(to, from, next) {
      if (from.query != to.query) {
        this.retrievePostList(to.query);
        next();
      }
    },

    // beforeMount() {
    //   const query = this.$route.query;
    //   this.filters.title = query.title;
    //   this.filters.language = query.language;
    //   this.filters.authors = query.authors === undefined ? undefined : (Array.isArray(query.authors) ? query.authors : [query.authors]);
    //   this.filters.contributors = query.contributors === undefined ? undefined : (Array.isArray(query.contributors) ? query.contributors : [query.contributors]);
    //   this.filters.communities = query.communities === undefined ? undefined : (Array.isArray(query.communities) ? query.communities : [query.communities]);
    // },

    mounted() {
      this.retrievePostList();
    },

    methods: {
      retrievePostList(query=undefined) {
        if (query == undefined)
          query = this.filters;

        getAPI.get(URL_API_POST_LIST, {
            params: query
          })
          .then(response => {
            this.posts = response.data.results;
          })
          .catch(e => {
            console.log(e);
          });
      },

      // AUTHORS
        autocompleteAuthors(username) {
          let query = {};
            query.username = username;
          if (Array.isArray(this.filters.authors))
            query.not_in_username = this.filters.authors;

          return getAPI.get(URL_API_USER_LIST, {
            params: query
          });
        },

        autocompleteAuthorsAfter(selected) {
          if (selected) {
            if (this.filters.authors === undefined)
              this.filters.authors = [];
            this.filters.authors.push(selected.username);
          }
        },

        removeAuthor(index) {
          if (this.filters.authors[index] !== undefined) {
            this.filters.authors.splice(index, 1);
          }
        },
      // -- AUTHORS

      // CONTRIBUTORS
        autocompleteContributors(username) {
          let query = {};
            query.username = username;
          if (Array.isArray(this.filters.contributors))
            query.not_in_username = this.filters.contributors;

          return getAPI.get(URL_API_USER_LIST, {
            params: query
          });
        },

        autocompleteContributorsAfter(selected) {
          if (selected) {
            if (this.filters.contributors === undefined)
              this.filters.contributors = [];
            this.filters.contributors.push(selected.username);
          }
        },

        removeContributor(index) {
          if (this.filters.contributors[index] !== undefined) {
            this.filters.contributors.splice(index, 1);
          }
        },
      // -- CONTRIBUTORS

      // COMMUNITIES
        autocompleteCommunities(name) {
          let query = {};
            query.name = name;
          if (Array.isArray(this.filters.communities))
            query.not_in_name = this.filters.communities;

          return getAPI.get(URL_API_COMMUNITY_LIST, {
            params: query
          });
        },

        autocompleteCommunitiesAfter(selected) {
          if (selected) {
            if (this.filters.communities === undefined)
              this.filters.communities = [];
            this.filters.communities.push(selected.name);
          }
        },

        removeCommunity(index) {
          if (this.filters.communities[index] !== undefined) {
            this.filters.communities.splice(index, 1);
          }
        },
      // -- COMMUNITIES

      clearFilters() {
        Object.keys(this.filters).forEach((i) => this.filters[i] = undefined);
      },

      callFilter() {
        this.$router.replace({
          name: "post-list",
          query: this.filters
        });
      }

    }
  };
</script>

<style>
</style>