<template>
<!--   <div class="nav-bar">
    <ul>
      <li v-if="accessToken==null"><router-link :to = "{ name:'register' }">REGISTER</router-link></li>
      <li v-if="accessToken==null"><router-link :to = "{ name:'login' }">LOGIN</router-link></li>
      <li v-if="accessToken!=null"><router-link :to = "{ name:'logout' }">LOGOUT</router-link></li>
      <li><router-link :to = "{ name:'downloads' }">DOWNLOADS</router-link></li>
      <li><router-link :to = "{ name:'home' }" exact>HOME</router-link></li>
    </ul>
  </div> -->

    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <div class="container container-fluid">
          <b-navbar-brand href="/">
            <font-awesome-icon :icon="['fas', 'home']" />
          </b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
              <b-nav-item :to="{name: 'post-list'}">Posts</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">

              <b-nav-item-dropdown text="Lang" right>
                <b-dropdown-item href="#">EN</b-dropdown-item>
                <b-dropdown-item href="#">ES</b-dropdown-item>
              </b-nav-item-dropdown>

              <b-nav-item v-if="accessToken==null" :to="{name: 'login'}">Login</b-nav-item>

              <b-nav-item-dropdown v-else="" right>
                <template #button-content>
                  <em>User</em>
                </template>
                <b-dropdown-item href="#">Profile</b-dropdown-item>
                <b-dropdown-item :to="{name: 'logout'}">Logout</b-dropdown-item>
              </b-nav-item-dropdown>

            </b-navbar-nav>
          </b-collapse>

        </div>
      </b-navbar>
    </div>

</template>

<script>
  import { mapState } from 'vuex'
  export default {
    name: 'NavBar',
    computed: mapState(['accessToken'])
  }
</script>