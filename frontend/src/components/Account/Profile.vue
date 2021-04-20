<template>
  <div class="row">
    <div class="col-12 shadow-sm">
      <template v-if="user">
        <h3>Profile</h3>

        <div class="row">
          <div class="col-3">
            <img v-bind:src="user.photo || urlImageUserDefault" alt="User Photo" class="img-thumbnail" width="100%">
          </div>
          <div class="col-9">
            <dl>
                <dt>Username</dt>
                <dd>{{ user.username }}</dd>

                <dt>Date Joined</dt>
                <!--
                <dd>{{ user.date_joined | dateFormat('YYYY-MM-DDTHH:mm:ss.sssZ') | dateFormat('MMMM D, YYYY') }}</dd>
                -->
                <dd>{{ formatDate(user.date_joined) }}</dd>
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
      getUser(username) {
        getAPI.get(URL_API_USER_READ.replace(':username', username))
          .then((response) => {
            this.user = response.data;
            console.log(formatDate(response.data.date_joined));
          })
          .catch(e => {
            this.errorGetUser = e.response.data.detail;
          });
      }
    }
  }
</script>