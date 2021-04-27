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
                <label for="title">Title</label>
                <input type="text" v-model="filters.title" class="form-control">
              </div>

              <div class="form-group col-md-6">
                <label for="language">Language</label>
                <select v-model="filters.language" class="form-control">
                    <option :value="undefined">Select a Language</option>
                    <option v-for="(language, index) in allLanguages" 
                      :key="index" 
                      :value="language.slug">{{ language.name }}
                    </option>
                </select>
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
  import { URL_API_POST_LIST } from "../../constants.js";

  export default {
    name: "post-list",
    computed: mapState(["accessToken", "allLanguages"]),
    data() {
      return {
        filters: {
          title: this.$route.query.title,
          language: this.$route.query.language,
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
          query = this.$route.query;

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