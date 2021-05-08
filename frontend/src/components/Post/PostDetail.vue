<template>
  <div class="row">
    <div class="col-12">
      <template v-if="post">
        <router-link
          v-if="isAuthorOrContributorInPost(post)"
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

        <div class="row">
          <div class="col-6">
            <dl>
              <template v-if="post.author && Object.keys(post.author).length">
                <dt>Author</dt>
                <dd class="ml-4">
                  <router-link
                    title="Profile"
                    class="btn btn-link text-primary my-1"
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
                    :to="{
                      name: 'profile',
                      params: { slug: user.username }
                    }">
                    {{ user.username }}
                  </router-link>
                </dd>
              </template>
            </dl>
          </div>
        </div>

        <hr>
        <hr>

        <div class="row">
          <div class="col-12">
            <h6>
              Rapid Filters Actions
            </h6>
          </div>

          <div class="col-12">
            <router-link
              class="btn btn-light mr-1"
              :to="{
                name: 'post-list',
                query: { authors: [post.author.username] }

              }">
              Author's Posts
            </router-link>

            <router-link
              class="btn btn-light mr-1"
              :to="{
                name: 'post-list',
                query: { communities: [post.community.name] }
              }">
              Community's Posts
            </router-link>

            <router-link
              class="btn btn-light mr-1"
              :to="{
                name: 'post-list',
                query: { language: post.language.slug }
              }">
              Language Posts
            </router-link>
          </div>

          <div class="col-12 mt-3">
            <h6>
              More personalized filters
            </h6>
          </div>

          <div class="col-12">
            <form @submit.prevent="callFilter" id="filterForm">

              <div class="form-check form-check-inline">
                <input type="checkbox" class="form-check-input" v-model="filters.checkboxAuthor">
                <label class="form-check-label">Author</label>
              </div>

              <div class="form-check form-check-inline">
                <input type="checkbox" class="form-check-input" v-model="filters.checkboxCommunity">
                <label class="form-check-label">Community</label>
              </div>

              <div class="form-check form-check-inline">
                <input type="checkbox" class="form-check-input" v-model="filters.checkboxLanguage">
                <label class="form-check-label">Language</label>
              </div>

              <template v-if="post.contributors && post.contributors.length">
                <br>
                <div v-for="(user, index) in post.contributors" :key="index" class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" v-model="filters.checkboxContributors[index]">
                  <label class="form-check-label">Contributor {{ user.username }}</label>
                </div>
              </template>

              <br>
              <button type="submit" class="btn btn-primary mt-2">Get Posts!</button>
            </form>
          </div>
        </div>

      </template>
      <template v-else="">
        <span v-if="error">Post Error: {{ error }}</span>
        <p>Please click on a Post...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { getAPI } from '../../api/axios-base';
  import { URL_API_POST_READ } from '../../constants.js';
  import isAuthorOrContributorInPost from '../../utils/isAuthorOrContributorInPost.js';

  export default {
    name: 'post-detail',
    props: ['post'],
    mixins: [
      isAuthorOrContributorInPost
    ],
    data() {
      return {
        filters: {
          checkboxAuthor: undefined,
          checkboxCommunity: undefined,
          checkboxLanguage: undefined,
          checkboxContributors: [],
        },

        error: undefined,
      };
    },
    beforeMount() {
      if (this.post === undefined)
        this.retrievePost(this.$route.params.slug);
    },
    methods: {
      callFilter() {

        let query = {}

        if (this.filters.checkboxAuthor) {
          query.authors = [this.post.author.username];
        }
        if (this.filters.checkboxCommunity) {
          query.communities = [this.post.community.name];
        }
        if (this.filters.checkboxLanguage) {
          query.language = this.post.language.slug;
        }
        if (this.filters.checkboxContributors && this.filters.checkboxContributors.length) {
          query.contributors = [];
          for (let i = 0; i < this.filters.checkboxContributors.length; i++) {
            query.contributors.push(this.post.contributors[i].username)
          }
        }

        this.$router.replace({
          name: 'post-list',
          query: query
        });
      },

      updatePost(post) {
        console.log(post)
      },

      retrievePost(slug) {
        getAPI.get(URL_API_POST_READ.replace(':slug', slug))
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