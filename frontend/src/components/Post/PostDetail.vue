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
        </h3>

        <div>
          {{ post.body }}
        </div>

        <hr>
        <hr>

        <strong>
          Author:
        </strong>
        <router-link
          v-if="isAuthorOrContributor(post)"
          title="Profile"
          class="btn btn-link text-primary my-1"
          :to="{
            name: 'profile',
            params: { username: post.author.username }
          }">
          {{ post.author.username }}
        </router-link>
        <router-link
          class="btn btn-light"
          :to="{
            name: 'post-list',
            query: { authors: post.author.username }
          }">
          Author's Posts
        </router-link>
        <br>

        <strong>
          Community:
        </strong>
        <router-link
          class="btn btn-link text-primary my-1"
          title="Community Detail"
          :to="{
            name: 'community-detail',
            params: { slug: post.community.slug }
          }">
          {{ post.community.name }}
        </router-link>
        <router-link
          class="btn btn-light"
          :to="{
            name: 'post-list',
            query: { community: post.community.slug }
          }">
          Community's Posts
        </router-link>
        <br>

        <strong>
          Language:
        </strong>
        {{ post.language.name }}
        <router-link
          class="btn btn-light my-1"
          :to="{
            name: 'post-list',
            query: { language: post.language.slug }
          }">
          Language Posts
        </router-link>
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
  import isAuthorOrContributor from "../../utils/isAuthorOrContributor.js";

  export default {
    name: "post-detail",
    props: ["post"],
    mixins: [
      isAuthorOrContributor
    ],
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