<template>
  <div class="row">
    <div class="col-12">

      <div class="float-right">
        <router-link
          v-if="accessToken!=null"
          class="btn btn-primary"
          :to="{
            name: 'community-create'
          }">
          Create Community
        </router-link>
      </div>

      <h3>Community List</h3>

      <div class="row">
        <div class="col-12">
          <Pagination
            :key="communitiesKey"
            :baseUrl="baseUrl"
            :query="communitiesQuery"
            :pageCount="communitiesCount"
            :previousUrl="communitiesPrevious"
            :nextUrl="communitiesNext"
          />
        </div>

        <!--
        <div class="col-6" v-for="(community, index) in communities" :key="index">
          <router-link
            title="Community Detail"
            :to="{
              name: 'community-detail',
              params: { community: community, slug: community.slug }
            }">
            {{ community.name }}
          </router-link>
        </div>
        -->

        <div class="col-12">
          <b-card v-for="(community, index) in communities" :key="index"
            :img-src="community.photo || urlImageCommunityDefault"
            img-height="200"
            img-width="200"
            :title="community.name"
            :img-alt="community.name"
            :img-left="index % 2 == 0"
            :img-right="index % 2 != 0"
            class="mb-2"
            border-variant="secondary"
            >
            <b-card-text>
                <br>
                <router-link
                  :to="{
                    name: 'community-detail',
                    params: { community: community, slug: community.slug }
                  }">
                  See ...
                </router-link>
            </b-card-text>
          </b-card>
        </div>

        <div class="col-12">
          <Pagination
            :key="communitiesKey"
            :baseUrl="baseUrl"
            :query="communitiesQuery"
            :pageCount="communitiesCount"
            :previousUrl="communitiesPrevious"
            :nextUrl="communitiesNext"
            :scrollToTopOnClick="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Pagination from '../Layout/Pagination';
  import { mapState } from 'vuex';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_COMMUNITY_LIST, URL_IMAGE_COMMUNITY_DEFAULT } from '../../constants.js';

  export default {
    name: 'community-list',
    components: {
      Pagination
    },
    computed: mapState(['accessToken']),
    data() {
      return {
        baseUrl: window.location.pathname,
        communities: [],
        communitiesCount: null,
        communitiesPrevious: null,
        communitiesNext: null,
        communitiesQuery: null,
        communitiesKey: null,
        urlImageCommunityDefault: URL_IMAGE_COMMUNITY_DEFAULT,
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

        this.communitiesQuery = query;
        getAPI.get(URL_API_COMMUNITY_LIST, {
            params: query
          })
          .then(response => {
            this.communities = response.data.results;
            this.communitiesCount = response.data.count;
            this.communitiesPrevious = response.data.previous;
            this.communitiesNext = response.data.next;
            this.communitiesKey = Date.now();
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