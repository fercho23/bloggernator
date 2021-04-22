<template>
  <div class="row">
    <div class="col-12">
      <template v-if="community">
        <router-link
          v-if="isOwner(community)"
          class="btn btn-primary float-right"
          :to="{
            name: 'community-update',
            params: { community: community, slug: community.slug }
          }">
          Update
        </router-link>

        <h3>Community Detail</h3>

        <div class="row">
          <div class="col-12">
            <dl>
                <dt>Name</dt>
                <dd class="ml-4">{{ community.name }}</dd>

                <template v-if="community.owner && Object.keys(community.owner).length">
                  <dt>Owner</dt>
                  <dd class="ml-4">
                    <router-link
                      :to="{
                        name: 'profile',
                        params: { slug: community.owner.username }
                      }">
                      {{ community.owner.username }}
                    </router-link>
                  </dd>
                </template>

                <template v-if="community.detail">
                  <dt>Detail</dt>
                  <dd class="ml-4">{{ community.detail }}</dd>
                </template>

                <template v-if="community.members.length">
                  <dt>Members</dt>
                  <dd v-for="(user, index) in community.members" :key="index" class="ml-4">
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
      </template>
      <template v-else="">
        <span v-if="error">Community Error: {{ error }}</span>
        <p>Please click on a Community...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import { getAPI } from "../../api/axios-base";
  import { URL_API_COMMUNITY_READ } from "../../constants.js";

  export default {
    name: "community-detail",
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
    beforeRouteUpdate(to) {
      this.retrieveCommunity(to.params.slug);
    },
    methods: {
      isOwner(community) {
        const uuid = this.$store.state.currentUser.uuid;
        if (community.owner.uuid == uuid)
          return true;

        return false;
      },

      retrieveCommunity(slug) {
        getAPI.get(URL_API_COMMUNITY_READ.replace(":slug", slug))
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