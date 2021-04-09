
<template>
    <div id="app">
      <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
          <div class="container container-fluid">
            <b-navbar-brand href="/">
              <font-awesome-icon :icon="['fas', 'home']" />
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
              <b-navbar-nav>
                <b-nav-item href="/post/list">Posts</b-nav-item>
              </b-navbar-nav>

              <!-- Right aligned nav items -->
              <b-navbar-nav class="ml-auto">

                <b-nav-item-dropdown text="Lang" right>
                  <b-dropdown-item href="#">EN</b-dropdown-item>
                  <b-dropdown-item href="#">ES</b-dropdown-item>
                  <b-dropdown-item href="#">RU</b-dropdown-item>
                  <b-dropdown-item href="#">FA</b-dropdown-item>
                </b-nav-item-dropdown>

                <b-nav-item-dropdown right>
                  <template #button-content>
                    <em>User</em>
                  </template>
                  <b-dropdown-item href="#">Profile</b-dropdown-item>
                  <b-dropdown-item href="#">Sign Out</b-dropdown-item>
                </b-nav-item-dropdown>

              </b-navbar-nav>
            </b-collapse>

          </div>
        </b-navbar>
      </div>

      <div class="container container-fluid mt-2">
        <router-view/>
      </div>
    </div>
</template>

<script>
export default {
  name: "app"
};
</script>

<style>
</style>