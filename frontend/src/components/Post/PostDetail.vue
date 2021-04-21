<template>
  <div class="row">
    <div class="col-12">
      <template v-if="post">
        <router-link
          v-if="isAuthorOrContributor(post)"
          class="btn btn-primary float-right"
          :to="{
            name: 'post-update',
            params: { post: post, slug: post.slug }
          }">
          Update
        </router-link>

        <h3>
          {{ post.title }}
          <br>
          <small>
            <router-link
              class="btn btn-light"
              title="Community Detail"
              :to="{
                name: 'community-detail',
                params: { slug: post.community.slug }
              }">
              {{ post.community.name }}
            </router-link>
             - {{ post.language.name }}
          </small>
        </h3>

        <div>
          {{ post.body }}

          <br>
          <small>
            Author: <router-link
              v-if="isAuthorOrContributor(post)"
              class="btn btn-light"
              :to="{
                name: 'profile',
                params: { username: post.author.username }
              }">
              {{ post.author.username }}
            </router-link>
          </small>
        </div>

        <ul class="list-group mt-1">
          <li class="list-group-item list-group-item-primary">
            <h5>
              Some quick actions
            </h5>
          </li>
          <li class="list-group-item">
            Find more posts from company 
            <router-link
              class="btn btn-light"
              :to="{
                name: 'post-list',
                query: { community: post.community.slug }
              }">
              {{ post.community.name }}
            </router-link>
            .
          </li>

          <li class="list-group-item">
            Find more posts in 
            <router-link
              class="btn btn-light"
              :to="{
                name: 'post-list',
                query: { language: post.language.slug }
              }">
              {{ post.language.name }}
            </router-link>
            .
          </li>
        </ul>
      </template>
      <template v-else="">
        <span v-if="error">Post Error: {{ error }}</span>
        <p>Please click on a Post...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { getAPI } from "../../api/axios-base";
  import { URL_API_POST_READ } from "../../constants.js";

  export default {
    name: "post-detail",
    props: ["post"],
    data() {
      return {
        error: undefined,
      }
    },
    beforeMount() {
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug);
    },
    methods: {
      isAuthorOrContributor(post) {
        const uuid = this.$store.state.currentUser.uuid;
        if (post.author.uuid == uuid)
          return true;

        const contributors = post.contributors.map(({ uuid }) => uuid);
        if (contributors.includes(uuid))
          return true;

        return false;
      },
      updatePost(post) {
        console.log(post)
      },
      retrievePost(slug) {
        getAPI.get(URL_API_POST_READ.replace(":slug", slug))
          .then(response => {
            this.post = response.data;
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