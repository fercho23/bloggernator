<template>
  <div class="row">
    <div class="col-12">
      <template v-if="post">
        <h3>
          {{ post.title }}
        </h3>

        <div>
          {{ post.body }}
        </div>

        <hr>

        <div class="row">
          <div class="col-6">
            <dl>
              <template v-if="post.author && Object.keys(post.author).length">
                <dt>Author</dt>
                <dd class="ml-4">
                  <router-link
                    class="btn btn-link text-primary my-1"
                    title="Profile"
                    :to="{
                      name: 'profile',
                      params: { username: post.author.username }
                    }">
                    {{ post.author.username }}
                  </router-link>
                </dd>
              </template>

              <template v-if="post.community && Object.keys(post.community).length">
                <dt>Community</dt>
                <dd class="ml-4">
                  <router-link
                    class="btn btn-link text-primary my-1"
                    title="Community Detail"
                    :to="{
                      name: 'community-detail',
                      params: { slug: post.community.slug }
                    }">
                    {{ post.community.name }}
                  </router-link>
                </dd>
              </template>
            </dl>
          </div>
          <div class="col-6">
            <dl>
              <template v-if="post.contributors && post.contributors.length">
                <dt>Contributors</dt>
                <dd v-for="(user, index) in post.contributors" :key="index" class="ml-4">
                  <router-link
                    title="Profile"
                    :to="{
                      name: 'profile',
                      params: { username: user.username }
                    }">
                    {{ user.username }}
                  </router-link>
                </dd>
              </template>
            </dl>
          </div>
        </div>

        <form @submit.prevent="callDelete" id="deleteForm">
          <button type="submit" class="btn btn-primary">Delete</button>
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
  import { getAPI } from '../../api/axios-base';
  import { URL_API_POST_DELETE, URL_API_POST_READ } from '../../constants.js';
  import isAuthorOrContributorInPost from '../../utils/isAuthorOrContributorInPost.js';

  export default {
    name: 'post-detail',
    props: ['post'],
    mixins: [
      isAuthorOrContributorInPost
    ],
    data() {
      return {
        error: undefined,
      };
    },
    beforeMount() {
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug);
    },
    methods: {
      retrievePost(slug) {
        getAPI.get(URL_API_POST_READ.replace(':slug', slug))
          .then(response => {
            this.post = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },
      callDelete() {
        getAPI.delete(URL_API_POST_DELETE.replace(':slug', this.post.slug))
          .then(() => {
            this.$root.$bvToast.toast(`Post "${this.post.name}" was successfully deleted.`, {
              title: 'Success',
              variant: 'success',
              solid: true
            });
            this.$store.dispatch('updateLocalCurrentUser');
            this.$router.push({ name: 'post-list'});
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