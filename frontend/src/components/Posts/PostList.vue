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

      <div class="row">
        <div class="col-6" v-for="(post, index) in posts" :key="index">
          <router-link :to="{
              name: 'post-details',
              params: { post: post, slug: post.slug }
            }">
            {{post.title}}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_POST_LIST } from '../../constants.js';

  export default {
    name: "post-list",
    computed: mapState(['accessToken']),
    data() {
      return {
        posts: []
      };
    },
    methods: {
      retrievePostList() {
        getAPI.get(URL_API_POST_LIST)
          .then(response => {
            this.posts = response.data.results;
          })
          .catch(e => {
            console.log(e);
          });
      }
    },
    mounted() {
      this.retrievePostList();
    }
  };
</script>

<style>
</style>