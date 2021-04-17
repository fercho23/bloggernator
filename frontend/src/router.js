
import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("./components/Home.vue"),
    },

    {
      path: '/login',
      name: 'login',
      component: () => import("./components/Account/Login.vue"),
      meta: {
        requiresLogged: true
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import("./components/Account/Signup.vue"),
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import("./components/Account/Logout.vue"),
      meta: {
        requiresAuth: true
      }
    },

    {
      path: "/post/list",
      name: "post-list",
      component: () => import("./components/Posts/PostList.vue"),
    },
    {
      path: "/post/create",
      name: "post-create",
      component: () => import("./components/Posts/PostCreate.vue"),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/post/:slug",
      name: "post-details",
      component: () => import("./components/Posts/PostDetail.vue"),
      props: true
    },
    // {
    //   path: "/post/:slug/delete",
    //   name: "post-details",
    //   component: () => import("./components/Posts/PostDelete.vue"),
    //   meta: {
    //     requiresAuth: true
    //   }
    //   props: true
    // },
    {
      path: "/post/:slug/update",
      name: "post-update",
      component: () => import("./components/Posts/PostUpdate.vue"),
      meta: {
        requiresAuth: true
      },
      props: true
    }
  ]
});
