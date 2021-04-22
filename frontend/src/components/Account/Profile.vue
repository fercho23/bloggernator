<template>
  <div class="row">
    <div class="col-12 shadow-sm">
      <template v-if="user">
        <router-link
          v-if="isYourProfile(user)"
          class="btn btn-primary float-right"
          :to="{
            name: 'profile-update',
            params: { user: user, username: user.username }
          }">
          Update
        </router-link>

        <h3>Profile</h3>

        <div class="row">
          <div class="col-3">
            <img v-bind:src="user.photo || urlImageUserDefault" alt="User Photo" class="img-thumbnail" width="100%">
          </div>
          <div class="col-9">
            <dl>
                <dt>Username</dt>
                <dd class="ml-4">{{ user.username }}</dd>

                <dt>Date Joined</dt>
                <dd class="ml-4">{{ formatDate(user.date_joined) }}</dd>

                <template v-if="user.owns_communities.length">
                  <dt>Owner of</dt>
                  <dd v-for="(community, index) in user.owns_communities" :key="index" class="ml-4">
                    <router-link
                      :to="{
                        name: 'community-detail',
                        params: { slug: community.slug }
                      }">
                      {{ community.name }}
                    </router-link>
                  </dd>
                </template>

                <template v-if="user.member_communities.length">
                  <dt>Member of</dt>
                  <dd v-for="(community, index) in user.member_communities" :key="index" class="ml-4">
                    <router-link
                      :to="{
                        name: 'community-detail',
                        params: { slug: community.slug }
                      }">
                      {{ community.name }}
                    </router-link>
                  </dd>
                </template>
            </dl>
          </div>
        </div>
      </template>
      <template v-else="">
        <span v-if="errorGetUser">Profile Error: {{ errorGetUser }}</span>
      </template>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import formatDate from "../../utils/formatDate.js";
  import { getAPI } from "../../api/axios-base";
  import { URL_API_USER_READ, URL_IMAGE_USER_DEFAULT } from "../../constants.js";

  export default {
    name: "profile",
    computed: mapState(["currentUser"]),
    mixins: [
      formatDate
    ],
    data() {
      return {
        user: undefined,
        errorGetUser: undefined,
        urlImageUserDefault: URL_IMAGE_USER_DEFAULT,
      }
    },
    beforeMount() {
      let username = this.$route.params.username;
      if (username == undefined)
        username = this.currentUser.username;
      this.getUser(username);
    },
    methods: {
      isYourProfile(user) {
        const uuid = this.$store.state.currentUser.uuid;
        if (user.uuid == uuid)
          return true;

        return false;
      },

      getUser(username) {
        getAPI.get(URL_API_USER_READ.replace(':username', username))
          .then((response) => {
            this.user = response.data;
          })
          .catch(e => {
            this.errorGetUser = e.response.data.detail;
          });
      }
    }
  }
</script>