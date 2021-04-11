<template>
    <div class="row">
        <div class="col-12">
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
import { getAPI } from '../../api/axios-base'
import { URL_API_POST_LIST } from '../../constants.js';

export default {
  name: "post-list",
  data() {
    return {
      posts: []
    };
  },
  methods: {
    /* eslint-disable no-console */
    retrievePostList() {
      getAPI
        .get(URL_API_POST_LIST)
        .then(response => {
          this.posts = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    }
    /* eslint-enable no-console */
  },
  mounted() {
    this.retrievePostList();
  }
};
</script>

<style>
</style>