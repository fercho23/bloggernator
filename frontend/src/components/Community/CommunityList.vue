<template>
  <div class="row">
    <div class="col-12">
      <!--
      <router-link
        v-if="accessToken!=null"
        class="btn btn-primary float-right"
        :to="{
          name: 'community-create'
        }">
        Create Community
      </router-link>
      -->
      <h3>Community List</h3>

      <div class="row">
        <div class="col-6" v-for="(community, index) in communities" :key="index">
          <router-link
            title="Community Detail"
            :to="{
              name: 'community-detail',
              params: { community: community, slug: community.slug }
            }">
            {{ community.title }}
          </router-link>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import { getAPI } from "../../api/axios-base";
  import { URL_API_COMMUNITY_LIST } from "../../constants.js";

  export default {
    name: "community-list",
    computed: mapState(["accessToken"]),
    data() {
      return {
        communities: []
      };
    },

    beforeRouteUpdate(to, from, next) {
      if (from.query != to.query) {
        this.retrieveCommunityList(to.query);
        next();
      }
    },

    mounted() {
      this.retrieveCommunityList();
    },

    methods: {
      retrieveCommunityList(query=undefined) {
        if (query == undefined)
          query = this.$route.query;

        getAPI.get(URL_API_COMMUNITY_LIST, {
            params: query
          })
          .then(response => {
            this.communities = response.data.results;
          })
          .catch(e => {
            console.log(e);
          });
      }
    }
  };
</script>

<style>
</style>