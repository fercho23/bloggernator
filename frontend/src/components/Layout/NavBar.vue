<template>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <div class="container container-fluid">
          <b-navbar-brand href="/">
            <font-awesome-icon :icon="['fas', 'home']" />
          </b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
              <b-nav-item :to="{name: 'post-list'}">Posts</b-nav-item>
              <b-nav-item :to="{name: 'community-list'}">Communities</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <b-nav-form @submit.prevent="callNavbarSearch">
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search" id="navbarSearchTitle"></b-form-input>
                <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
              </b-nav-form>

              <b-nav-item-dropdown text="Lang" right>
                <b-dropdown-item v-for="(language, index) in allLanguages" :key="index">
                  {{ language.name }}
                </b-dropdown-item>
              </b-nav-item-dropdown>

              <template v-if="accessToken==null">
                <b-nav-item v-if="accessToken==null" :to="{name: 'signup'}">Signup</b-nav-item>
                <b-nav-item v-if="accessToken==null" :to="{name: 'login'}">Login</b-nav-item>
              </template>
              <template v-else="">
                <b-nav-item-dropdown text="Community" right>
                  <b-dropdown-item v-for="(community, index) in currentUser.owns_communities" 
                    :key="index" 
                    :to="{
                      name: 'community-detail',
                      params: { slug: community.slug }
                    }">{{ community.name }}
                  </b-dropdown-item>
                </b-nav-item-dropdown>

                <b-nav-item-dropdown right>
                  <template #button-content>
                    <em>User</em>
                  </template>

                  <b-dropdown-item :to="{name: 'post-create'}">Create Post</b-dropdown-item>
                  <b-dropdown-item :to="{name: 'profile'}">Profile</b-dropdown-item>
                  <b-dropdown-item :to="{name: 'logout'}">Logout</b-dropdown-item>
                </b-nav-item-dropdown>
              </template>

            </b-navbar-nav>
          </b-collapse>

        </div>
      </b-navbar>
    </div>
</template>

<script>
  import { mapState } from "vuex";

  export default {
    name: "NavBar",
    computed: mapState(["accessToken", "currentUser", "allLanguages"]),

    // beforeMount() {
    //   console.log(this.currentUser);
    // },

    // beforeRouteUpdate(to, from) {
    //   console.log(to);
    //   console.log(from);
    // },

    methods: {
      callNavbarSearch() {
        let title = document.getElementById("navbarSearchTitle").value;

        this.$router.push({
          name: "post-list",
          query: { title: title }
        });
      }
    }
  }
</script>