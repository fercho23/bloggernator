<template>
  <div class="row">
    <div class="col-12">
      <template v-if="community">
        <div class="float-right">
          <router-link
            v-if="isOwnerInCommunity(community)"
            class="btn btn-primary ml-1"
            :to="{
              name: 'community-update',
              params: { community: community, slug: community.slug }
            }">
            Update
          </router-link>
          <router-link
            v-if="isOwnerInCommunity(community)"
            class="btn btn-primary ml-1"
            :to="{
              name: 'community-delete',
              params: { community: community, slug: community.slug }
            }">
            Delete
          </router-link>
        </div>

        <h3>Community Detail</h3>

        <div class="row">
          <div class="col-6">
            <dl>
              <dt>Name</dt>
              <dd class="ml-4">{{ community.name }}</dd>
            </dl>
          </div>

          <div class="col-6">
            <template v-if="community.owner && Object.keys(community.owner).length">
              <dl>
                <dt>Owner</dt>
                <dd class="ml-4">
                  <router-link
                    title="Profile"
                    :to="{
                      name: 'profile',
                      params: { username: community.owner.username }
                    }">
                    {{ community.owner.username }}
                  </router-link>
                </dd>
              </dl>
            </template>
          </div>

          <div class="col-12">
            <dl>
              <template v-if="community.detail">
                <dt>Detail</dt>
                <dd class="ml-4">{{ community.detail }}</dd>
              </template>

              <template v-if="community.members && community.members.length">
                <dt>Members</dt>
                <dd v-for="(user, index) in community.members" :key="index" class="ml-4">
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

              <template v-if="community.last_posts && community.last_posts.length">
                <dt>Last Posts</dt>
                <dd v-for="(post, index) in community.last_posts" :key="index" class="ml-4">
                  <router-link
                    title="Post Detail"
                    :to="{
                      name: 'post-detail',
                      params: { slug: post.slug }
                    }">
                    {{ post.title }}
                  </router-link>
                </dd>
              </template>
            </dl>
          </div>

        </div>
      </template>
      <template v-else="">
        <span v-if="error" class="alert alert-danger">Community Error: {{ error }}</span>
        <p>Please click on a Community...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import isOwnerInCommunity from '../../utils/isOwnerInCommunity.js';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_COMMUNITY_READ } from '../../constants.js';

  export default {
    name: 'community-detail',
    mixins: [
      isOwnerInCommunity
    ],
    data() {
      return {
        community: undefined,
        error: undefined,
      }
    },
    beforeMount() {
      if (this.community === undefined)
        this.retrieveCommunity(this.$route.params.slug);
    },

    beforeRouteUpdate(to, from, next) {
      if (from.params.slug != to.params.slug) {
        this.retrieveCommunity(to.params.slug);
        next();
      }
    },

    methods: {
      retrieveCommunity(slug) {
        getAPI.get(URL_API_COMMUNITY_READ.replace(':slug', slug))
          .then(response => {
            this.community = response.data;
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