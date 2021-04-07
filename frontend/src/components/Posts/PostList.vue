<template>
    <div class="row">
        <div class="col-12">
            <h4>Post List</h4>

            <ul>
                <li v-for="(post, index) in posts" :key="index">
                    <router-link :to="{
                            name: 'post-details',
                            params: { post: post, uuid: post.uuid }
                        }">
                            {{post.title}}
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import http from "../../http-common";

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
      http
        .get("/post/list/")
        .then(response => {
          this.posts = response.data.results; // JSON are parsed automatically.
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },
    refreshList() {
      this.retrievePostList();
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