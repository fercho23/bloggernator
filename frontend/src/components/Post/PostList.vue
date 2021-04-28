<template>
  <div class="row">
    <div class="col-12">
      <router-link
        v-if="accessToken!=null"
        class="btn btn-primary float-right"
        :to="{
          name: 'post-create'
        }">
        Create Post
      </router-link>
      <h3>Post List</h3>

      <div class="card bg-light my-2">
        <div class="card-header">
          <strong>
            Filters
          </strong>
        </div>

        <div class="card-body">
          <form @submit.prevent="callFilter" id="filterForm">
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>Title</label>
                <input type="text" v-model="filters.title" class="form-control">
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
                  <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeAuthor($event, index)">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <input type="hidden" v-model="filters.authors[index]">
                </span>

                <AutoComplete :api="autocompleteUsers" :prop-to-show="'username'" :function-after="autocompleteUsersAfter" />
              </div>

              <div class="form-group col-md-6">
                <label>Communities</label>
                <span v-for="(community, index) in filters.communities" :key="index" class="badge badge-secondary mx-1 mb-1">
                  {{ community }}
                  <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeCommunity($event, index)">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <input type="hidden" v-model="filters.communities[index]">
                </span>

                <AutoComplete :api="autocompleteCommunity" :prop-to-show="'name'" :function-after="autocompleteCommunityAfter" />
              </div>
            </div>

            <button type="submit" class="btn btn-primary">Filter</button>
          </form>
        </div>
      </div>

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
          authors: Array.isArray(this.$route.query.authors) || this.$route.query.authors === undefined ? this.$route.query.authors : [this.$route.query.authors],
          communities: Array.isArray(this.$route.query.communities) || this.$route.query.communities === undefined ? this.$route.query.communities : [this.$route.query.communities],
          // community: this.$route.query.community,
        },
        posts: []
      };
    },

    beforeRouteUpdate(to, from, next) {
      if (from.query != to.query) {
        this.retrievePostList(to.query);
        next();
      }
    },

    // beforeMount() {
    //   this.getCommunities();
    // },

    mounted() {
      this.retrievePostList();
    },
    methods: {
      retrievePostList(query=undefined) {
        if (query == undefined)
          query = this.filters

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

      autocompleteUsers(username) {
        let query = {};
          query.username = username;
        if (Array.isArray(this.filters.authors))
          query.not_in_username = this.filters.authors;

        return getAPI.get(URL_API_USER_LIST, {
          params: query
        });
      },

      autocompleteUsersAfter(selected) {
        if (this.filters.authors === undefined)
          this.filters.authors = [];
        this.filters.authors.push(selected.username);
      },

      removeAuthor(event, index) {
        if (this.filters.authors.indexOf(index)) {
          delete this.filters.authors[index];
          event.currentTarget.parentNode.remove();
        }
      },

      autocompleteCommunity(name) {
        let query = {};
          query.name = name;
        if (Array.isArray(this.filters.communities))
          query.not_in_name = this.filters.communities;

        return getAPI.get(URL_API_COMMUNITY_LIST, {
          params: query
        });
      },

      autocompleteCommunityAfter(selected) {
        if (this.filters.communities === undefined)
          this.filters.communities = [];
        this.filters.communities.push(selected.name);
      },

      removeCommunity(event, index) {
        if (this.filters.communities.indexOf(index)) {
          delete this.filters.communities[index];
          event.currentTarget.parentNode.remove();
        }
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